# Mp3-Mp4-Youtube-Downloader

Programs we need to install:
    1. Python 3
    2. Virtualenv (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
        Linux installation: "sudo apt install python3-virtualenv"
        Windows installation: "python -m pip install --user virtualenv", but before in Powershell (as administrator) "Set-ExecutionPolicy RemoteSigned".
        To init virtual environment type inside the project directory: For Linux "virtualenv env" and for Windows "py -m venv env".
        To start virtual environment type inside the project directory for Linux "source env/bin/activate" and for Windows ".\env\Scripts\activate"
    3. Flask: pip3 install flask
        To execute the main python file type: for Linux "python3 app.py" or for Windows "python app.py"
    4. Pytube: to install pytube inside the virtual environment type "pip3 install pytube" (https://pypi.org/project/pytube/)
    5. For metadata editor install eyeD3 inside virtual environment, type "pip install eyed3"
    6. For trimmer install trimmer inside virtual environment, type "pip3 install trimmer" (https://pypi.org/project/trimmer/)
    7. For trimmer we also need to install something extra inside the virtual environment: 
        For Linux: "sudo apt install ffmpeg libavcodec-extra"
        For Windows put ffmpeg binaries to PATH
    8. Inside virtual environment install ffmpeg:
        For Linux: "sudo apt install ffmpeg"
        For Windows download ffmpeg exe and add it to PATH (if not already done it)
    9. Inside virtual environment install dependency ffmpeg-python a python wrapper of ffmpeg, type "pip install ffmpeg-python"
    10. For the mp4 trimmer install moviepy library: "pip install moviepy"