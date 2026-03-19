# QUICK GUIDE — Creating Subtitles (.srt) for Voiceover Videos (for Papers)

## 1. Generate Subtitles with an LLM

You can use an LLM such as **ChatGPT**, **Gemini**, or similar tools.

- Upload the video you want to subtitle.
- Use the following prompt:

```text
Please create subtitles in .srt format with accurate timestamps for the attached video.

Requirements:
- Output must be valid .srt.
- Timestamps must follow exactly: HH:MM:SS,mmm --> HH:MM:SS,mmm
- Provide sequential numeric indexes starting from 1.
- Keep ONLY 1 sentence per subtitle entry (one caption = one sentence).
- Double-check timestamps are in chronological order and do not overlap.
- Keep captions readable (avoid very long lines).
- Return ONLY the .srt content (no extra commentary).

.srt example:

1
00:00:00,392 --> 00:00:03,842
Have you ever tried to upload a lot of information to ChatGPT or any AI?

2
00:00:04,182 --> 00:00:05,232
Obviously you can't.
```

## 2. Save the Output as an `.srt` File

- Create a file named, for example, **`subtitles.srt`**.
- Paste the generated content and save it.
- If you only have a **`.txt`** file, convert it to **`.srt`** using an online converter.

## 3. Check and Fix Subtitles with an Online Editor

- Upload the video and the **`.srt`** file to verify synchronization and formatting.
- Recommended tool: **Happy Scribe – Online Subtitle Editor**.

Typical issues to fix:

- typos and punctuation
- timestamps out of order or overlapping
- captions that are too long
- missing or incorrect subtitle numbering

## 4. Add Subtitles to the Video

There are three common options.

### 4.1 FFmpeg (embed soft subtitles into the MP4)

Install **FFmpeg**:

- **Windows (winget)**

```bash
winget install "FFmpeg (Essentials Build)"
```

- **Ubuntu / Debian**

```bash
sudo apt update
sudo apt install ffmpeg
```

- **macOS (Homebrew)**

```bash
brew install ffmpeg
```

In the folder containing **`input_video.mp4`** and **`subtitles.srt`**, run:

```bash
ffmpeg -i input_video.mp4 -i subtitles.srt -c copy -c:s mov_text output_video.mp4
```

**Result:**

- **`output_video.mp4`** will include selectable subtitles that can be turned on or off.

### 4.2 VLC (use subtitles as an external file)

- Keep the **`.srt`** file in the same folder as the video.
- Load it in **VLC** as an external subtitle track.

### 4.3 Video Editor (import the `.srt` directly)

- Import the **`.srt`** into your editing software (for example, **DaVinci Resolve**).
- Verify the timing.
- Export the video with subtitles embedded or as a subtitle track.
