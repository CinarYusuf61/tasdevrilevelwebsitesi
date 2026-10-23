import os
import subprocess
import threading
import uuid
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

active_process = None
current_session_id = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_code')
def handle_run_code(data):
    global active_process, current_session_id
    
    session_id = str(uuid.uuid4())
    current_session_id = session_id
    
    if active_process:
        try:
            active_process.terminate()
            active_process.kill()
        except:
            pass
        active_process = None

    code = data.get('code', '')
    
    os.makedirs('codes', exist_ok=True)
    file_path = os.path.join('codes', 'main.cpp')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    emit('output', "\r\n[Sistem] Kod derleniyor...\r\n")
    
    try:
        # Doğrudan konteyner içinde g++ ile derleme yapıyoruz
        compile_cmd = ["g++", file_path, "-o", "codes/program"]
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if compile_result.returncode != 0:
            emit('output', f"\r\n--- DERLEME HATASI ---\r\n{compile_result.stderr}\r\n")
            return
        
        emit('output', "[Sistem] Derleme başarılı! Program başlatılıyor...\r\n\n")
        
        # Derlenen programı doğrudan çalıştırıyoruz
        run_cmd = ["./codes/program"]
        
        active_process = subprocess.Popen(
            run_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
            bufsize=0
        )
        
        def read_output(s_id):
            global active_process, current_session_id
            try:
                while active_process and current_session_id == s_id:
                    chunk = active_process.stdout.read(1024)
                    if not chunk:
                        break
                    if current_session_id == s_id:
                        text = chunk.decode('utf-8', errors='ignore')
                        text = text.replace('\r\n', '\n').replace('\n', '\r\n')
                        socketio.emit('output', text)
            except Exception:
                pass
            finally:
                if current_session_id == s_id:
                    socketio.emit('output', "\r\n\n[Sistem] Program sonlandırıldı.\r\n")
                    active_process = None

        threading.Thread(target=read_output, args=(session_id,)).start()

    except Exception as e:
        emit('output', f"\r\nSistem Hatası: {str(e)}\r\n")

@socketio.on('client_input')
def handle_client_input(data):
    global active_process
    if active_process and active_process.stdin:
        try:
            if data == '\r':
                data = '\n'
            active_process.stdin.write(data.encode('utf-8'))
            active_process.stdin.flush()
        except Exception:
            pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)