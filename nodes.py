import os
import ctypes
from pathlib import Path
import torchaudio
import torch

# ============================================================
# ComfyUI-Monja-CharacterVoice
# Author: Andre Monjardim
# Repository: https://github.com/andremonjardim/ComfyUI-Monja-CharacterVoice
#
# Copyright (c) 2026 Andre Monjardim
# Licensed under the MIT License.
# See the LICENSE file for details.
# SPDX-License-Identifier: MIT
# ============================================================

__author__ = "Andre Monjardim"
__version__ = "1.0.2"


def get_documents_folder():
    """
    Retorna a pasta 'Documentos' do usuário utilizando a API do Windows.
    Caso não seja possível obter o caminho, usa a pasta Home.
    """
    try:
        CSIDL_PERSONAL = 5
        SHGFP_TYPE_CURRENT = 0

        buf = ctypes.create_unicode_buffer(260)

        ctypes.windll.shell32.SHGetFolderPathW(
            None,
            CSIDL_PERSONAL,
            None,
            SHGFP_TYPE_CURRENT,
            buf
        )

        return Path(buf.value)

    except Exception:
        return Path.home()


BASE_PATH = os.getenv(
    "MONJA_CHARACTER_PATH",
    str(get_documents_folder() / "MonjaCharacterVoice" / "personagens")
)


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


def list_characters():
    characters = ["Nenhum"]

    if os.path.exists(BASE_PATH):
        found = [
            d for d in os.listdir(BASE_PATH)
            if os.path.isdir(os.path.join(BASE_PATH, d))
        ]
        if found:
            characters = sorted(found)

    return characters


def list_voice_names(character=None):
    voices = []

    if character and character != "Nenhum":
        ref_path = os.path.join(BASE_PATH, character, "Voz", "Referencia")

        if os.path.exists(ref_path):
            for name in os.listdir(ref_path):
                full = os.path.join(ref_path, name)

                if os.path.isfile(full) and name.lower().endswith(".wav"):
                    voices.append(os.path.splitext(name)[0])

    if not voices:
        voices = ["Principal"]

    return sorted(set(voices))


class SaveCharacterVoice:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "character": ("STRING", {"default": ""}),
                "voice_name": ("STRING", {"default": "Principal"}),
                "transcription": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "run"
    CATEGORY = "Monja/Character Voice"

    def run(self, audio, character, voice_name, transcription):
        character = character.strip()
        voice_name = voice_name.strip()

        if not character:
            raise ValueError("Please enter a character name.")

        if not voice_name:
            voice_name = "Principal"

        voice_folder = os.path.join(
            BASE_PATH,
            character,
            "Voz",
            "Referencia"
        )

        os.makedirs(voice_folder, exist_ok=True)

        wav_path = os.path.join(voice_folder, f"{voice_name}.wav")
        txt_path = os.path.join(voice_folder, f"{voice_name}.txt")

        if (
            not isinstance(audio, dict)
            or "waveform" not in audio
            or "sample_rate" not in audio
        ):
            raise ValueError(
                "Invalid audio input. Expected ComfyUI AUDIO type."
            )

        waveform = audio["waveform"]
        sample_rate = int(audio["sample_rate"])

        if waveform.dim() == 3:
            waveform = waveform.squeeze(0)

        if waveform.dim() != 2:
            raise ValueError(
                f"Unexpected waveform shape: {tuple(waveform.shape)}"
            )

        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        torchaudio.save(
            wav_path,
            waveform.cpu(),
            sample_rate
        )

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write((transcription or "").strip())

        print(f"[Monja Character Voice] Voice saved: {wav_path}")
        return (audio,)


class LoadCharacterVoice:

    @classmethod
    def INPUT_TYPES(cls):
        characters = list_characters()
        default_character = next(
            (c for c in characters if c != "Nenhum"),
            "Nenhum"
        )

        voice_names = list_voice_names(default_character)

        return {
            "required": {
                "character": (characters,),
                "voice_name": (voice_names,),
            }
        }

    RETURN_TYPES = ("AUDIO", "STRING", any_typ)
    RETURN_NAMES = ("audio", "ref_text", "voice_pack")
    FUNCTION = "load"
    CATEGORY = "Monja/Character Voice"

    def load(self, character, voice_name):
        if character == "Nenhum":
            raise ValueError(
                "No character found. Please save a voice first."
            )

        ref_path = os.path.join(
            BASE_PATH,
            character,
            "Voz",
            "Referencia"
        )

        wav_path = os.path.join(ref_path, f"{voice_name}.wav")
        txt_path = os.path.join(ref_path, f"{voice_name}.txt")

        if not os.path.exists(wav_path):
            raise FileNotFoundError(
                f"Voice file not found: {wav_path}"
            )

        waveform, sample_rate = torchaudio.load(wav_path)

        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        audio_dict = {
            "waveform": waveform.unsqueeze(0),
            "sample_rate": int(sample_rate),
        }

        ref_text = ""

        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                ref_text = f.read().strip()

        voice_pack = {
            "audio": audio_dict,
            "audio_path": wav_path,
            "reference_text": ref_text,
            "character_name": character,
        }

        print(f"[Monja Character Voice] Character '{character}' loaded.")

        return (
            audio_dict,
            ref_text,
            voice_pack,
        )


NODE_CLASS_MAPPINGS = {
    "SaveCharacterVoice": SaveCharacterVoice,
    "LoadCharacterVoice": LoadCharacterVoice,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveCharacterVoice": "Monja Character Voice • Save",
    "LoadCharacterVoice": "Monja Character Voice • Load",
}