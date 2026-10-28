# backend/app/main.py
import asyncio, math, time
from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket

app = FastAPI()

async def fake_stream():
    t0, seq = time.monotonic(), 0
    while True:
        t = time.monotonic() - t0
        roll = 0.4 * math.sin(t)
        q = [math.cos(roll/2), math.sin(roll/2), 0.0, 0.0]
        seq += 1
        yield {
            "schema_version": 1, "vehicle_id": "drone-01", "msg_type": "attitude",
            "t_boot_us": int(t * 1e6),
            "t_recv_utc": datetime.now(timezone.utc).isoformat(),
            "seq": seq,
            "payload": {"q": q, "rates_rad_s": [0.4*math.cos(t), 0, 0]},
        }
        await asyncio.sleep(0.1)   # 10 Hz, matching the link budget

@app.websocket("/ws")
async def ws(sock: WebSocket):
    await sock.accept()
    async for msg in fake_stream():
        await sock.send_json(msg)