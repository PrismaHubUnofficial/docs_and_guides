# QUICK GUIDE — Voiceover for a Video with Text-to-Speech (TTS)

## 1. Prepare the Script

- Write the narration.
- Add punctuation to control pauses.
- If the script is long, split it into short chunks (approximately **15–60 s** each).

Optional: make it **TTS-ready** with an AI **without changing any words**.

**Prompt:**

```text
Please prepare this script for text-to-speech.
Rules:
- Do NOT change, add, or remove any words.
- Only adjust punctuation, capitalization, spacing, and line breaks.
- Add line breaks/extra punctuation to improve pauses.
Output ONLY the cleaned script.
```

## 2. Generate the Voiceover

Choose one of the following methods.

### A. Hugging Face TTS

Recommended model: **Kokoro**

- Open the Hugging Face models page for text-to-speech.
- Select a model.
- Recommended space: **Kokoro-TTS**.
- Paste one chunk of text.
- Pick a voice.
- Generate and preview the result.
- If the output sounds wrong:
  - add punctuation
  - split the chunk further
  - regenerate
- Download the audio (**MP3** or **WAV**, depending on the tool).

### B. Microsoft Clipchamp (Text-to-Speech)

- Open a project.
- Import the video and place it on the timeline.
- Go to **Record & create → Text to speech**.
- Choose language and voice.
- Adjust pace and pitch if available.
- Paste one chunk.
- Preview the result.
- Save it or add it to the timeline.
- Export the voiceover as **audio-only (MP3)**.
