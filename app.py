from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('O8PmWOJO5BdwzyLyoqG5KNxHeF+j0BTr7qcW4/q9cbuwd2y+X23LGmCLs7M0XQOrDPKDbnLWRfOAbSTOzqQBuH+4bO6JtY8MUsQcmN22cDymuoc7MPQEEeuvv6wsIChlmY/irrod9OMaYfLyFtBIBAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fafa550a433aab93d0d57739f3d21ef7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg == '貼圖':
        sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
    r = '很抱歉我聽不懂'
    if msg in ['hi','Hi']:
        r = '你好'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif '訂位' in msg :
        r = '你好,請輸入日期&時間'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()