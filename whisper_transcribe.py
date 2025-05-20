#!/usr/bin/env python3
"""
Whisper Interview Transcribe
---------------------------
Transcribes an audio interview to plain text, SRT, and VTT files using OpenAI Whisper.
Also outputs a cleaned Q&A version of the transcript for better readability.
"""
import whisper
import torch
import sys
import os
from clean_interview_text import clean_interview_transcript


def transcribe(audio_path, model_name="medium"):  # <-- Default is now "medium"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print(
            "\n[WARNING] No GPU detected! Transcription on CPU can be VERY slow, "
            "especially for medium or large models.\n"
            "If you have an NVIDIA GPU, make sure you have installed the correct CUDA version of PyTorch.\n"
        )
    print(f"Loading model '{model_name}' on device: {device}")
    model = whisper.load_model(model_name).to(device)
    print(f"Transcribing {audio_path} ...")
    result = model.transcribe(audio_path, verbose=True)

    base = os.path.splitext(audio_path)[0]

    # Save plain text
    txt_path = f"{base}_transcription.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Save cleaned Q&A version
    cleaned_txt_path = txt_path.replace(".txt", "_cleaned.txt")
    clean_interview_transcript(txt_path, cleaned_txt_path)

    # Save SRT (with timestamps)
    srt_path = f"{base}_transcription.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], 1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            def format_time(t):
                hours = int(t // 3600)
                minutes = int((t % 3600) // 60)
                seconds = int(t % 60)
                milliseconds = int((t - int(t)) * 1000)
                return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

            f.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")

    # Save VTT (with timestamps)
    vtt_path = f"{base}_transcription.vtt"
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            def format_time_vtt(t):
                hours = int(t // 3600)
                minutes = int((t % 3600) // 60)
                seconds = int(t % 60)
                milliseconds = int((t - int(t)) * 1000)
                return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

            f.write(f"{format_time_vtt(start)} --> {format_time_vtt(end)}\n{text}\n\n")

    print("\nTranscriptions saved as:")
    print(f"- {txt_path} (plain)")
    print(f"- {cleaned_txt_path} (cleaned Q&A)")
    print(f"- {srt_path} (with timestamps)")
    print(f"- {vtt_path} (with timestamps)")

    return result["text"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_interview.py <audiofile> [modelname]")
        sys.exit(1)
    audiofile = sys.argv[1]
    modelname = sys.argv[2] if len(sys.argv) > 2 else "medium"
    transcribe(audiofile, modelname)
