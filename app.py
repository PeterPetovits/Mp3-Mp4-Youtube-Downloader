from flask import Flask, render_template, url_for, request, redirect
import os
from pytube import YouTube
import ffmpeg
import eyed3

UPLOAD_FOLDER = './upload-files'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#original app route to index page
@app.route('/')
def index():
    return render_template('index.html')


#template page after pressing mp3 option button 
@app.route('/mp3_option_button', methods = ["GET", "POST"])
def mp3_option_button():
    if request.method == "POST":
        return render_template('index.html', option_form_mp3 = "mp3")
    return render_template('index.html')

      
#template page after pressing mp4 option button
@app.route('/mp4_option_button', methods = ["GET", "POST"])
def mp4_option_button():
    if request.method == "POST":
        return render_template('index.html', option_form_mp4 = "mp4")
    return render_template('index.html')


#mp3 download function after link inserted and download mp3 button pressed
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

        global fileNameDownloadPath
        fileNameDownloadPath = new_file

        global songFileNameToTrimmer
        useless, songFileNameToTrimmer = fileNameDownloadPath.split('/./')
        os.rename(songFileNameToTrimmer, "temp-download.mp3")
        os.system("ffmpeg -i temp-download.mp3 -ab 320k temp.mp3")
        os.rename("temp.mp3", songFileNameToTrimmer)
        os.remove("temp-download.mp3")
        return render_template('index.html', result = "Download Complete", file = fileNameDownloadPath, option_form_mp3 = "mp3", trimmer_open = "open")
    return render_template('index.html')


#mp4 download function after link inserted
@app.route('/mp4_download', methods= ["GET", "POST"])
def mp4_download():
    if request.method == "POST":
        youtube_link = request.form.get("youtube_link")
        video_quality = request.form.get("video_quality")

        yt = YouTube(str(youtube_link))
        v_quality = str(video_quality)
        fileNameDownloadPathVideoOnly = yt.streams.filter(res = v_quality).first().download('./temp-video')
        #yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('.')
        
        useless, videoFileName = fileNameDownloadPathVideoOnly.split('./temp-video/')   #keep the video file name for later in order to save it

        yt = YouTube(str(youtube_link))
        out_file = yt.streams.filter(only_audio=True).first().download('./temp-audio')  #extract audio only
        
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '_audio.mp4'
        os.rename(out_file, new_file)

        fileNameDownloadPathAudioOnly = new_file

        video_stream = ffmpeg.input(fileNameDownloadPathVideoOnly)
        audio_stream = ffmpeg.input(fileNameDownloadPathAudioOnly)
        ffmpeg.output(audio_stream, video_stream, videoFileName).run()

        if os.path.exists(str(fileNameDownloadPathVideoOnly)) and os.path.exists(str(fileNameDownloadPathAudioOnly)):       #delete the temp video and audio files
            os.remove(str(fileNameDownloadPathAudioOnly))
            os.remove(str(fileNameDownloadPathVideoOnly))
        else:
            print("The files do not exist")

        return render_template('index.html', result = "Download Complete", filePath = videoFileName, option_form_mp4 = "mp4")
    return render_template('index.html')


