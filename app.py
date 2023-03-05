import os
import re
import time
from threading import Thread

from revChatGPT.revChatGPT import Chatbot
from slack_bolt import App

ChatGPTConfig = {
        "email": os.environ['CHATGPT_EMAIL'],
        "password": os.environ['CHATGPT_PASSWORD']
    }

app = App()
chatbot = Chatbot(ChatGPTConfig, conversation_id=None)

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

    # Get the `ts` value of the original message
    original_message_ts = event["ts"]

    # Use the `app.event` method to send a reply to the message thread
    say(send, thread_ts=original_message_ts)

def chatgpt_refresh():
    while True:
        chatbot.refresh_session()
        time.sleep(60)

if __name__ == "__main__":
    thread = Thread(target=chatgpt_refresh)
    thread.start()
    app.start(4000)  # POST http://localhost:4000/slack/events
    
