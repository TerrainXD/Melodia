from midi2audio import FluidSynth
from pydub import AudioSegment
import os

def midi_to_mp3(midi_file_path, mp3_file_path):
    # กำหนด SoundFont
    sound_font = 'C:\\Users\\aomna\\OneDrive\\Documents\\Year3Sem1\\AI\\melodia\\backend\\soundfont\\SalC5Light2.sf2'
    fs = FluidSynth(sound_font=sound_font)

    # แปลง MIDI เป็น WAV
    wav_file_path = midi_file_path.replace('.mid', '.wav')
    fs.midi_to_audio(midi_file_path, wav_file_path)

    # แปลง WAV เป็น MP3
    sound = AudioSegment.from_wav(wav_file_path)
    sound.export(mp3_file_path, format="mp3", bitrate="128k")

    # ลบไฟล์ WAV หลังจากแปลงเสร็จแล้ว
    os.remove(wav_file_path)

    return mp3_file_path
