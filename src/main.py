from utils.constants import DATASET_PATH, DOCUMENTS_PATH
from scripts.DocumentBuilder import build_document
from scripts.Scraper import get_channel_video_ids, download_captions

handle_name = ""

video_ids = get_channel_video_ids(handle_name)

download_captions(video_ids, DATASET_PATH)

build_document(DATASET_PATH, DOCUMENTS_PATH)

