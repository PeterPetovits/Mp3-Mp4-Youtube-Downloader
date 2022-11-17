from flask import Flask, render_template, url_for, request, redirect
import os
from pytube import YouTube

fileNameDownloadPath = ''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mp3_download', methods= ["GET", "POST"])
def mp3_download():
    if request.method == "POST":
        youtube_link = request.form.get("youtube_link")
        yt = YouTube(str(youtube_link))
  
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
        
        # check for destination to save file
        destination = '.'
        
        # download the file
        out_file = video.download(output_path=destination)
        
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        fileNameDownloadPath = new_file
        print(fileNameDownloadPath)
        return render_template('index.html', result = "Download Complete", file = fileNameDownloadPath)
    return render_template('index.html')

@app.route('/mp4_download', methods= ["GET", "POST"])
def mp4_download():
    if request.method == "POST":
        youtube_link = request.form.get("youtube_link")

        yt = YouTube(str(youtube_link))
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('.')
        return redirect('index.html', result = "Download Complete")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)