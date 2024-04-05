import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()


API_KEY = os.getenv("DEEPGRAM_API")


def transcrib(AUDIO_FILE):
    try:
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()
            print(f"File read: {file.name}")

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        print(transcript)
        return transcript

    except Exception as e:
        print(f"Exception: {e}")
