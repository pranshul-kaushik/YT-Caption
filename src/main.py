from utils.constants import DATASET_PATH, DOCUMENTS_PATH
from scripts.DocumentBuilder import build_document
from scripts.Scraper import get_channel_video_ids, download_captions


channel_id = 'UCFroPOUSXXZhO75WHSVpm6w'   #  Free Code Camp Youtube
video_ids = get_channel_video_ids(channel_id)

download_captions(video_ids, DATASET_PATH)

build_document(DATASET_PATH, DOCUMENTS_PATH)

