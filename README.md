\# ComfyUI-Monja-CharacterVoice



Custom Character Voice nodes for ComfyUI.



\## Features



\- Save Character Voice

\- Load Character Voice

\- Store multiple voice references per character

\- Save reference transcription

\- Load voice reference and transcription

\- Compatible with ComfyUI audio workflows



\---



\## Installation



Clone this repository into:



```text

ComfyUI/custom\_nodes/

```



Example:



```text

ComfyUI/

└── custom\_nodes/

&#x20;   └── ComfyUI-Monja-CharacterVoice/

```



Restart ComfyUI after installation.



\---



\## Requirements



```

torch

torchaudio

```



\---



\## Character Folder Structure



```text

C:\\ComfyUI\_Arquivos\\personagens



├── Yasmin

│   └── Voz

│       └── Referencia

│           ├── Principal.wav

│           └── Principal.txt

│

├── Character2

│   └── Voz

│       └── Referencia

│           ├── Voice01.wav

│           └── Voice01.txt

```



\---



\## Nodes



\### Monja - Save Character Voice



Saves:



\- WAV reference audio

\- Reference transcription (.txt)



\---



\### Monja - Load Character Voice



Loads:



\- Reference audio

\- Reference transcription

\- Voice Pack



\---



\## Category



```

Monja/Character Voice

```



\---



\## Author



Andre Monjardim



GitHub



https://github.com/andremonjardim



\---



\## License



MIT License

