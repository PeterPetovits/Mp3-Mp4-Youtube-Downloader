import os

os.rename("Fall Out Boy - This Aint A Scene Its An Arms Race (Official Music Video).mp3", "temp.mp3")

os.system("ffmpeg -i temp.mp3 -ab 320k  newfilename1.mp3")

print("done")