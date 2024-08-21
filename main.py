from pprint import pprint as pp

import chainlit as cl
from chainlit.input_widget import Select, Slider

import config as c
from llmmod import *

# 設定

PROJECT_ID = c.PROJECT_ID
BUCKET_NAME = c.BUCKET_NAME
LOCATION = c.LOCATION

# 設定
default_model = "Gemini-1.5-Flash"

@cl.set_chat_profiles
async def _set_chat_profile():
    profiles = []
    return profiles

@cl.on_chat_start
async def _on_chat_start():

    settings = await cl.ChatSettings(
        [
            Slider(
                id="MAX_TOKEN_SIZE",
                label="Max token size",
                initial=4096,
                min=1024,
                max=8192,
                step=512,
            ),
            Slider(
                id="TEMPARATURE",
                label="Temperature",
                initial=0.6,
                min=0,
                max=1,
                step=0.1,
            ),
        ]
    ).send()
    session = get_chat_session()
    cl.user_session.set("session", session)

    await setup_runnable(settings)

@cl.on_settings_update
async def setup_runnable(settings):
    profile = cl.user_session.get("chat_profile")
    return profile

@cl.on_message
async def _on_message(message: cl.Message):

    session = cl.user_session.get("session")
    content = get_chat_response(session, message.content)
    pp(dict(session=session))

    res = cl.Message(content=content)

    await res.send()
