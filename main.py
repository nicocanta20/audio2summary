import streamlit as st
from openai import OpenAI
from pydub import AudioSegment
import io

def process_file(file):
    byte_io = io.BytesIO(file.read())
    format_type = file.type.split("/")[1]  # Extracted format here
    format_handlers = {
        "ogg": AudioSegment.from_ogg,
        "wav": AudioSegment.from_wav,
        "mp3": AudioSegment.from_mp3,
        "mpeg": AudioSegment.from_mp3,
    }
    
    if format_type in format_handlers:
        sound = format_handlers[format_type](byte_io)
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

def audio2text(client, audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

def summary(client, text, language):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarize the following conversation into bullet points."},
            {"role": "user", "content": "respond everything in " + language},
            {"role": "user", "content": text},
        ])
    return response.choices[0].message.content

def warning_api_key(openai_api_key):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

def main():
    st.title("Audio2Summary")
    st.write("### Powered by OpenAI's [Whisper](https://platform.openai.com/docs/guides/speech-to-text) and [GPT4o-mini](https://platform.openai.com/docs/guides/gpt)")
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

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
                client = OpenAI(api_key=openai_api_key)

                with open(combined_audio_path, "rb") as f:
                    text = audio2text(client, f)

                response = summary(client, text, language)
                
                if response:
                    st.subheader("Summary of the audio file:")
                    st.write(response)
                    with st.expander("Show complete transcript of the audio file"):
                        st.write(text)
            except Exception as e:
                st.error(f"Something went wrong. Please try again. Error: {e}")

if __name__ == "__main__":
    main()