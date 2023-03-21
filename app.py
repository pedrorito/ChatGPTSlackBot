import os
import re
import time
from threading import Thread

from revChatGPT.V3 import Chatbot
from slack_bolt import App

ChatGPTConfig = {
    "api_key": os.getenv("OPENAI_API_KEY"),
}

if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

app = App()
chatbot = Chatbot(**ChatGPTConfig)


@app.event("app_mention")
def event_test(event, say):
    prompt = re.sub('\\s<@[^, ]*|^<@[^, ]*', '', event['text'])
    try:
        response = chatbot.ask(prompt)
        user = event['user']
        send = f"<@{user}> {response}"
    except Exception as e:
        print(e)
        send = "We're experiencing exceptionally high demand. Please, try again."

    # Get the `ts` value of the original message
    original_message_ts = event["ts"]

    # Use the `app.event` method to send a reply to the message thread
    say(send, thread_ts=original_message_ts)


def chatgpt_refresh():
    while True:
        time.sleep(60)


if __name__ == "__main__":
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
