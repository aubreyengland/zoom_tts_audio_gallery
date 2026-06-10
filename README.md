# Zoom TTS Voice Gallery

An interactive audio gallery for previewing Text-to-Speech voices available in **Zoom**. Built by [CDW](https://cdw.com) This is as a resource for customers to explore the wide variety of TTS voices offered in Zoom's accessibility features.

**Live gallery:** `https://aubreyengland.github.io/zoom_tts_audio_gallery/` *(or your GitHub Pages URL)*

---

## Authors
- [Aubrey England](https://github.com/aubreyengland)(
    [aubrey.england@cdw.com](mailto:aubrey.england@cdw.com))
)
    
## What it does

- Browse TTS voices by language (40+ languages)
- Click any voice to hear a sample in that language
- Voices labeled by type: Male, Female, Male · Child, Female · Child
- Now Playing bar with stop control
- Audio samples generated via AWS Polly (neural + standard engines)

---

## Repository structure

```
zoom_tts_audio_gallery/
├── index.html          # The gallery — single-file app
├── main.py             # AWS Polly script to generate audio files
├── zoom-logo.png       # Zoom logo
├── cdw-logo.png        # CDW logo
└── audios/
    ├── en-us/
    │   ├── matthew.mp3
    │   ├── danielle.mp3
    │   └── ...
    ├── fr/
    │   └── lea.mp3
    └── ...             # One folder per language key
```

---

## Adding or updating voices

### 1. Add audio files

Run `main.py` to generate MP3s via AWS Polly (see below), then commit the new files under `audios/{language-key}/`.

### 2. Update the gallery

Edit the `LANGUAGES` array in `index.html` to add the voice entry:

```js
{ label: "English (United States)", key: "en-us", voices: [
    { name: "Matthew", type: "male" },
    // add new entry here:
    { name: "NewVoice", type: "female" },
]}
```

Voice types: `"male"` · `"female"` · `"male-child"` · `"female-child"`

Audio is resolved automatically as `audios/{key}/{name.toLowerCase()}.mp3`.

---

## Generating audio files (AWS Polly)

### Prerequisites

```bash
pip install boto3
# or: uv sync
```

### AWS credentials

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### Run

```bash
python main.py
```

Outputs MP3s to `audios/` organized by language folder. Commit and push the new files — the gallery loads audio directly from GitHub raw content.

---

## Deploying

The gallery is a static HTML file with no build step. Enable **GitHub Pages** on the `main` branch (root) and it's live. Audio loads from:

```
https://raw.githubusercontent.com/aubreyengland/zoom_tts_audio_gallery/main/audios/{lang}/{voice}.mp3
```

---

## Built with

- [AWS Polly](https://aws.amazon.com/polly/) — TTS synthesis (neural + standard engines)
- Vanilla HTML/CSS/JS — no framework or build tooling
- GitHub Pages + raw.githubusercontent.com for static hosting
