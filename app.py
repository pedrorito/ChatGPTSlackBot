import os
import re
import time
from threading import Thread

from revChatGPT.V3 import Chatbot
from slack_bolt import App

ChatGPTConfig = {
        "api_key":, os.getenv("OPENAI_API_KEY"),
    }
if os.getenv("OPENAI_ENGINE"):
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")

app = App()
chatbot = Chatbot(ChatGPTConfig)

# Listen for an event from the Events API
@app.event("app_mention")
def event_test(event, say):
    prompt = re.sub('(?:\s)<@[^, ]*|(?:^)<@[^, ]*', '', event['text'])
    try:
        response = chatbot.get_chat_response(prompt)
        user = event['user']
        user = f"<@{user}> you asked:"
        asked = ['>',prompt]
        asked = "".join(asked)
        send = [user,asked,response["message"]]
        send = "\n".join(send)
    except Exception as e:
        send = "We're experiencing exceptionally high demand. Please, try again."
    say(send)

def chatgpt_refresh():
    while True:
        chatbot.refresh_session()
        time.sleep(60)

if __name__ == "__main__":
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
    
