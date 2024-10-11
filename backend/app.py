from flask import Flask, render_template, jsonify
from predict import generate_music  # นำเข้าฟังก์ชัน generate_music จาก predict.py
from converttomp3 import midi_to_mp3  # นำเข้าฟังก์ชันแปลง MIDI เป็น MP3
import os


app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_music_flask():
    try:
        midi_file_path = generate_music()
        if midi_file_path:
            mp3_file_path = midi_file_path.replace('.mid', '.mp3')
            mp3_file_path = midi_to_mp3(midi_file_path, mp3_file_path)
            print(f"Sending MP3 URL: /static/{os.path.basename(mp3_file_path)}")  # เพิ่มการพิมพ์ลิงก์ MP3
            return jsonify({"mp3_url": f"/static/{os.path.basename(mp3_file_path)}"})
        else:
            raise ValueError("MIDI file path is None. Could not generate MP3.")
    except Exception as e:
        print(f"Error during music generation: {e}")
        return jsonify({"error": "Error generating music."}), 500

if __name__ == '__main__':
    app.run(debug=True)
