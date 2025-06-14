from flask import Flask, request
import os

app = Flask(__name__)

# 這個字串等等在 Meta webhook 驗證時也要填一樣的
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'my_secret_token')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # webhook 驗證邏輯：Meta 要求我們返回 challenge
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("✅ Webhook 驗證成功")
            return challenge
        else:
            print("❌ Webhook 驗證失敗")
            return '驗證失敗', 403

    if request.method == 'POST':
        # 實際收到 IG 留言時會觸發這裡
        data = request.json
        print("💬 收到留言資料：", data)
        return 'OK', 200

if __name__ == '__main__':
    print("⚡ Flask 準備啟動囉！")
    app.run(port=5000)