import os
import re
import time
from threading import Thread
from flask import Flask

from revChatGPT.V3 import Chatbot
from slack_bolt import App

ChatGPTConfig = {
    "api_key": os.getenv("OPENAI_API_KEY"),
}

if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

app = App()
chatbot = Chatbot(**ChatGPTConfig)
flask_app = Flask(__name__)


def handle_event(event, say, is_mention):
    prompt = re.sub('\\s<@[^, ]*|^<@[^, ]*', '', event['text'])
    try:
        response = chatbot.ask(prompt)
        user = event['user']

        if is_mention:
            send = f"<@{user}> {response}"
        else:
            send = response
    except Exception as e:
        print(e)
        send = "We're experiencing exceptionally high demand. Please, try again."

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


@flask_app.route("/", methods=["GET"])
def health():
    return ""


def chatgpt_refresh():
    while True:
        time.sleep(60)


if __name__ == "__main__":
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
