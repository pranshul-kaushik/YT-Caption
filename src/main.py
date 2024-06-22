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
            caption_paths = download_captions(handle_name, video_ids, DATASET_PATH)
            caption_document_path = build_document(
                handle_name, caption_paths, DOCUMENTS_PATH
            )

            # TODO: Save all the data to S3 and then delete the locally dowloaded files
            # ...

            st.success(f"Captions downloaded for channel {handle_name}")
        else:
            st.error("Please enter a YouTube handle")


if __name__ == "__main__":
    main()
