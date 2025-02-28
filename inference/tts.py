import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
import edge_tts
#import asyncio
from inference.edge_tts_utils import load_edge_tts_shortnames

SUPPORTED_VOICES = {voice: voice for voice in load_edge_tts_shortnames("./inference/edge-tts-list/edge-tts-list.txt")}

def voice_cloning(base_audio, reference_speaker, model_version="v2"):
    try:
        ckpt_converter = f'./OPENVOICE_MODELS/{model_version}'
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        source_se, _ = se_extractor.get_se(base_audio, tone_color_converter, vad=True)
        target_se, _ = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)
        
        output_path = "./tmp/output_cloned.wav"
        tone_color_converter.convert(
            audio_src_path=base_audio, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=output_path,
        )
        return output_path
    except Exception as e:
        raise (f"Cloning failed: {str(e)}")

async def textToSpeech(text, voices, rate, volume, pitch, use_clone, reference_speaker, model_version):
    try:
        output_file = "./tmp/output_tts.mp3"
        voices = SUPPORTED_VOICES[voices]
        rates = f"+{rate}%" if rate >= 0 else f"{rate}%"
        volumes = f"+{volume}%" if volume >= 0 else f"{volume}%"
        pitchs = f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"

        communicate = edge_tts.Communicate(text,
                                         voices,
                                         rate=rates,
                                         volume=volumes,
                                         pitch=pitchs)
        await communicate.save(output_file)
        
        if use_clone and reference_speaker:
            if not os.path.exists(reference_speaker):
                raise ("Reference audio file does not exist")
            output_file = voice_cloning(output_file, reference_speaker, model_version)
        
        return output_file
    except Exception as e:
        raise (f"Conversion failed: {str(e)}")
    