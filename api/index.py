from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pytube
import os
import requests

app = Flask(__name__)
CORS(app)

# Fungsi Download Utama
def download_youtube_video(url):
    try:
        # Bypass YouTube Restrictions
        pytube.request.default_range_size = 9437184
        
        # Inisialisasi YouTube
        yt = pytube.YouTube(
            url, 
            use_oauth=False,
            allow_oauth_cache=True
        )
        
        # Pilih Stream Terbaik
        video = yt.streams.get_highest_resolution()
        
        # Buat Direktori Tmp Jika Tidak Ada
        os.makedirs('/tmp', exist_ok=True)
        
        # Path Download
        output_path = f'/tmp/{yt.title}.mp4'
        
        # Download Video
        video.download(
            output_path='/tmp', 
            filename=f'{yt.title}.mp4'
        )
        
        return {
            'status': 'success',
            'title': yt.title,
            'path': output_path
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

# Route Download
@app.route('/api/download', methods=['POST'])
def download_route():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({
            'status': 'error',
            'message': 'URL YouTube diperlukan'
        }), 400
    
    # Proses Download
    result = download_youtube_video(url)
    
    if result['status'] == 'error':
        return jsonify(result), 400
    
    return jsonify(result)

# Route Streaming
@app.route('/api/stream', methods=['POST'])
def stream_video():
    data = request.json
    url = data.get('url')
    
    try:
        # Inisialisasi YouTube
        yt = pytube.YouTube(url)
        
        # Ambil Informasi Video
        return jsonify({
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'duration': yt.length,
            'views': yt.views,
            'rating': yt.rating
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# Halaman Utama
@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Downloader</title>
        <style>
            body { 
                font-family: Arial; 
                max-width: 500px; 
                margin: 0 auto; 
                padding: 20px; 
                text-align: center; 
            }
            input, button { 
                width: 100%; 
                padding: 10px; 
                margin: 10px 0; 
            }
        </style>
    </head>
    <body>
        <h1>📥 YouTube Downloader</h1>
        <input 
            type="text" 
            id="urlInput" 
            placeholder="Masukkan URL YouTube"
        >
        <button onclick="downloadVideo()">Download</button>
        <div id="result"></div>

        <script>
            async function downloadVideo() {
                const url = document.getElementById('urlInput').value;
                const resultDiv = document.getElementById('result');
                
                resultDiv.innerHTML = 'Memproses...';
                
                try {
                    const response = await fetch('/api/download', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ url })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        resultDiv.innerHTML = `Download Berhasil: ${data.title}`;
                    } else {
                        resultDiv.innerHTML = `Error: ${data.message}`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `Kesalahan: ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    '''

# Handler Vercel
def handler(event, context):
    return app(event, context)
