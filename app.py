from flask import Flask, render_template, request, send_from_directory, abort
import os
from pytube import YouTube
import ffmpeg
import eyed3
from werkzeug.datastructures import FileStorage
from moviepy.editor import VideoFileClip

#file pathname separator
sep = os.sep

UPLOAD_FOLDER = '.' + sep + 'upload-files'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLIENT_MUSIC'] = os.path.expanduser("~" + sep + "Desktop" + sep + "Mp3-Mp4-Youtube-Downloader")

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
        useless, songFileNameToTrimmer = fileNameDownloadPath.split(sep+'.'+sep)
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
        fileNameDownloadPathVideoOnly = yt.streams.filter(res = v_quality).first().download('.'+sep+'temp-video')
        #yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('.')
        
        global videoFileName
        useless, videoFileName = fileNameDownloadPathVideoOnly.split('.'+sep+'temp-video'+sep)   #keep the video file name for later in order to save it

        yt = YouTube(str(youtube_link))
        out_file = yt.streams.filter(only_audio=True).first().download('.'+sep+'temp-audio')  #extract audio only
        
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

        return render_template('index.html', result = "Download Complete", filePath = videoFileName, option_form_mp4 = "mp4", mp4_trimmer_open = "open")
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


#mp4 trimmer template after mp4 file download complete
@app.route('/mp4_trimmer_editor', methods = ["GET", "POST"])
def mp4_trimmer_editor():
    if request.method == "POST":

        start = str(request.form.get("start-time"))
        end = str(request.form.get("end-time"))

        clip = VideoFileClip(videoFileName)
        duration = clip.duration

        global fileNameDownloadPath
        
        if start == '' and end == '':       #if no values for trim have been inserted, just default passthrough to trimmer library
            return render_template('index.html', result = "Download Complete", option_form_mp4 = "mp4", mp4_trimmer_open = "open", result_trimmer = "Trim not applied", metadata_editor_open = "open")
        elif start != '' and end == '':     #if only start value for trim has been inserted
            os.system("ffmpeg -i " + '"' + videoFileName + '"' + " -codec copy " + '"' + "temp_vid.mp4" + '"')
            os.system("ffmpeg -y -i " + '"' + "temp_vid.mp4" + '"' + " -ss " + start + " -to " + str(duration) + " -c:v copy -c:a copy " + '"' + videoFileName + '"')
            os.remove("temp_vid.mp4")
            return render_template('index.html', result = "Download Complete", option_form_mp4 = "mp4", mp4_trimmer_open = "open", result_trimmer = "Trim for Start Done", metadata_editor_open = "open")
        elif start == '' and end != '':     #if only end value for trim has been inserted
            os.system("ffmpeg -i " + '"' + videoFileName + '"' + " -codec copy " + '"' + "temp_vid.mp4" + '"')
            os.system("ffmpeg -y -i " + '"' + "temp_vid.mp4" + '"' + " -ss " + "0" + " -to " + str(duration - int(end)) + " -c:v copy -c:a copy " + '"' + videoFileName + '"')
            os.remove("temp_vid.mp4")
            return render_template('index.html', result = "Download Complete", option_form_mp4 = "mp4", mp4_trimmer_open = "open", result_trimmer = "Trim for End Done", metadata_editor_open = "open")
        else:           #if both values have been inserted
            os.system("ffmpeg -i " + '"' + videoFileName + '"' + " -codec copy " + '"' + "temp_vid.mp4" + '"')
            os.system("ffmpeg -y -i " + '"' + "temp_vid.mp4" + '"' + " -ss " + start + " -to " + str(duration - int(end)) + " -c:v copy -c:a copy " + '"' + videoFileName + '"')
            os.remove("temp_vid.mp4")

            return render_template('index.html', result = "Download Complete", option_form_mp4 = "mp4", mp4_trimmer_open = "open", result_trimmer = "Trim Done")

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
        cover_art_file = request.files['cover_art_file']
        
        flag_no_cover_user = False
        if cover_art_file.filename == '':   #here we check if the request includes a cover art file
            print('inside first if block')
            flag_no_cover_user = True
            with open('.'+sep+'upload-files'+sep+'default-cover.jpeg', "rb") as fp:
                cover_art_file = FileStorage(fp, content_type='image/jpeg')
                
            print(cover_art_file)
        else:
            cover_art_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_art_file.filename))

        #useless, songFileName = fileNameDownloadPath.split('/./')

        songFileName = fileNameDownloadPath

        os.rename(songFileName, "temp.mp3")
        os.system("ffmpeg -i temp.mp3 -ab 320k temp2.mp3")
        os.rename("temp2.mp3", songFileName)
        os.remove("temp.mp3")

        try:
            audioFile = eyed3.load(songFileName)
            if not audioFile.tag:
                audioFile.initTag()

            if audioFile:
                audioFile.tag.artist = artist
                audioFile.tag.album = album
                audioFile.tag.album_artist = album_artist
                audioFile.tag.title = title
                audioFile.tag.track_number = track_number
                audioFile.tag.genre = genre
                audioFile.tag.year = year

                if(flag_no_cover_user):
                    with open(cover_art_file.filename, "rb") as cover_art:
                        audioFile.tag.images.set(0, cover_art.read(), "image/jpeg")

                    with open(cover_art_file.filename, "rb") as cover_art:
                        audioFile.tag.images.set(3, cover_art.read(), "image/jpeg")
                else:
                    with open(UPLOAD_FOLDER + sep + cover_art_file.filename, "rb") as cover_art:
                        audioFile.tag.images.set(0, cover_art.read(), "image/jpeg")

                    with open(UPLOAD_FOLDER + sep + cover_art_file.filename, "rb") as cover_art:
                        audioFile.tag.images.set(3, cover_art.read(), "image/jpeg")

                audioFile.tag.save()

                os.rename(songFileName, artist + " - " + title + ".mp3")
                os.remove(UPLOAD_FOLDER + sep + cover_art_file.filename)
                global finalFileNameMp3
                finalFileNameMp3 = artist + " - " + title + ".mp3"
        except IOError:
            IOError
        
        return render_template('index.html', result = "Download Complete", option_form_mp3 = "mp3", metadata_editor_open = "open", trimmer_open = "open", player_button_open = "open")
    return render_template('index.html')

#render mp3 player page in browser
@app.route('/mp3_player', methods= ["GET", "POST"])
def mp3_player():
    return render_template('mp3-player-One.html')

#download the final file to downloads folder in user's computer
@app.route('/download_file', methods = ["GET", "POST"])
def download_file():
    try:
        print(finalFileNameMp3)
        return send_from_directory(directory = app.config['CLIENT_MUSIC'], path = finalFileNameMp3, as_attachment = True)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)