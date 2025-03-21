# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr
from brain_of_doc import encode_image, analyze_image_with_query
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doc import text_to_speech_with_gtts
import shutil
from flask import Flask
from fastapi import FastAPI
from gradio.routes import mount_gradio_app

# Add Flask app for health check
app = Flask(__name__)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Update the output_filepath in process_inputs function

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    else:
        speech_to_text_output = "Please record audio to transcribe."

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"
    import time
    output_filepath = f"doctor_response_{int(time.time())}.mp3"
     # Use gTTS instead of ElevenLabs since there's an auth issue
    voice_of_doctor = text_to_speech_with_gtts(
        input_text=doctor_response, 
        output_filepath="Temp.mp3"
    ) 

    return speech_to_text_output, doctor_response, voice_of_doctor

    '''# Fix the output path to match what's in the interface
    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="Temp.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor'''


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice")
    ],
    title="AI Doctor with Vision and Voice"
)

# Mount your Gradio interface
app = mount_gradio_app(app, iface, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        timeout_keep_alive=60,
        access_log=True
    )

#http://127.0.0.1:7860