import os

# ===================== CONFIG =====================
DEFAULT_MIN_SIM = 10
FIXED_IMAGE_SIZE = 160
MAX_NAME_LENGTH_PER_LINE = 15
MAX_NAME_LINES = 3
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
INDEX_FILE = os.path.join(TEMP_FOLDER, "index.faiss")
PATHS_FILE = os.path.join(TEMP_FOLDER, "paths.pkl")
SUPPORTED_FORMATS = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff', '*.webp', '*.ppm', '*.pgm']
CLICK_DELAY = 300
# ===================================================