# ComfyUI-Monja-CharacterVoice (v1.0.2)

Custom Character Voice nodes for ComfyUI.

**Monja Character Voice** allows you to save and load reusable voice references for any character, making it easy to organize multiple voices and reference transcriptions for audio generation workflows.

---

## 🚀 Key Features

- **Dynamic Select Filtering (JS):** Choosing a character automatically updates the voice list to show only the voices belonging to that specific character. No more guesswork!
- **Recursive Folder Scanning:** The system automatically scans the character's folder and all its subfolders (like `Voz` or `Referencia`) to find your `.wav` files.
- **Persistent Storage:** Saves everything inside your user **Documents** folder for easy manual access and organization.
- **F5-TTS Optimized:** The output `voice_pack` is pre-configured with the correct tags (`samples`, `text`, `ref_text`) to work instantly with the F5-TTS Engine and `tts_audio_suite`.
- **Mono Conversion:** Automatically ensures reference audio is converted to Mono on load, preventing common cloning errors in AI models.

---

## 📦 Installation

1. Navigate to your ComfyUI `custom_nodes` folder.
2. Clone the repository:

   ```bash
   git clone https://github.com/andremonjardim/ComfyUI-Monja-CharacterVoice.git
   ```

3. Restart ComfyUI.

---

## 📂 Character Storage

By default, Monja Character Voice stores all characters inside the user's Documents folder:

```text
Documents/
└── MonjaCharacterVoice/
    └── characters/
        ├── Character_Name/
        │   ├── voice_01.wav
        │   ├── voice_01.txt
        │   └── [Optional Subfolders]/
```

Each character has its own folder. Files can be placed directly in the character's root folder or within subfolders — the recursive search will find them regardless.

### Custom Storage Location

If you prefer a different location, define the environment variable:

```text
MONJA_CHARACTER_PATH=D:\Your\Custom\Path
```

---

## 🛠️ Nodes

### Monja Character Voice • Save

Saves reference audio and its transcription.

- `audio`: Input for the reference audio waveform.  
- `character`: Name of the character (creates a folder).  
- `voice_name`: Filename for this specific voice identity.  
- `transcription`: The text spoken in the audio (essential for high-quality F5-TTS cloning).

### Monja Character Voice • Load

Loads the saved voice for use in workflows.

- `character`: Select the character from your library.  
- `voice_name`: Select the specific voice (filtered automatically via JavaScript).  

**Outputs:** Provides the ComfyUI `AUDIO` format, the `ref_text` string, and the `voice_pack` dictionary compatible with F5-TTS.

---

## 👤 Author

Andre Monjardim  

- GitHub: [andremonjardim](https://github.com/andremonjardim)  
- Repository: [ComfyUI-Monja-CharacterVoice](https://github.com/andremonjardim/ComfyUI-Monja-CharacterVoice)

---

## 📜 License

MIT License  

Copyright (c) 2026 Andre Monjardim  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.