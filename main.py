import io
from pprint import pprint as pp

import chainlit as cl
from chainlit.element import ElementBased
from chainlit.input_widget import Slider

import google.cloud.speech as speech


import config as c
from llmmod import *

PROJECT_ID = c.PROJECT_ID
BUCKET_NAME = c.BUCKET_NAME
LOCATION = c.LOCATION

default_model = "Gemini-1.5-Flash"


@cl.step(type="tool")
async def speech_to_text(content: bytes):
    # クライアントを初期化
    client = speech.SpeechClient()

    import os
    # 音声の設定
    # audio = speech.RecognitionAudio(uri=f"gs://{os.environ.get('PROJECT_ID')}/test.wav")

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        sample_rate_hertz=48000,
        language_code="en-US",
        model="latest_long"
    )

    # 音声認識を実行
    response = client.recognize(config=config, audio=audio)

    # 結果を出力
    text = ""
    pp(response)
    for result in response.results:
        text += result.alternatives[0].transcript

    pp("text:"+text)
    return text

@cl.step(type="tool")
async def speech_to_text2(audio_content: bytes):
    """Transcribe an audio file.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
    Returns:
        cloud_speech.RecognizeResponse: The response from the recognize request, containing
        the transcription results
    """
    # Reads a file as bytes
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        # language_codes=["ja-JP"],
        model="latest_long",
        explicit_decoding_config=dict(encoding=cloud_speech.Encoding.ENCODING_UNSPECIFIED),
    )

    # with open("/Users/kawanos/Desktop/test.wav", "rb") as f:
    #     audio_content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    text = ""
    for result in response.results:
        text += result.alternatives[0].transcript
    print("text",text)

    return text

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


    message = get_chat_response(session, """
    挨拶と自己紹介をして、どんなテーマで英語の練習をしたいかを質問してください。
    フランクな言葉遣いで。
    例: 私の名前は〇〇です。今日はどんなテーマで英語の練習をしたいですか？
        例えば、職場の同僚との会話、友達との食事、海外旅行 など。
    """)
    await cl.Message(content=message).send()
    # await cl.Message(content="### どんなテーマで英語の練習をしたいですか?").send()

    # await setup_runnable(settings)

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = io.BytesIO()
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"

        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)
   
    cl.user_session.get("audio_buffer").write(chunk.data)

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

@cl.on_audio_end
async def on_audio_end(elements: list[ElementBased]):
    session = cl.user_session.get("session")
     # Get the audio buffer from the session
    audio_buffer: io.BytesIO = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)  # Move the file pointer to the beginning
    audio_file = audio_buffer.read()
    audio_mime_type: str = cl.user_session.get("audio_mime_type")

    text = await speech_to_text(audio_file)

    if text != "":
        content = get_chat_response(session, text)
        pp(dict(session=session))

        await cl.Message(content=content).send()
    else:
        await cl.Message(content="もう一度？").send()
