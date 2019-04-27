# Global
FRAME_INDEX_DIGITS = 7
SOURCE_INDEX_DIGITS = 2
OUTPUT_FORMAT = 'JPG'

# Scrape
INTERVAL_ROUND_TO = 10

# Compile
MONTAGE_ARGS = ['-tile', '2x2', '-geometry', '1920x1080+0+0', '-background', 'black']
# In order: DashCam front (source 2), DashCam rear (source 3), GoPro (source 1), map frame (source 4)
MONTAGE_SOURCE_ORDER_DICT = {1: 3, 2: 1, 3: 2, 4: 4}
