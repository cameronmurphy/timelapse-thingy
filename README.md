Timelapse Thingy
================
Some scripts for taking source material from a timelapse camera such as a GoPro and video cameras such as dash cams and
building out a video like [this](todo://linkme).

Install requirements
------------
You will need ffmpeg and ImageMagick. To install on macOS using Homebrew run `brew install ffmpeg imagemagick`.
```
pip install -r requirements.txt
```

Scrape
------
This script scrapes frames from your 'slave' video sources.

```
$ timelapse-thingy/scrape.py --master-dir gopro --output-dir scrape-output --slave-dirs dashcam/front dashcam/rear --slave-offsets -159 -160
```

This will run in alphabetic order through the images in the `gopro` directory. It detects the timelapse interval and
then goes looking for the appropriate frames from the video files in the directories specified by `--slave-dirs`.
If your device clocks weren't in perfect sync you can specify the difference in seconds with `--slave-offsets`. The
resulting files in the `output` directory will look something like this:
```
0000001_01_G0030030.JPG                # Source 01 - GoPro image
0000001_02_20190414_113821_PF_660.JPG  # Source 02 - Frame 660 from dashcam/front/20190414_113821_PF.mp4
0000001_03_20190414_113821_PR_630.JPG  # Source 03 - Frame 630 from dashcam/rear/20190414_113821_PR.mp4

0000002_01_G0030031.JPG                # Source 01 - GoPro image
0000002_02_20190414_113821_PF_1590.JPG # Source 02 - Frame 1590 from dashcam/front/20190414_113821_PF.mp4
0000002_03_20190414_113821_PR_1560.JPG # Source 03 - Frame 1560 from dashcam/rear/20190414_113821_PR.mp4

...
```
Here, frames `0000001` and `0000002` can later be combined into composed frames for your unified timelapse video.

The scrape script even allows for breaks in the GoPro timelapse (mine likes to overheat and shutdown when my car is
parked 😒). The script will keep advancing through time by the detected timelapse interval until it finds the next
appropriate timelapse image, repeating the last image it saw before the break. 

Similarly, if the script cannot find corresponding frames from the videos in your slave directories it will repeat the
last image it was able to locate.

Note: The most reliable way to identify the timestamps of video files is parsing the filename. If the video filenames
do not begin with a timestamp in `YYYYMMDD_HHmmss` format you can customise the date format e.g.
`--slave-filename-date-format '%Y_%m_%d_%H_%M_%s'`. You will also need to specify a different regular expression to
match the date portion of the filename e.g. `--slave-filename-date-regex '^\\d{4}(?:_\\d{2}){5}'`. It's imperative your
date format is in descending order of magnitude e.g. year then month then day as this ensures sorting the files
alphabetically is identical to sorting the files by date 🍻. 

Compose
-------
This script takes your source images (written by `scrape.py` or otherwise) and compiles them into output frame images
using the `montage` tool from ImageMagick.
```
$ timelapse-thingy/compose.py --input-dir scrape-output --output-dir compose-output
```
By default, based on the `MONTAGE_ARGS` and `MONTAGE_SOURCE_ORDER_DICT` constants in `constants.py`, this builds 4K
(3840x2160) frames with a 2x2 grid of images sized to 1920x1080. For me, this put source 02 (dash cam front) in the top
left, source 03 (dash cam rear) in the top right, source 01 (GoPro) in the bottom left and source 04 (a custom generated
frame) in the bottom right by feel free to tweak it 🐫.

Tip: my GoPro outputs 4000 x 3000 images so I used this command to convert the GoPro (source 01) images to 16:9.
```
$ find scrape-output -name '*_01_*' -exec convert {} -distort SRT 1,0 -gravity center -crop 4000x2250+0+0 +repage {} \;
```
This isn't mandatory but if you leave images at 4x3 aspect ratio there will be black bars either side of your images in
the composed frames.
