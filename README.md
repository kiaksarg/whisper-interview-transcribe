# whisper-interview-transcribe

**Transcribe and structure interview audio using OpenAI Whisper, with Q\&A formatting for improved qualitative analysis.**

---

## Overview

* Transcribe interviews and qualitative sessions from audio files using [OpenAI Whisper](https://github.com/openai/whisper)
* Automatically generate:

  * **Plain text**
  * **Cleaned Q\&A text** (grouping questions and answers with extra readability)
  * **Subtitle files** (`.srt` and `.vtt` with timestamps)

**Recommended default model:**
This project defaults to Whisper’s `medium` model for the best balance of speed and accuracy, but you may specify any supported model (`base`, `small`, `medium`, `large`, etc.).

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/whisper-interview-transcribe.git
cd whisper-interview-transcribe
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv whisper-env
# On Windows:
whisper-env\Scripts\activate
# On Mac/Linux:
source whisper-env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:**
> For GPU acceleration, install PyTorch matching your CUDA version.
> See [PyTorch official instructions](https://pytorch.org/get-started/locally/) if you need a different setup.
>
> **Note on GPU Support:**
> PyTorch runs on CPU by default, and is optimized for NVIDIA GPUs (CUDA). Not all GPUs or hardware platforms are supported. If no compatible GPU is found, the script will run on CPU, which can be much slower.
---

## Usage

### **Transcribe and clean an interview in one command**

```bash
python transcribe_interview.py <audiofile> [modelname]
```

* By default, the `medium` model is used.
* Example:

  ```bash
  python transcribe_interview.py myinterview.m4a
  ```
* To use a different model (e.g., `large`):

  ```bash
  python transcribe_interview.py myinterview.m4a large
  ```

### **Output files**

All files are saved next to your audio with the same base name:

* `<basename>_transcription.txt` — Whisper’s plain transcription
* `<basename>_transcription_cleaned.txt` — Cleaned, Q\&A-formatted version
* `<basename>_transcription.srt` — Subtitle (SRT) with timestamps
* `<basename>_transcription.vtt` — Subtitle (VTT) with timestamps
