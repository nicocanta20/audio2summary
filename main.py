import streamlit as st
import openai
from pydub import AudioSegment

def ogg2mp3(file):
    sound = AudioSegment.from_ogg(file)
    sound.export("audio.mp3", format="mp3")
    return "audio.mp3"

def audio2text(audio_file):
    # read the audio file
    audio_file= open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    res= transcript['text']
    return res

def summary(text):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant and must make a summary of the following conversation. Must return a bullet point list of the main points of the conversation. Additionaly return the 3 most important ideas of the conversation."},
        {"role": "user", "content": text},
    ])
    return response.choices[0]["message"]["content"]


def warning_api_key(openai_api_key):
     if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

def main():
    st.title("Audio2Summary")
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/nicocanta20/audio2summary.git)"
    

    audio_file = st.file_uploader("Upload Audio", type=["ogg", "wav", "mp3"])
    if st.button("Start", key="whisper"):
        if audio_file:
            try:
                if audio_file.type == "audio/ogg":
                    audio_file = ogg2mp3(audio_file)

                warning_api_key(openai_api_key)
                openai.api_key = openai_api_key
                text = audio2text(audio_file)
                response = summary(text)
                if response:
                    st.subheader("Summary of the audio file:")
                    st.write(response)
                    with st.expander("Show complete transcript of the audio file"):
                        st.write(text)

            except:
                st.error("Something went wrong. Please try again.", icon="🚨")

if __name__ == "__main__":
    main()
