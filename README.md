# Audio2Summary

Upload one or more audio files and get a bullet-point summary of what was said,
in English or Spanish, plus the full transcript.

## How it works
- Accepts `mp3`, `wav`, and `ogg` files. Multiple files are merged into one
  recording with `pydub` (useful for voice notes split in parts).
- Transcribes the audio with OpenAI's Whisper API.
- Summarizes the transcript with `gpt-4o-mini`.

You use your own OpenAI API key, entered in the sidebar.

## Run locally
Requires `ffmpeg`.
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Stack
Python · Streamlit · pydub · OpenAI API (`whisper-1`, `gpt-4o-mini`)

Built in August 2023; updated in October 2024.
