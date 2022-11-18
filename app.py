from flask import Flask, render_template, url_for, request, redirect
import os
from pytube import YouTube

fileNameDownloadPath = ''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mp3_option_button', methods = ["GET", "POST"])
def mp3_option_button():
    if request.method == "POST":
        return render_template('index.html', option_form_mp3 = "mp3")
    return render_template('mp3-form.html')
        

@app.route('/mp4_option_button', methods = ["GET", "POST"])
def mp4_option_button():
    if request.method == "POST":
        return render_template('index.html', option_form_mp4 = "mp4")
    return render_template('mp4-form.html')

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
        return render_template('index.html', result = "Download Complete", file = fileNameDownloadPath, option_form_mp3 = "mp3")
    return render_template('index.html')

@app.route('/mp4_download', methods= ["GET", "POST"])
def mp4_download():
    if request.method == "POST":
        youtube_link = request.form.get("youtube_link")
        yt = YouTube(str(youtube_link))
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('.')
        return render_template('index.html', result = "Download Complete", option_form_mp4 = "mp4")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)