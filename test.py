from local_config import get_setting
import json
import ssl
import time
import websocket

# ========== اطلاعات خودت ==========
ACCESS_TOKEN = get_setting("GAPGPT_ACCESS_TOKEN")
CHAT_TOKEN = get_setting("GAPGPT_CHAT_TOKEN")
WS_URL = "wss://gapgpt.app/ws/salam"
# ==================================

def test_payload(desc, payload):
    print(f"\n📤 در حال آزمایش {desc} ...")
    response_event = [None]

    def on_message(ws, msg):
        data = json.loads(msg)
        if data.get("event") == "new_message":
            # دریافت پاسخ کامل
            content = data["data"]["message"]["response"][0]["content"]
            response_event[0] = content
            print(f"✅ پاسخ دریافت شد: {content}")
            ws.close()
        else:
            print(f"ℹ️ پیام غیرمنتظره: {msg[:100]}")

    def on_error(ws, err):
        print(f"❌ خطای وب‌سوکت: {err}")

    def on_open(ws):
        # اول دست‌تکون بده (Auth)
        handshake = {"token": ACCESS_TOKEN, "version": 82}
        ws.send(json.dumps(handshake))
        # کمی صبر کن، بعد پیام اصلی رو بفرست
        time.sleep(0.5)
        ws.send(json.dumps(payload))

    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error
    )
    # اجرا با تایم‌اوت
    import threading
    def run():
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    time.sleep(10)  # حداکثر ۱۰ ثانیه منتظر بمون
    ws.close()
    if response_event[0] is None:
        print("⏰ پاسخی دریافت نشد (تایم‌اوت)")

# ۴ فرمت محتمل که بر اساس تجربه از این دست سایت‌ها حدس زده شده
payloads = [
    ("حالت ۱: action=send_message", {
        "action": "send_message",
        "chat_token": CHAT_TOKEN,
        "message": "سلام از ربات",
        "model": "A-GPT-5.2-PRO"
    }),
    ("حالت ۲: type=message", {
        "type": "message",
        "chat_token": CHAT_TOKEN,
        "text": "سلام از ربات",
        "model": "A-GPT-5.2-PRO"
    }),
    ("حالت ۳: event=user_message", {
        "event": "user_message",
        "data": {
            "chat_token": CHAT_TOKEN,
            "message": "سلام از ربات",
            "model": "A-GPT-5.2-PRO"
        }
    }),
    ("حالت ۴: فقط chat_token و text", {
        "chat_token": CHAT_TOKEN,
        "text": "سلام از ربات"
    })
]

for desc, payload in payloads:
    test_payload(desc, payload)
    time.sleep(2)  # فاصلهٔ بین تست‌ها