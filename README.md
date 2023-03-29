# ChatGPT for Slack Bot
[![playwright-version](https://img.shields.io/badge/revChatGPT-0.0.31.5-green.svg)](https://github.com/acheong08/ChatGPT)
[![license](https://img.shields.io/badge/License-GPL%202.0-brightgreen.svg)](LICENSE)

This is a simple Slackbot that uses the [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT) `revChatGPT` package to respond to messages in Slack. It is designed to be used with the Slack Events API, and it listens for `app_mention` events, which are triggered when a user mentions the bot in a Slack channel.

When the bot receives a `app_mention` event, it extracts the user's message from the event payload, sends it to the `revChatGPT` package to generate a response, and then sends the response back to the user via Slack.

The `revChatGPT` package is used to handle authentication and communication with the GPT-3 API, and it is also used to refresh the session with the GPT-3 API on a regular basis. This is done in a separate thread to prevent the session from expiring while the bot is handling requests.

## Usage

To use the bot, you will need to install the dependencies and set the `CHATGPT_EMAIL` and `CHATGPT_PASSWORD` environment variables with your OpenAI credentials. You also need to set `SLACK_SIGNING_SECRET` and `SLACK_BOT_TOKEN` environment variables after creating the Slack App. You can then run the `app.py` script to start the bot.

```python
pip install -r requirements.txt
export SLACK_SIGNING_SECRET=slack_signing_secret
export SLACK_BOT_TOKEN=slack_bot_token
export OPENAI_API_KEY=you_openai_api_key
python app.py
```

Alternatively, you can use the containerized version by setting the environment variables in the `variables.env` file and then run

```
docker-compose up -d
```

Once the bot is running, you can mention it in a Slack channel to send it a message. For example, you can type `@my-bot hello` to send the message "hello" to the bot. The bot will respond with a generated message based on the GPT-3 model.

## ChatGPT Configuration

The `ChatGPTConfig` dictionary at the top of the `app.py` script contains the configuration for the `revChatGPT` package. It specifies the email and password for the OpenAI account that the bot will use to authenticate with the GPT-3 API. These values are read from the `CHATGPT_EMAIL` and `CHATGPT_PASSWORD` environment variables.

The `conversation_id` parameter in the `Chatbot` constructor is used to specify the ID of the conversation that the bot should use. If this parameter is not provided, the `revChatGPT` package will generate a new conversation ID for each message that the bot receives.

## Slack Configuration

By default, `app.py` is exposing port 4000 for Slack events. You may change the port number in the end of the script.

To configure the Slack App, follow [these](https://github.com/slackapi/python-slack-events-api/blob/main/example/README.rst) example instructions from the official SlackApi GitHub account.

For this bot, the required Scopes in `OAuth & Permissions` are:
* app_mentions:read
* chat:write
* im:write

For direct message required & config :
* `Enable bot direct messages` go to : Features -> App Home -> (Enable) Messages Tab
* `OAuth & Permissions` im:history

In the `Event Subscriptions`, you need to subscribe to the `app_mention` event.

## Limitations

The bot uses a pre-trained GPT-3 model, which means that its responses are limited to the information that is contained in the model. It may not be able to respond accurately to messages that are outside of the scope of the pre-trained model.

Additionally, the bot is only designed to handle `app_mention` events, so it will not respond to other types of messages. This can be easily extended by adding more event handlers to the `app.py` script.

## Notes

The `tls-client` python library that is used by the `revChatGPT` package does not currently support ARM architectures. As a result, the bot may not be able to run on devices with ARM processors. This limitation will be addressed in a future update.

## Disclaimer
This is a personal project and is not affiliated with OpenAI or Slack in any way.

## License
This project is released under the terms of the GPL 2.0 license. For more information, see the [LICENSE](LICENSE) file included in the repository.
