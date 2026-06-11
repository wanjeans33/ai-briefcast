"""Doubao TTS 2.0 双向流式 WebSocket 客户端 (v3 二进制协议).

用法: python scripts/doubao_tts_ws.py "要合成的文本" 输出.mp3
依赖: websockets
"""
import asyncio, json, os, struct, sys, uuid
import websockets


def _load_dotenv():
    """从仓库根目录的 .env 读取密钥（该文件已 gitignore，不入库）。"""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (".env", os.path.join(here, "..", ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            break


_load_dotenv()

# 密钥来源优先级：环境变量 > 仓库根 .env（见 .env.example）
#   VOLC_APP_ID / VOLC_API_KEY / VOLC_SPEAKER
APP_ID = os.environ.get("VOLC_APP_ID", "")
API_KEY = os.environ.get("VOLC_API_KEY", "")
RESOURCE_ID = os.environ.get("VOLC_RESOURCE_ID", "seed-icl-2.0")
SPEAKER = os.environ.get("VOLC_SPEAKER", "")
WS_URL = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"

if not (APP_ID and API_KEY and SPEAKER):
    sys.exit("请先设置环境变量 VOLC_APP_ID / VOLC_API_KEY / VOLC_SPEAKER")

# 协议常量
PROTO = 0x11            # version=1, header size=1 (4 bytes)
SER_JSON = 0x10         # serialization=JSON(1), compression=none(0)
SER_RAW = 0x00          # for audio
MSG_FULL_CLIENT = 0x14  # full client request (0x1) | with-event flag (0x4)
# server msg types: 0x9 full server resp, 0xb audio-only, 0xf error

# events
EV_StartConnection = 1
EV_FinishConnection = 2
EV_StartSession = 100
EV_FinishSession = 102
EV_TaskRequest = 200


def build(event, payload: dict, session_id: str | None = None):
    body = bytearray([PROTO, MSG_FULL_CLIENT, SER_JSON, 0x00])
    body += struct.pack(">i", event)
    if session_id is not None:
        sid = session_id.encode()
        body += struct.pack(">I", len(sid)) + sid
    pl = json.dumps(payload).encode()
    body += struct.pack(">I", len(pl)) + pl
    return bytes(body)


def parse(data: bytes):
    b0, b1 = data[0], data[1]
    msg_type = b1 >> 4
    flags = b1 & 0x0f
    off = (b0 & 0x0f) * 4
    event = None
    if flags & 0x04:
        event = struct.unpack(">i", data[off:off+4])[0]; off += 4
    # length-prefixed connection/session id
    sid = None
    if off + 4 <= len(data):
        ln = struct.unpack(">I", data[off:off+4])[0]
        if 0 <= ln < 256 and off + 4 + ln + 4 <= len(data) + 4:
            sid = data[off+4:off+4+ln].decode("utf-8", "replace"); off += 4 + ln
    # length-prefixed payload
    payload = b""
    if off + 4 <= len(data):
        pl = struct.unpack(">I", data[off:off+4])[0]; off += 4
        payload = data[off:off+pl]
    return msg_type, event, sid, payload


async def recv(ws):
    msg = await asyncio.wait_for(ws.recv(), timeout=20)
    if isinstance(msg, str):
        print("TEXT:", msg[:200]); return None
    return parse(msg)


def pad_tail(t: str) -> str:
    """末尾补一个停顿缓冲，避免双向流式 TTS 把最后一个字截掉。

    服务端在收到 FinishSession 后停止生成，末 token 有时来不及解码完整，
    导致「最后一个字」被吞。补一句末标点（纯停顿、不发音）给解码器留出余量。
    """
    t = (t or "").rstrip()
    if not t:
        return t
    if t[-1] not in "。！？!?…":
        t += "。"
    # 末字偶发被流式解码截掉；补一段「逗号停顿 + 多句号」给解码器留足余量
    return t + "，。。。"


async def main(text, out_path):
    text = pad_tail(text)
    headers = {
        "x-api-key": API_KEY,
        "X-Api-App-Id": APP_ID,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Connect-Id": str(uuid.uuid4()),
    }
    audio = bytearray()
    async with websockets.connect(WS_URL, additional_headers=headers, max_size=None) as ws:
        sid = str(uuid.uuid4())
        # 1. connection
        await ws.send(build(EV_StartConnection, {}))
        mt, ev, s, pl = await recv(ws)
        print(f"  <- event {ev} (expect 50 ConnectionStarted)")
        # 2. session with full req_params
        audio_params = {"format": "mp3", "sample_rate": 24000}
        try:
            sr = float(os.environ.get("VOLC_SPEECH_RATE", "") or 0)
        except ValueError:
            sr = 0
        if sr:
            audio_params["speech_rate"] = sr   # 语速，正数更快（范围约 -50~100）
        await ws.send(build(EV_StartSession, {
            "event": EV_StartSession,
            "namespace": "BidirectionalTTS",
            "req_params": {
                "speaker": SPEAKER,
                "audio_params": audio_params,
            },
        }, sid))
        mt, ev, s, pl = await recv(ws)
        print(f"  <- event {ev} (expect 150 SessionStarted) {pl[:120]}")
        # 3. send text
        await ws.send(build(EV_TaskRequest, {
            "event": EV_TaskRequest,
            "namespace": "BidirectionalTTS",
            "req_params": {"text": text, "speaker": SPEAKER},
        }, sid))
        # 4. finish session -> triggers synthesis
        await ws.send(build(EV_FinishSession, {"event": EV_FinishSession}, sid))
        # 5. read audio until SessionFinished
        while True:
            r = await recv(ws)
            if r is None:
                continue
            mt, ev, s, pl = r
            if mt == 0xb:
                audio += pl
                print(f"  audio frame event={ev} +{len(pl)} bytes (total {len(audio)})")
            elif mt == 0xf:
                print("  ERROR:", pl.decode("utf-8", "replace")[:300]); break
            else:
                print(f"  msg_type={mt:#x} event={ev} payload={pl.decode('utf-8','replace')[:150]}")
            if ev in (152, 153):
                break
        await ws.send(build(EV_FinishConnection, {}))
    if audio:
        with open(out_path, "wb") as f:
            f.write(audio)
        print(f"WROTE {out_path} : {len(audio)} bytes")
    else:
        print("NO AUDIO RECEIVED")


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "大家好，欢迎收听今天的 AI 简报。"
    out = sys.argv[2] if len(sys.argv) > 2 else "audio_output/libairan_zh.mp3"
    asyncio.run(main(text, out))
