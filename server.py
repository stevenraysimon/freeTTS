import os
import io
from flask import Flask, request, render_template, send_file, Response
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

app = Flask(__name__)

# Download and load all models
preload_models()

# Define available voices
VOICES = {
    "v1": {"name": "Aditya", "preset": "v2/en_speaker_1"},
    "v2": {"name": "Andrew", "preset": "v2/en_speaker_2"},
    "v3": {"name": "Johnston", "preset": "v2/en_speaker_3"},
    "v4": {"name": "Brad", "preset": "v2/en_speaker_4"},
    "v5": {"name": "Mark", "preset": "v2/en_speaker_5"},
    "v6": {"name": "Brian", "preset": "v2/en_speaker_6"},
    "v7": {"name": "Marcus", "preset": "v2/en_speaker_7"},
    "v8": {"name": "Jackson", "preset": "v2/en_speaker_8"},
    "v9": {"name": "Amanda", "preset": "v2/en_speaker_9"}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        selected_voice = request.form['voice']
        filename = request.form['filename']
        
        voice_preset = VOICES[selected_voice]['preset']
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        # Create an in-memory file-like object
        mem_file = io.BytesIO()
        write_wav(mem_file, SAMPLE_RATE, audio_array)
        mem_file.seek(0)
        
        return send_file(
            mem_file,
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f"{filename}.wav"
        )
    
    return render_template('index.html', voices=VOICES)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))