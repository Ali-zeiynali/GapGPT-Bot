from local_config import get_setting
import asyncio
import websockets
import json
import uuid
import time
from datetime import datetime, timezone

# ========== فقط این سه مقدار رو از مرورگرت پر کن ==========
WS_URL = "wss://gapgpt.app/ws/salam"
ACCESS_TOKEN = get_setting("GAPGPT_ASYNC_ACCESS_TOKEN", fallback="GAPGPT_ACCESS_TOKEN")

# ========== ساخت ساده‌ترین پیام ==========
def make_message(text):
    now = datetime.now(timezone.utc).isoformat()
    return {
        "event": "new_message",
        "data": {
            "message": {
                "token": str(uuid.uuid4()),
                "text": text,
                "response": [],
                "created_at": now,
                "vote": 0,
                "chat_token": str(uuid.uuid4()),
                "file_name": None,
                "extra_display": {"mode": "", "status": ""},
                "is_v5": True,
                "status": "just_created",
                "can_regenerate": True,
                "all_responses": [],
                "images": [],
                "file_names": []
            },
            "sent_at": time.time()
        }
    }

async def main():
    # هدر ساده: فقط کوکی با accessToken
    cookie_str = f"accessToken={ACCESS_TOKEN}"
    headers = {"Cookie": cookie_str}

    print("🔌 اتصال...")
    async with websockets.connect(WS_URL, additional_headers=headers) as ws:
        print("✅ متصل. یک پیام آزمایشی می‌فرستم...")
        msg = make_message("سلام داداش")
        await ws.send(json.dumps(msg, ensure_ascii=False))
        print("📤 فرستادم، منتظر پاسخ...\n")

        while True:
            resp = await ws.recv()
            data = json.loads(resp)
            ev = data.get("event")

            if ev == "message_chunk":
                chunk = data.get("data", {}).get("chunk", "")
                print(chunk, end="", flush=True)

            elif ev == "message_complete" or ev == "agent_loop_complete":
                print("\n\n✅ تمام!")
                break

            elif ev == "error":
                print("❌ خطا:", json.dumps(data, indent=2, ensure_ascii=False))
                break

            elif ev == "ack_new_message":
                status = data["data"].get("status", "")
                if status == "unauthorized":
                    print("🚫 احراز نشد! احتمالاً توکن منقضی شده. یه توکن جدید از مرورگر بگیر.")
                else:
                    print("📨", ev, "→", json.dumps(data, indent=2, ensure_ascii=False))

            else:
                print("📨", ev, json.dumps(data, indent=2, ensure_ascii=False))

asyncio.run(main())