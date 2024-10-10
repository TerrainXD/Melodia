from flask import Flask, render_template, jsonify
from predict import generate_music  # นำเข้าฟังก์ชัน generate_music จาก predict.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_music_flask():  # เปลี่ยนชื่อฟังก์ชันนี้เพื่อไม่ให้ชนกับฟังก์ชันใน predict.py
    print("Received request to generate music")
    try:
        # เรียกใช้ฟังก์ชัน generate_music จาก predict.py
        midi_file_path = generate_music()

        # ตรวจสอบว่ามีการสร้างไฟล์ MIDI หรือไม่
        print(f"Generated MIDI file path: {midi_file_path}")
        
        # ส่งลิงก์สำหรับดาวน์โหลดเพลงกลับไปยัง frontend
        return jsonify({"music_url": f"/static/generated_music.mid"})
    except Exception as e:
        print(f"Error during music generation: {e}")
        return jsonify({"error": "Error generating music."}), 500

if __name__ == '__main__':
    app.run(debug=True)
