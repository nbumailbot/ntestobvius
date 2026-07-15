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
    # Asosiy sahifani ochish
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    # Frontend'dan kelgan ma'lumotlarni qabul qilish
    kuyov = request.form.get('kuyov')
    kelin = request.form.get('kelin')
    sana = request.form.get('sana')
    vaqt = request.form.get('vaqt')

    input_video = "static/template.mp4"
    font_file = "static/font.ttf"
    
    # Har bir yaratilgan video uchun unikal nom berish
    output_filename = f"outputs/taklifnoma_{int(time.time())}.mp4"

    # Agar fon fayllari yo'q bo'lsa xatolik berish
    if not os.path.exists(input_video) or not os.path.exists(font_file):
        return "Xatolik: 'static/template.mp4' yoki 'static/font.ttf' fayllari topilmadi. Iltimos ularni joylashtiring."

    # FFmpeg orqali matnlarni videoga chizish filtri
    # x va y - bu yozuvning ekrandagi joylashuvi. Uni o'z videongizga qarab moslaysiz.
    text_filter = (
        f"drawtext=fontfile={font_file}:text='{kuyov} va {kelin}':fontcolor=gold:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2-100,"
        f"drawtext=fontfile={font_file}:text='{sana}':fontcolor=white:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+50,"
        f"drawtext=fontfile={font_file}:text='{vaqt}':fontcolor=white:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+130"
    )

    # FFmpeg komandasi (-c:a copy orqali video musiqasi saqlab qolinadi)
    command = [
        'ffmpeg', '-i', input_video,
        '-vf', text_filter,
        '-c:a', 'copy',
        '-y', output_filename
    ]

    try:
        # Komandani terminalda ishga tushirish
        subprocess.run(command, check=True)
        # Yaratilgan faylni foydalanuvchiga yuklab berish
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return f"Video generatsiyasida xatolik yuz berdi: {str(e)}"

if __name__ == '__main__':
    # Serverni ishga tushirish
    app.run(debug=True, port=5000)
