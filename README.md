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
$ ./main.py --master-dir gopro --output-dir output --slave-dirs dashcam/front dashcam/rear --slave-offsets -158 -159
```

This will run in alphabetic order through the images in the `gopro` directory. It detects the timelapse interval and
then goes looking for the appropriate frames from the video files in the directories specified by `--slave-dirs`.
If your device clocks weren't in perfect sync you can specify the difference in seconds with `--slave-offsets`. The
resulting files in the `output` directory will look like this:
```
0000001_01_G0030030.JPG                # GoPro image
0000001_02_20190414_113821_PF_690.JPG  # Frame 690 from dashcam/front/20190414_113821_PF.mp4
0000001_03_20190414_113821_PR_660.JPG  # Frame 660 from dashcam/rear/20190414_113821_PR.mp4
...
```
This allows you to compose frame `0000001` from the sources `01` (GoPro), `02` (forward facing dash cam) and `03` (rear
facing dash cam) any way you'd like. That's just my use case anyway 🙃.

The script even allows for breaks in the GoPro timelapse (mine overheated and shutdown when we were parked 😒).
The script will keep advancing through time by the detected interval until it finds the next timelapse image, repeating
the last timelapse image it saw before the break. 

Similarly, if the script cannot find corresponding frames from the videos in your slave directories it will repeat the
last image it was able to locate.

Note: The most reliable way to identify the timestamps of video files is parsing the filename. If the video filenames
do not begin with a timestamp in `YYYYMMDD_HHmmss` format you can customise the date format e.g.
`--slave-filename-date-format '%Y_%m_%d_%H_%M_%s'`. You will also need to specify a different regular expression to match 
the date portion of the filename e.g. `--slave-filename-date-regex '^\\d{4}(?:_\\d{2}){5}'`. It's imperative your date
format is in descending order of magnitude e.g. year then month then day as this ensures sorting the files
alphabetically is identical to sorting the files by date 🍻. 
