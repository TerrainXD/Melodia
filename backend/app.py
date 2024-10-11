from flask import Flask, render_template, jsonify, request
from predict import generate_music  # นำเข้าฟังก์ชัน generate_music จาก predict.py
from converttomp3 import midi_to_mp3  # นำเข้าฟังก์ชันแปลง MIDI เป็น MP3
import os

app = Flask(__name__, template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/custom')
def custom():
    return render_template('Custom.html')  

@app.route('/listen')
def listen():
    return render_template('listen.html')

@app.route('/thank-you')
def thank_you():
    return render_template('ThankYou.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    num_notes = int(data.get('numNotes', 500))  # Default to 500 notes if not provided
    instrument_name = data.get('instrument', 'Piano')  # Default to Piano if not provided

    try:
        midi_file_path = generate_music(num_notes, instrument_name)  # Pass instrument to the function
        if midi_file_path and os.path.exists(midi_file_path):
            mp3_file_path = midi_to_mp3(midi_file_path, midi_file_path.replace('.mid', '.mp3'))
            return jsonify({'mp3_url': '/static/generated_music.mp3'})
        else:
            return jsonify({'error': 'MIDI file path is None or file does not exist.'}), 500
    except Exception as e:
        print(f"Error during music generation: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)