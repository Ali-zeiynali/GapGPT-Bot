from local_config import get_setting
import json
import ssl
import time
import threading
import websocket

# ========== اطلاعاتتو بذار اینجا ==========
ACCESS_TOKEN = get_setting("GAPGPT_ACCESS_TOKEN")
CHAT_TOKEN = get_setting("GAPGPT_CHAT_TOKEN")
# =========================================

def ask(question):
    """
    سوال رو میپرسه و جواب رو سریع برمیگردونه.
    """
    answer = []
    done = threading.Event()

    def on_open(ws):
        # دست‌تکون اولیه
        ws.send(json.dumps({"token": ACCESS_TOKEN, "version": 82}))
        time.sleep(0.5)
        # ارسال سوال
        ws.send(json.dumps({"chat_token": CHAT_TOKEN, "text": question}))

    def on_message(ws, raw_msg):
        data = json.loads(raw_msg)
        if data.get("event") == "new_message":
            # گرفتن متن پاسخ
            content = data["data"]["message"]["response"][0]["content"]
            answer.append(content)
            ws.close()
            done.set()

    def on_error(ws, err):
        done.set()

    ws = websocket.WebSocketApp(
        "wss://gapgpt.app/ws/salam",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error
    )

    # اجرا در نخ جداگانه
    t = threading.Thread(
        target=ws.run_forever,
        kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}}
    )
    t.daemon = True
    t.start()

    # صبر کن تا پاسخ دریافت بشه (حداکثر ۶۰ ثانیه)
    done.wait(60)
    ws.close()
    return answer[0] if answer else None


# ================= استفاده =================
if __name__ == "__main__":
    while True:
        msg = input("\n✍️ پیامت رو بنویس (exit برای خروج): ")
        if msg.lower() == "exit":
            break
        resp = ask(msg)
        if resp:
            print(f"\n🤖 {resp}")
        else:
            print("❌ پاسخی دریافت نشد (اینترنت یا توکن مشکل داره)")