import streamlit as st
import openai
from pydub import AudioSegment
import io

def process_file(file):
    byte_io = io.BytesIO(file.read())
    format_type = file.type.split("/")[1]  # Extracted format here
    if format_type == "ogg":
        sound = AudioSegment.from_ogg(byte_io)
    elif format_type == "wav":
        sound = AudioSegment.from_wav(byte_io)
    elif format_type in ["mp3", "mpeg"]:
        sound = AudioSegment.from_mp3(byte_io)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    return sound

def join_audios(audios):
    combined = AudioSegment.empty()
    for audio in audios:
        combined += audio
    return combined

def save_audio_to_file(audio, format="mp3"):
    temp_filename = "temp_audio_file." + format
    audio.export(temp_filename, format=format)
    return temp_filename

def audio2text(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def summary(text,language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarize the following conversation into bullet points."},
            {"role": "user", "content": "respond everything in " + language},
            {"role": "user", "content": text},
        ])
    return response.choices[0]["message"]["content"]

def warning_api_key(openai_api_key):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

def main():
    st.title("Audio2Summary")
    st.write("### Powered by OpenAI's [Whisper](https://platform.openai.com/docs/guides/speech-to-text) and [GPT-3.5 Turbo](https://platform.openai.com/docs/guides/gpt)")
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        st.divider()
        st.write('#### By: \n - [Nicolas Cantarovici](https://github.com/nicocanta20) \n - [Florian Reyes](https://github.com/florianreyes)')
    
    audio_files = st.file_uploader("Upload Audio(s)", type=["ogg", "wav", "mp3", "mpeg"], accept_multiple_files=True)
    language = st.selectbox("Language", ["English", "Spanish"])

    if st.button("Start", key="whisper"):
        if audio_files:
            try:
                audios = []
                for audio_file in audio_files:
                    audios.append(process_file(audio_file))

                combined_audio = join_audios(audios)
                combined_audio_path = save_audio_to_file(combined_audio)

                warning_api_key(openai_api_key)
                openai.api_key = openai_api_key

                with open(combined_audio_path, "rb") as f:
                    text = audio2text(f)

                response = summary(text, language)
                
                if response:
                    st.subheader("Summary of the audio file:")
                    st.write(response)
                    with st.expander("Show complete transcript of the audio file"):
                        st.write(text)
            except Exception as e:
                st.error(f"Something went wrong. Please try again. Error: {e}")

if __name__ == "__main__":
    main()