#mp3 trimmer template after mp3 file download complete
@app.route('/trimmer_editor', methods = ["GET", "POST"])
def trimmer_editor():
    if request.method == "POST":

        start = str(request.form.get("start-time"))
        end = str(request.form.get("end-time"))

        global fileNameDownloadPath
        
        if start == '' and end == '':       #if no values for trim have been inserted, just default passthrough to trimmer library
            os.system("trimmer " + '"' + songFileNameToTrimmer + '"' + " --title tempTitle --artist tempArtist")
            fileNameDownloadPath = str("tempArtist - tempTitle.mp3")
            return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", trimmer_open = "open", result_trimmer = "Trim not applied", metadata_editor_open = "open")
        elif start != '' and end == '':     #if only start value for trim has been inserted
            os.system("trimmer " + '"' + songFileNameToTrimmer + '"' + " --trim-start " + start + " --title tempTitle --artist tempArtist")
            fileNameDownloadPath = str("tempArtist - tempTitle.mp3")
            return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", trimmer_open = "open", result_trimmer = "Trim for Start Done", metadata_editor_open = "open")
        elif start == '' and end != '':     #if only end value for trim has been inserted
            os.system("trimmer " + '"' + songFileNameToTrimmer + '"' + " --trim-end " + end + " --title tempTitle --artist tempArtist")
            fileNameDownloadPath = str("tempArtist - tempTitle.mp3")
            return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", trimmer_open = "open", result_trimmer = "Trim for End Done", metadata_editor_open = "open")
        else:           #if both values have been inserted
            os.system("trimmer " + '"' + songFileNameToTrimmer + '"' + " --trim-start " + start + " --trim-end " + end + " --title tempTitle --artist tempArtist")
            fileNameDownloadPath = str("tempArtist - tempTitle.mp3")
            return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", trimmer_open = "open", result_trimmer = "Trim Done", metadata_editor_open = "open")

        #os.system("trimmer " + '"' + songFileNameToTrimmer + '"' + " --trim-start " + start + " --trim-end " + end + " --title tempTitle --artist tempArtist")

        #global fileNameDownloadPath
        #fileNameDownloadPath = str("tempArtist - tempTitle.mp3")

        #return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", trimmer_open = "open", result_trimmer = "Trim Done", metadata_editor_open = "open")
    return render_template('index.html')


#mp3 metadata editor after mp3 file trimming complete
@app.route('/mp3_metadata_editor', methods= ["GET", "POST"])
def mp3_metadata_editor():
    if request.method == "POST":

        artist = str(request.form.get("artist"))
        album = str(request.form.get("album"))
        album_artist = str(request.form.get("album_artist"))
        title = str(request.form.get("title"))
        track_number = str(request.form.get("track_number"))
        genre = str(request.form.get("genre"))
        year = str(request.form.get("year"))

        if 'cover_art_file' not in request.files:
            return render_template(request.url)
        else:
            cover_art_file = request.files['cover_art_file']

        if cover_art_file.filename == '':
            return redirect(request.url)
        if cover_art_file :
            cover_art_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_art_file.filename))

        #useless, songFileName = fileNameDownloadPath.split('/./')

        print(fileNameDownloadPath)
        songFileName = fileNameDownloadPath
        print(songFileName)

        os.rename(songFileName, "temp.mp3")
        os.system("ffmpeg -i temp.mp3 -ab 320k temp2.mp3")
        os.rename("temp2.mp3", songFileName)
        os.remove("temp.mp3")

        try:
            audioFile = eyed3.load(songFileName)
            if not audioFile.tag:
                audioFile.initTag()

            if audioFile:
                print("1")
                audioFile.tag.artist = artist
                audioFile.tag.album = album
                audioFile.tag.album_artist = album_artist
                audioFile.tag.title = title
                audioFile.tag.track_number = track_number
                audioFile.tag.genre = genre
                audioFile.tag.year = year

                with open(UPLOAD_FOLDER + "/" + cover_art_file.filename, "rb") as cover_art:
                    audioFile.tag.images.set(0, cover_art.read(), "image/jpeg")

                with open(UPLOAD_FOLDER + "/" + cover_art_file.filename, "rb") as cover_art:
                    audioFile.tag.images.set(3, cover_art.read(), "image/jpeg")

                audioFile.tag.save()

                os.rename(songFileName, artist + " - " + title + ".mp3")
                os.remove(UPLOAD_FOLDER + "/" + cover_art_file.filename)
                global finalFileNameMp3
                finalFileNameMp3 = artist + " - " + title + ".mp3"
        except IOError:
            IOError
        
        return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", metadata_editor_open = "open", trimmer_open = "open")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)