import os
import re
import sys
from threading import Thread

from flask import Flask
from revChatGPT.V3 import Chatbot
from slack_bolt import App

ChatGPTConfig = {
    "api_key": os.getenv("OPENAI_API_KEY"),
}

if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

flask_app = Flask(__name__)
app = App()
chatbot = Chatbot(**ChatGPTConfig)


def handle_event(event, say, is_mention):
    prompt = re.sub("\\s<@[^, ]*|^<@[^, ]*", "", event["text"])

    # Each thread should be a separate conversation
    convo_id = event.get("thread_ts") or event.get("ts") or ""

    try:
        response = chatbot.ask(prompt, convo_id=convo_id)
        user = event["user"]

        if is_mention:
            send = f"<@{user}> {response}"
        else:
            send = response
    except Exception as e:
        print(e, file=sys.stderr)
        send = "We are experiencing exceptionally high demand. Please, try again."

    if is_mention:
        # Get the `ts` value of the original message
        original_message_ts = event["ts"]
    else:
        original_message_ts = None

    # Use the `app.event` method to send a message
    say(send, thread_ts=original_message_ts)


@app.event("app_mention")
def handle_mention(event, say):
    handle_event(event, say, is_mention=True)


@app.event("message")
def handle_message(event, say):
    handle_event(event, say, is_mention=False)


def start_flask_app():
    flask_app.run(host='0.0.0.0', port=3000)


# Define a health check route that returns a 200 HTTP response code
@flask_app.route('/health', methods=['GET'])
def health_check():
    return 'Bot is healthy'


if __name__ == "__main__":
    print("Bot Started!", file=sys.stderr)
    thread = Thread(target=start_flask_app).start()
    app.start(port=4000)  # POST http://localhost:4000/slack/events
