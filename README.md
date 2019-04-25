Timelapse Thingy
================
A script for taking a GoPro (or similar) batch of timelapse photos and grabbing frames from accompanying video.

Install requirements
------------
You will need ffmpeg. To install on macOS using Homebrew run `brew install ffmpeg`.
```
pip install -r requirements.txt
```

Usage
-----
```
$ ./main.py --master-dir GoPro --output-dir Output --slave-dirs DashCam/Front DashCam/Rear --slave-offset -130
```

This will run in alphabetic order through the images in the `GoPro` directory. It detects the timelapse interval and
then goes looking for the appropriate frames from the video files in the directories specified by `--slave-dirs`.
If your device timestamps weren't in perfect sync you can specify an offset in seconds via `--slave-offset`.
The resulting files in the `Output` directory will look like this:

```
0000001_01_G0030030.JPG                # GoPro image
0000001_02_20190414_114011_PF_240.JPG  # Frame 240 from DashCam/Front/20190414_114011_PF.mp4
0000001_03_20190414_114011_PR_240.JPG  # Frame 240 from DashCam/Rear/20190414_114011_PR.mp4
...
``` 

This allows you to composit frame `0000001` from the sources `01` (GoPro), `02` (forward facing dash cam) and
`03` (rear facing dash cam) any way you'd like. That's just my use case anyway 🙃.

The script even allows for breaks in the GoPro timelapse (mine overheated and shutdown when we were parked 😒).
The script will keep advancing through time by the detected interval until it finds the next timelapse image, repeating
the last timelapse image it saw before the break. 

Similarly, if the script cannot find corresponding frames from the videos in your slave directories it will repeat the
last image it was able to locate.
