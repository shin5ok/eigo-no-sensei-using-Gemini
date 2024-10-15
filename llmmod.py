
import vertexai

from vertexai.generative_models import GenerativeModel, ChatSession

import config as c

project_id = c.PROJECT_ID
location = c.LOCATION


vertexai.init(project=project_id, location=location)

def gen_system_intruction():
    instructions = []
    with open("prompts.md", "r") as f:
        instructions = f.readlines()
    return instructions

model = GenerativeModel(
        model_name="gemini-1.5-flash-002",
        system_instruction=gen_system_intruction(),
)

def get_chat_session() -> ChatSession:
    chat = model.start_chat()
    return chat

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

