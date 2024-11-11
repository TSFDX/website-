from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def download_youtube():
    try:
        url = request.form.get('url')
        
        # Konfigurasi tanpa merging format
        ydl_opts = {
            'format': 'mp4', # Pilih format video langsung
            'outtmpl': '%(title)s.%(ext)s',
            'nooverwrites': True,
            'no_warnings': True,
            'ignoreerrors': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return f"Error Download: {str(e)}", 400

@app.route('/download', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Downloader</title>
        <style>
            body { 
                font-family: Arial; 
                text-align: center; 
                margin-top: 50px; 
            }
            input { 
                width: 300px; 
                padding: 10px; 
                margin: 10px 0; 
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
            }
        </style>
    </head>
    <body>
        <h2>YouTube Video Downloader</h2>
        <form method="POST" action="/">
            <input type="text" name="url" placeholder="Masukkan URL YouTube">
            <br>
            <button type="submit">Download Video</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Buat direktori download jika belum ada
    os.makedirs('downloads', exist_ok=True)
