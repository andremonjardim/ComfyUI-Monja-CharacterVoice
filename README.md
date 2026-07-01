# ComfyUI-Monja-CharacterVoice

Custom Character Voice nodes for ComfyUI.

Monja Character Voice allows you to save and load reusable voice references for any character, making it easy to organize multiple voices and reference transcriptions for audio generation workflows.

---

## Features

- Save character voice references
- Load character voice references
- Store multiple voice references per character
- Automatic character folder creation
- Automatic storage inside the user's Documents folder
- Save reference transcription
- Load reference transcription
- Compatible with ComfyUI audio workflows
- Custom storage location through the `MONJA_CHARACTER_PATH` environment variable

---

## Installation

Clone this repository into:

```text
ComfyUI/
└── custom_nodes/
    └── ComfyUI-Monja-CharacterVoice/
```

or

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/andremonjardim/ComfyUI-Monja-CharacterVoice.git
```

Restart ComfyUI after installation.

---

## Requirements

```text
torch
torchaudio
```

---

## Character Storage

By default, Monja Character Voice stores all characters inside the user's Documents folder.

```text
Documents/
└── MonjaCharacterVoice/
    └── personagens/
```

Each character has its own folder:

```text
Documents/
└── MonjaCharacterVoice/
    └── personagens/
        ├── Character1/
        │   └── Voz/
        │       └── Referencia/
        │           ├── Principal.wav
        │           └── Principal.txt
        │
        └── Character2/
            └── Voz/
                └── Referencia/
                    ├── Voice01.wav
                    └── Voice01.txt
```

The folders are created automatically when the first voice is saved.

---

## Custom Storage Location

If you prefer another location, define the environment variable:

```text
MONJA_CHARACTER_PATH
```

Example:

```text
MONJA_CHARACTER_PATH=D:\AI\Characters
```

Monja Character Voice will use this folder instead of the default Documents location.

---

## Nodes

### Monja Character Voice • Save

Saves:

- WAV reference audio
- Reference transcription (.txt)

Automatically creates the character folder if it does not exist.

---

### Monja Character Voice • Load

Loads:

- Reference audio
- Reference transcription
- Voice Pack

The available characters and voices are detected automatically from the storage folder.

---

## Category

```text
Monja/Character Voice
```

---

## Repository

https://github.com/andremonjardim/ComfyUI-Monja-CharacterVoice

---

## Author

Andre Monjardim

GitHub:

https://github.com/andremonjardim

---

## License

MIT License

Copyright (c) 2026 Andre Monjardim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.