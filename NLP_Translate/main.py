import openai

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,AudioMessage, TextSendMessage, AudioSendMessage, QuickReply, QuickReplyButton, MessageAction
from flask import Flask, request, abort

#透過讀檔帶入參數
app = Flask(__name__)
config = {}
with open("config.txt") as f:
    for line in f:
        list_line = line.strip().replace(" ","").split("=")
        config[list_line[0]] = list_line[1]

#line 、 openai  api key
LINE_CHANNEL_ACCESS_TOKEN = config.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = config.get("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = config.get("OPENAI_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai_key = OPENAI_API_KEY
openai.api_key = openai_key

translate_language = "Japanese"
audio_language = "Traditional Chinese"
translate_id = {}

lan_dic = {"日文": "Japanese", "英文": "English", "繁體中文": "Traditional Chinese", "韓文": "Korean", 
"法文":"French", "泰文": "Thai", "義大利文": "Italian", "西班牙文": "Spanish", "荷蘭文":"Dutch", "德文": "German"}
reverse_lan_dict = {value: key for key, value in lan_dic.items()}

print("access_token:"+LINE_CHANNEL_ACCESS_TOKEN)
print("secret:"+LINE_CHANNEL_SECRET)
print("openai:"+OPENAI_API_KEY)

#定義語音翻譯使用方式
def openai_whisper(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

#定義prompt使用方法帶入轉換語言
def translate_openai(text, trans_language):
    prompt = f"""'{text}'
    Help me to translate this sentence to {trans_language}, only target language, no need original language."""

    # openai api呼叫
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # engine = "deployment_name".
        messages= [{"role":"user", "content":prompt}],
        temperature = 0.5
    )
    translated_subtitles = response['choices'][0]['message']['content']
    return translated_subtitles

# 單純使用openai api
def only_openai(text):
    # openai api呼叫
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # engine = "deployment_name".
        messages= [{"role":"user", "content":text}],
        temperature = 0.5
    )
    translated_subtitles = response['choices'][0]['message']['content']
    return translated_subtitles

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print (body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global translate_language, audio_language
    user_input = event.message.text
    if (user_input == "/setting") or (user_input == "設定"):
        flex_message = TextSendMessage(text="請選擇語音辨識後的翻譯語言 (我方語言)",
                        quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="繁體中文", text="設定辨識翻譯 " + "繁體中文")),
                        QuickReplyButton(action=MessageAction(label="英文", text="設定辨識翻譯 " + "英文")),
                        QuickReplyButton(action=MessageAction(label="日文", text="設定辨識翻譯 " + "日文")),
                        QuickReplyButton(action=MessageAction(label="韓文", text="設定辨識翻譯 " + "韓文")),
                        QuickReplyButton(action=MessageAction(label="法文", text="設定辨識翻譯 " + "法文")),
                        QuickReplyButton(action=MessageAction(label="泰文", text="設定辨識翻譯 " + "泰文")),
                        QuickReplyButton(action=MessageAction(label="義大利文", text="設定辨識翻譯 " + "義大利文")),
                        QuickReplyButton(action=MessageAction(label="西班牙文", text="設定辨識翻譯 " + "西班牙文")),
                        QuickReplyButton(action=MessageAction(label="荷蘭文", text="設定辨識翻譯 " + "荷蘭文")),
                        QuickReplyButton(action=MessageAction(label="德文", text="設定辨識翻譯 " +"德文")),
                        ]))
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)
            
    elif ("設定辨識翻譯" in user_input):
        audio_language = lan_dic[user_input.split(" ")[1]]
        flex_message = TextSendMessage(text="請選擇打字後的翻譯語言 (對方語言)",
                        quick_reply=QuickReply(items=[
                        QuickReplyButton(action=MessageAction(label="繁體中文", text="設定打字翻譯 " + "繁體中文")),
                        QuickReplyButton(action=MessageAction(label="英文", text="設定打字翻譯 " + "英文")),
                        QuickReplyButton(action=MessageAction(label="日文", text="設定打字翻譯 " + "日文")),
                        QuickReplyButton(action=MessageAction(label="韓文", text="設定打字翻譯 " + "韓文")),
                        QuickReplyButton(action=MessageAction(label="法文", text="設定打字翻譯 " + "法文")),
                        QuickReplyButton(action=MessageAction(label="泰文", text="設定打字翻譯 " + "泰文")),
                        QuickReplyButton(action=MessageAction(label="義大利文", text="設定打字翻譯 " + "義大利文")),
                        QuickReplyButton(action=MessageAction(label="西班牙文", text="設定打字翻譯 " + "西班牙文")),
                        QuickReplyButton(action=MessageAction(label="荷蘭文", text="設定打字翻譯 " + "荷蘭文")),
                        QuickReplyButton(action=MessageAction(label="德文", text="設定打字翻譯 " +"德文")),
                        ]))
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)

    elif ("設定打字翻譯" in user_input):
        translate_language = lan_dic[user_input.split(" ")[1]]
        response = f"""設定完成!!!
我方語言: {reverse_lan_dict[audio_language]}
對方語言: {reverse_lan_dict[translate_language]}"""
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

    elif (user_input=="目前設定") or (user_input=="/current_setting"):
        response = f"我方語言: {reverse_lan_dict[audio_language]}, 對方語言: {reverse_lan_dict[translate_language]}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
    else:
        # response = translate_openai(user_input, translate_language)
        response = only_openai(user_input)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))

# 事件觸發 語音訊息
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    #取出消息ID。這個ID是每條消息的唯一標識符。
    global translate_language, audio_language
    #使用 LINE Bot API 的 get_message_content 方法來根據消息ID下載消息的內容。
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    with open(f'whisper_audio.m4a', 'wb') as f:
        f.write(message_content.content)
    whisper_text = openai_whisper(f'whisper_audio.m4a')
    # response_text = translate_openai(whisper_text, audio_language)
    response_text = only_openai(whisper_text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text))
    
if __name__ == '__main__':
    app.run()