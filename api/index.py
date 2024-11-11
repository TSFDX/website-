from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        # Ambil URL dari request
        url = request.json.get('url')
        
        # Pengaturan download
        download_options = {
            'format': 'best[ext=mp4]',  # Pilih video terbaik
            'outtmpl': '/tmp/video.mp4'  # Simpan di folder sementara
        }
        
        # Proses download
        with yt_dlp.YoutubeDL(download_options) as downloader:
            video_info = downloader.extract_info(url, download=True)
            
        # Kirim balasan sukses
        return jsonify({
            'status': 'success',
            'message': 'Video berhasil didownload'
        })
    
    except Exception as error:
        # Tangani error
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 400

# Halaman utama
@app.route('/', methods=['GET'])
def home():
    return '''
    <html>
        <body>
            <h1>YouTube Downloader</h1>
            <input type="text" id="url" placeholder="Masukkan URL YouTube">
            <button onclick="download()">Download</button>
            
            <script>
                function download() {
                    const url = document.getElementById('url').value;
                    fetch('/api/download', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({url: url})
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                    });
                }
            </script>
        </body>
    </html>
    '''
