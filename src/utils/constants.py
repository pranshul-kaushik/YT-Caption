import os

DATASET_PATH = "./dataset/"
DOCUMENTS_PATH = './documents/'

os.makedirs(DATASET_PATH, exist_ok= True)
os.makedirs(DOCUMENTS_PATH, exist_ok= True)

# Get Channel ID URL
CHANNEL_ID_URL = "https://www.googleapis.com/youtube/v3/channels?key={GOOGLE_API_KEY}&forHandle={handle_name}&part=id"