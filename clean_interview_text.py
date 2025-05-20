#!/usr/bin/env python3
"""
Interview Transcript Cleaner
---------------------------
Improves readability of transcribed interviews by formatting Q&A blocks.
"""
import sys
import re
import os


def split_into_sentences(text):
    """Splits text into sentences based on . ? ! followed by capital."""
    sentence_endings = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
    return sentence_endings.split(text)


def clean_interview_transcript(input_file, output_file=None):
    """
    Reads a plain transcript and outputs a more readable Q&A version.
    Groups questions and their answers, adds empty lines between blocks.
    If output_file is None, saves to input_file.replace('.txt', '_cleaned.txt')
    """
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = split_into_sentences(text)
    output_lines = []
    group = []

    def flush_group():
        if group:
            output_lines.extend(group)
            output_lines.append("")  # One blank line after group

    i = 0
    n = len(sentences)
    while i < n:
        group = []
        # Collect consecutive questions
        while i < n and sentences[i].strip().endswith("?"):
            group.append(sentences[i].strip())
            i += 1
        # Collect consecutive answers (not questions), as a block
        while i < n and not sentences[i].strip().endswith("?") and sentences[i].strip():
            group.append(sentences[i].strip())
            i += 1
        flush_group()
        # skip any accidental extra blank sentences
        while i < n and not sentences[i].strip():
            i += 1

    # Remove extra blank lines at the end
    while len(output_lines) > 1 and output_lines[-1] == "":
        output_lines.pop()

    if output_file is None:
        output_file = input_file.replace(".txt", "_cleaned.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"✔️ Saved cleaned transcript to {output_file}")
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_interview_text.py input.txt [output.txt]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    clean_interview_transcript(input_file, output_file)
