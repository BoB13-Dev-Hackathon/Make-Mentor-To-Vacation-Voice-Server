
import os, sys, base64
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="VQUrqlK1umy7kNUW0AXa", 
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path



@app.route('/chain', methods=['POST'])
def _chain():
    mp3 = text_to_speech_file(request.json['prompt'])
    f = open(mp3, 'rb')
    b = base64.b64encode(f.read())
    f.close()
    return Response(b, mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True, debug=True)