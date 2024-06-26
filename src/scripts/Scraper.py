import json
import os
from uuid import uuid4

import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

from utils.constants import CHANNEL_ID_URL

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_channel_id(handle_name):
    try:
        response = requests.get(
            CHANNEL_ID_URL.format(
                handle_name=handle_name, GOOGLE_API_KEY=GOOGLE_API_KEY
            )
        )
        response.raise_for_status()  # Raise an exception for unsuccessful requests

        # Parse the JSON response
        data = json.loads(response.text)

        # Check if there are any items
        if not data["items"]:
            print("No Channel found in the response")
            raise "No Channel Found!"
        else:
            # Get the first item and extract the id
            first_item = data["items"][0]
            channel_id = first_item["id"]

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e
    return channel_id


def get_channel_video_ids(handle_name, num_videos):
    channel_id = get_channel_id(handle_name)
    youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

    # Get the uploads playlist ID for the channel
    playlist_response = (
        youtube.channels().list(part="contentDetails", id=channel_id).execute()
    )

    uploads_playlist_id = playlist_response["items"][0]["contentDetails"][
        "relatedPlaylists"
    ]["uploads"]

    # Get all video IDs in the uploads playlist
    playlist_items = []
    next_page_token = None

    while True:
        playlist_response = (
            youtube.playlistItems()
            .list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=30,
                pageToken=next_page_token,
            )
            .execute()
        )

        playlist_items.extend(playlist_response["items"])
        next_page_token = playlist_response.get("nextPageToken")

        if not next_page_token or len(playlist_items) >= num_videos:
            break

    video_ids = [item["contentDetails"]["videoId"] for item in playlist_items]
    return video_ids


def list_of_dicts_to_jsonl(list_of_dicts, output_file):
    with open(output_file, "w") as file:
        for dictionary in list_of_dicts:
            json_line = json.dumps(dictionary)
            file.write(json_line + "\n")


def download_captions(handle_name, video_ids, DATASET_PATH):
    caption_paths = []

    for video_id in tqdm(video_ids):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            file_path = (
                f"{DATASET_PATH}{handle_name}_{video_id}_{uuid4().hex}_captions.jsonl"
            )
            list_of_dicts_to_jsonl(transcript, file_path)
            caption_paths.append(file_path)

        except Exception as e:
            print(f"An error occurred for video {video_id}: {str(e)}")

    return caption_paths


def save_captions_to_file(video_id, transcript):
    filename = f"./dataset/{video_id}_captions.txt"
    with open(filename, "w", encoding="utf-8") as file:
        for entry in transcript:
            file.write(f"{entry['text']} ")
