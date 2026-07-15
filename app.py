from flask import Flask, render_template, request, send_file
import subprocess
import os
import time

app = Flask(__name__)

# Kerakli papkalarni yaratish
os.makedirs('outputs', exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    kuyov = request.form.get('kuyov')
    kelin = request.form.get('kelin')
    sana = request.form.get('sana')
    vaqt = request.form.get('vaqt')

    # To'liq (absolyut) yo'llarni avtomatik topish
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_video = os.path.join(base_dir, "static", "template.mp4")
    font_file = os.path.join(base_dir, "static", "font.ttf")
    
    output_filename = f"outputs/taklifnoma_{int(time.time())}.mp4"
    output_filepath = os.path.join(base_dir, output_filename)

    if not os.path.exists(input_video) or not os.path.exists(font_file):
        return "Xatolik: 'template.mp4' yoki 'font.ttf' fayllari topilmadi! Ularni static papkasiga joylang."

    # Yo'llarni FFmpeg tushunadigan formatga keltirish (Ayniqsa Windows uchun muhim)
    font_file_ff = font_file.replace('\\', '/').replace(':', '\\:')

    text_filter = (
        f"drawtext=fontfile='{font_file_ff}':text='{kuyov} va {kelin}':fontcolor=gold:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2-100,"
        f"drawtext=fontfile='{font_file_ff}':text='{sana}':fontcolor=white:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+50,"
        f"drawtext=fontfile='{font_file_ff}':text='{vaqt}':fontcolor=white:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+130"
    )

    # DİQQAT: '-c:a', 'copy' olib tashlandi, ovozsiz videoda ham ishlayverishi uchun
    command = [
        'ffmpeg', '-i', input_video,
        '-vf', text_filter,
        '-y', output_filepath
    ]

    try:
        # Xatoliklarni tutib olish uchun maxsus sozlamalar
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return send_file(output_filepath, as_attachment=True)
    except subprocess.CalledProcessError as e:
        # Agar yana xato chiqsa, endi u 234 demaydi, balki to'liq muammoni yozib beradi
        error_msg = e.stderr.decode('utf-8', errors='ignore')
        return f"<h3>FFmpeg da xatolik yuz berdi:</h3><pre>{error_msg}</pre>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
