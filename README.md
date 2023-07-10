# Buddyhelper AI cli
- How and why <b>Buddy Helper AI</b> is born https://medium.com/@buddyhelperai/buddyhelperai-410fa1a4774c
- What is Helper (in Buddy Helper AI) https://medium.com/@buddyhelperai/what-is-helper-in-buddy-helper-ai-f3b28862aba4
- How to design a Helper https://medium.com/@buddyhelperai/how-to-designa-helper-for-a-task-a-video-example-buddy-helper-ai-9cc4b3b8aee6

## Why a cli?
Buddy Helper AI is the project, the cli (Command Line Interface) is just a simple way to start.

## Install on Ubuntu/Python
```
pip install llama-index
pip install openai
```

## Understand the "chat with" document method
https://github.com/buddyhelperai/chat-with-documents
<br>
https://medium.com/@buddyhelperai/chat-with-documents-7aeecbe1d06c

## Understand the "helper" method
https://medium.com/@buddyhelperai/what-is-helper-in-buddy-helper-ai-f3b28862aba4

## main.py
This is a Python piece code mainly based on llama index (with OpenAI API Key) and openai. It is a very simple Python script, and it should be more complex/advanced: it provides an chat-alike prompt with IF statements that answers to specific keywords.

### Commands
#### create
```
create helper [helper-based-on] [new-helper-name] => to create an helper based on an existing helper (see config.js to find existing helpers)
```
#### get
```
get [new-helper-name] => to see helper's features
```
#### use (with 3 options: (1) for view, (2) for change/edit, (3) for run
```
use helper [new-helper-name] => to start a chat to use the helper
```
#### assistant
chat with gpt-3.5-model. Use "chat-reset" to reset the chat history and start a new chat.
