import os
import gradio as gr
from inference.tts import SUPPORTED_VOICES, textToSpeech
from inference.podcast import textToSpeechPodcast

SUPPORTED_VOICE = SUPPORTED_VOICES

def clear_tts_speech():
    for file in ["./tmp/output.mp3", "./tmp/output_cloned.wav"]:
        if os.path.exists(file):
            os.remove(file)
    return None, None, None

def clear_podcast_speech():
    for file in ["./tmp/podcast_output.wav"]:
        if os.path.exists(file):
            os.remove(file)
    return None

def tts_interface():  
    with gr.Row():
        with gr.Column(scale=2):
            text = gr.TextArea(
                label="Text",
                placeholder="Enter your text here to convert to speech...",
                elem_classes="text-area",
                lines=10
            )
            
            with gr.Row():
                btn = gr.Button("🔊 Generate Speech", variant="primary", elem_id="submit-btn")
                clear = gr.Button("🗑️ Clear", variant="secondary", elem_id="clear-btn")
            
            audio = gr.Audio(label="Output Audio", interactive=False, elem_classes="audio")
            
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### Voice Selection")
                voices = gr.Dropdown(
                    choices=list(SUPPORTED_VOICES.keys()),
                    value="en-US-AriaNeural",
                    label="Voice",
                    info="Select a voice from the list",
                    interactive=True
                )
            
            with gr.Group():
                gr.Markdown("### Voice Adjustments")
                rate = gr.Slider(-100, 100, step=1, value=0, label="Speed", info="Adjust speech speed")
                volume = gr.Slider(-100, 100, step=1, value=0, label="Volume", info="Adjust volume")
                pitch = gr.Slider(-100, 100, step=1, value=0, label="Pitch", info="Adjust pitch")
            
            with gr.Group():
                gr.Markdown("### Voice Cloning")
                use_clone = gr.Checkbox(label="Enable Voice Clone", value=False)
                reference_speaker = gr.Audio(label="Upload Reference Audio", type="filepath", visible=True)
                model_version = gr.Dropdown(choices=["v2"], label="Model Version", value="v2", interactive=False, visible=False)
                
    btn.click(
        fn=textToSpeech,
        inputs=[text, voices, rate, volume, pitch, use_clone, reference_speaker, model_version],
        outputs=[audio]
    )
    clear.click(fn=clear_tts_speech, outputs=[text, audio, reference_speaker])

def podcast_interface():  
    with gr.Row():
        with gr.Column(scale=2):
            text = gr.TextArea(
                label="Podcast Script",
                placeholder="Format your script like this:\nSpeaker 1: Hello there!\nSpeaker 2: Hi, how are you?",
                elem_classes="text-area",
                lines=12
            )
            
            with gr.Row():
                btn = gr.Button("🎙️ Generate Podcast", variant="primary", elem_id="submit-btn")
                clear = gr.Button("🗑️ Clear", variant="secondary", elem_id="clear-btn")
            
            audio = gr.Audio(label="Podcast Output", interactive=False, elem_classes="audio")
            
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### Speaker Voices")
                voices1 = gr.Dropdown(
                    choices=list(SUPPORTED_VOICES.keys()),
                    value="en-US-AriaNeural",
                    label="Speaker 1",
                    info="Voice for first speaker",
                    interactive=True
                )
                voices2 = gr.Dropdown(
                    choices=list(SUPPORTED_VOICES.keys()),
                    value="en-US-EricNeural",
                    label="Speaker 2",
                    info="Voice for second speaker",
                    interactive=True
                )
            
            with gr.Group():
                gr.Markdown("### Voice Adjustments")
                rate = gr.Slider(-100, 100, step=1, value=0, label="Speed", info="Adjust speech speed")
                volume = gr.Slider(-100, 100, step=1, value=0, label="Volume", info="Adjust volume")
                pitch = gr.Slider(-100, 100, step=1, value=0, label="Pitch", info="Adjust pitch")
            
            with gr.Group():
                gr.Markdown("### Voice Cloning")
                use_clone = gr.Checkbox(label="Enable Voice Cloning", value=False)
                ref_speaker1 = gr.Audio(label="Speaker 1 Reference Audio", type="filepath", visible=True)
                ref_speaker2 = gr.Audio(label="Speaker 2 Reference Audio", type="filepath", visible=True)
                model_version = gr.Dropdown(choices=["v2"], label="Model Version", value="v2", interactive=False, visible=False)
            
    btn.click(
        fn=textToSpeechPodcast,
        inputs=[text, voices1, voices2, rate, volume, pitch, use_clone, ref_speaker1, ref_speaker2, model_version],
        outputs=[audio]
    )
    clear.click(fn=clear_podcast_speech, outputs=[audio])

with gr.Blocks(
    title="EdgeTTS-Studio",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown("""
    # 🎧 EdgeTTS-Studio
    ### Convert text to natural-sounding speech using edge-tts with optional voice cloning
    """)
    
    with gr.Tabs(selected=0):
        with gr.Tab("✨ Text to Speech"):
            tts_interface()
        with gr.Tab("🎙️ Podcast Generator"):
            podcast_interface()

if __name__ == "__main__":
    demo.launch()