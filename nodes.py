import os
import ctypes
from pathlib import Path
import torchaudio
import torch
import shutil

# ============================================================
# ComfyUI-Monja-CharacterVoice
# Corrigido para compatibilidade total com F5-TTS e tts_audio_suite
# ============================================================

def get_documents_folder():
    try:
        CSIDL_PERSONAL = 5
        SHGFP_TYPE_CURRENT = 0
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return Path(buf.value)
    except Exception:
        return Path.home()

# Forçamos o caminho que você definiu como sua biblioteca
BASE_PATH = r"C:\ComfyUI_Arquivos\personagens"
os.makedirs(BASE_PATH, exist_ok=True)

def list_characters():
    characters = ["Nenhum"]
    if os.path.exists(BASE_PATH):
        found = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
        if found: characters = sorted(found)
    return characters

def list_voice_names(character=None):
    voices = []
    if character and character != "Nenhum":
        # Procuramos na subpasta 'Voz/Referencia' que é onde o Save guarda
        ref_path = os.path.join(BASE_PATH, character, "Voz", "Referencia")
        if os.path.exists(ref_path):
            for name in os.listdir(ref_path):
                if name.lower().endswith(".wav"):
                    voices.append(os.path.splitext(name)[0])
    if not voices: voices = ["Principal"]
    return sorted(set(voices))

class SaveCharacterVoice:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "character": ("STRING", {"default": "Yasmin"}),
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
        if not character: raise ValueError("Enter a character name.")
        
        # Salva na estrutura organizada: Personagem > Voz > Referencia
        voice_folder = os.path.join(BASE_PATH, character, "Voz", "Referencia")
        os.makedirs(voice_folder, exist_ok=True)

        wav_path = os.path.join(voice_folder, f"{voice_name}.wav")
        txt_path = os.path.join(voice_folder, f"{voice_name}.txt")

        waveform = audio["waveform"]
        sample_rate = int(audio["sample_rate"])
        if waveform.dim() == 3: waveform = waveform.squeeze(0)
        
        # O F5-TTS exige Mono. Convertemos aqui para evitar erro.
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        torchaudio.save(wav_path, waveform.cpu(), sample_rate)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write((transcription or "").strip())

        print(f"✅ [Monja Save] Salvo em: {wav_path}")
        return (audio,)

class LoadCharacterVoice:
    @classmethod
    def INPUT_TYPES(cls):
        characters = list_characters()
        # Nota: O ComfyUI não atualiza o segundo dropdown dinamicamente sem JS customizado,
        # mas ele lerá todas as vozes disponíveis no BASE_PATH no arranque.
        all_voices = []
        for char in characters:
            all_voices.extend(list_voice_names(char))
        
        return {
            "required": {
                "character": (characters,),
                "voice_name": (sorted(list(set(all_voices))) if all_voices else ["Principal"],),
            }
        }

    RETURN_TYPES = ("AUDIO", "STRING", "VOICE")
    RETURN_NAMES = ("audio", "ref_text", "voice_pack")
    FUNCTION = "load"
    CATEGORY = "Monja/Character Voice"

    def load(self, character, voice_name):
        # Caminho corrigido para a sua estrutura de pastas
        ref_path = os.path.join(BASE_PATH, character, "Voz", "Referencia")
        wav_path = os.path.join(ref_path, f"{voice_name}.wav")
        txt_path = os.path.join(ref_path, f"{voice_name}.txt")

        if not os.path.exists(wav_path):
            print(f"❌ [Monja Load] Não encontrado: {wav_path}")
            return (None, "", None)

        waveform, sample_rate = torchaudio.load(wav_path)
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        audio_dict = {"waveform": waveform.unsqueeze(0), "sample_rate": int(sample_rate)}
        
        ref_text = ""
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                ref_text = f.read().strip()

        # AQUI ESTÁ A CORREÇÃO PARA O F5-TTS (Etiquetas text e samples)
        voice_pack = {
            "samples": waveform,         # O que o motor F5 realmente lê
            "sample_rate": sample_rate,
            "text": ref_text,            # O que o erro reclamava que faltava
            "ref_text": ref_text,        # Backup
            "audio": audio_dict          # Padrão ComfyUI
        }

        print(f"✅ [Monja Load] '{character}' carregado com sucesso.")
        return (audio_dict, ref_text, voice_pack)

NODE_CLASS_MAPPINGS = {"SaveCharacterVoice": SaveCharacterVoice, "LoadCharacterVoice": LoadCharacterVoice}
NODE_DISPLAY_NAME_MAPPINGS = {"SaveCharacterVoice": "Monja Character Voice • Save", "LoadCharacterVoice": "Monja Character Voice • Load"}