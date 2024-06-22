import streamlit as st

from scripts.DocumentBuilder import build_document
from scripts.Scraper import download_captions, get_channel_video_ids
from utils.constants import DATASET_PATH, DOCUMENTS_PATH


def main():
    """
    This function defines the Streamlit app logic
    """

    st.title("YouTube Caption Downloader")
    handle_name = st.text_input("Enter YouTube Channel Handle")
    num_videos = st.number_input(
        "Enter Number of Videos to Scrape", min_value=1, value=5, step=1
    )

    # Add a button to trigger the download process
    if st.button("Download Captions"):
        if handle_name:
            video_ids = get_channel_video_ids(handle_name, num_videos)
            download_captions(video_ids, DATASET_PATH)
            build_document(DATASET_PATH, DOCUMENTS_PATH)
            st.success(f"Captions downloaded for channel {handle_name}")
        else:
            st.error("Please enter a YouTube handle")


if __name__ == "__main__":
    main()
