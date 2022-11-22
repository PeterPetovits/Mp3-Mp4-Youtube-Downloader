# Mp3-Mp4-Youtube-Downloader

Προγράμματα που χρειάζονται: 

    1. python 3
    2. virtualenv (command: sudo apt install python3-virtualenv. Σε windows μάλλον μέσω pip). To init virtual environment type inside the project directory, virtualenv env.
    3. To start env type inside project directory source env/bin/activate and in Windows type \env\Scripts\activate.bat
    4. Inside env (check for '(env)' in the beginning of the command) type pip3 install flask to install flask
    5. To execute the main python file type python3 app.py

    6. pip3 install pytube inside env
    7. To save audio/video file we need to install os_sys pip install os_sys inside env
    8.For the metadata editor we need to insall tinytag : pip install eyed3 inside env
    9. For the trimmer we need to install trimmer: pip3 install trimmer inside env
    10. For trimmer we also need to install: For linux: apt install ffmpeg libavcodec-extra
                                            For Windows put ffmpeg binaries to PATH

    
New README.ME

Programs we need to install:
    1. python 3
    2. virtualenv (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
        Linux installation: "sudo apt install python3-virtualenv"
        Windows installation: "python -m pip install --user virtualenv"
        To init virtual environment type inside the project directory: For Linux "virtualenv env" and for Windows "py -m venv env".
        To start virtual environment type inside the project directory for Linux "source env/bin/activate" and for Windows ".\env\Scripts\activate"
    3. flask: pip3 install flask
        To execute the main python file type: for Linux "python3 app.py" or for Windows "python app.py"
    4. pytube: to install pytube inside the virtual environment type "pip3 install pytube" (https://pypi.org/project/pytube/)
    5. To save the audio files install os_sys inside the virtual environment, type "pip install os_sys"
    6. For metadata editor install eyeD3 inside virtual environment, type "pip install eyed3"
    7. For trimmer install trimmer inside virtual environment, type "pip3 install trimmer" (https://pypi.org/project/trimmer/)
    9. For trimmer we also need to install something extra inside the virtual environment: 
        For Linux: "sudo apt install ffmpeg libavcodec-extra"
        For Windows put ffmpeg binaries to PATH
    10. Inside virtual environment install ffmpeg:
        For Linux: sudo apt install ffmpeg
        For Windows download ffmpeg exe and add it to PATH (if not already done it)
    11. Inside virtual environment install dependency ffmpeg-python a python wrapper of ffmpeg, type "pip install ffmpeg-python"