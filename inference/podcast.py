import os
import torch
import edge_tts
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from inference.edge_tts_utils import load_edge_tts_shortnames
import pydub
import random

SUPPORTED_VOICES = {voice: voice for voice in load_edge_tts_shortnames("./inference/edge-tts-list/edge-tts-list.txt")}

def voice_cloning(base_audio, reference_speaker, model_version="v2"):
    try:
        ckpt_converter = f'./OPENVOICE_MODELS/{model_version}'
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        source_se, _ = se_extractor.get_se(base_audio, tone_color_converter, vad=True)
        target_se, _ = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)
        
        output_path = base_audio.replace(".mp3", "_cloned.wav")
        tone_color_converter.convert(
            audio_src_path=base_audio, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=output_path,
        )
        return output_path
    except Exception as e:
        raise (f"Cloning failed: {str(e)}")
    
async def textToSpeechPodcast(text, voices1, voices2, rate, volume, pitch, use_clone, ref_speaker1, ref_speaker2, model_version):
    try:
        lines = text.strip().split("\n")
        output_files = []
        
        for i, line in enumerate(lines):
            if "Speaker 1:" in line:
                voice = voices1
                ref_audio = ref_speaker1
            elif "Speaker 2:" in line:
                voice = voices2
                ref_audio = ref_speaker2
            else:
                continue
            
            spoken_text = line.split(":", 1)[1].strip()
            output_file = f"./tmp/temp_{i}.mp3"
            rates = f"+{rate}%" if rate >= 0 else f"{rate}%"
            volumes = f"+{volume}%" if volume >= 0 else f"{volume}%"
            pitchs = f"+{pitch}Hz" if pitch >= 0 else f"{pitch}Hz"
            
            communicate = edge_tts.Communicate(spoken_text, voice, rate=rates, volume=volumes, pitch=pitchs)
            await communicate.save(output_file)
            
            if use_clone and ref_audio:
                if not os.path.exists(ref_audio):
                    raise ("Reference audio file does not exist")
                output_file = voice_cloning(output_file, ref_audio, model_version)
                
            output_files.append(output_file)
        
        final_output = "tmp/podcast_output.wav"
        
        # Merge audio files using pydub instead of ffmpeg
        combined = pydub.AudioSegment.empty()
        for file in output_files:
            segment = pydub.AudioSegment.from_file(file)
            # Remove random airtime between 0.1 and 0.8 seconds
            airtime_to_remove = random.uniform(0.1, 0.8) * 1000  # Convert to milliseconds
            segment = segment[:len(segment) - airtime_to_remove]
            combined += segment
        
        combined.export(final_output, format="wav")
        
        for file in output_files:
            os.remove(file)
        
        return final_output
    except Exception as e:
        raise (f"Podcast conversion failed: {str(e)}")