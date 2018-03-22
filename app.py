import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('68OMZuFJsIFTH0NY4hwT+AhNFXc3vuCwhCSpxLEIJqSrYF1d/1R9fzln9QkQwPDfJp0LnaaeQ49Cdw/I5HsEWmaf4T2tdQRCYTEelatKA9t9q/nUaQKRFzUeX0x9z3H2MBMvfqtFROaKFUutAqp7IgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ddc9210bc0da8745bd9893deccf980cf')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
