# YT-Caption
YT-Caption will scrape captions from Youtube for N number of Machine Learning Tasks like Topic Modeling, Sentiment Analysis, etc.

# To Run the App

- Get your `GOOGLE_API_KEY`
- Create a `.env` file with same keys as `local.env` but populate your values
- Build docker image `sudo docker build -t yt-caption:latest .`
- Run the container `docker run -p 8501:8501 yt-caption:latest`

And you are good to go!


# TODOs
1. Topic Modeling on the extracted Captions.
  - Example: Ludwig Channel
    - <img src="https://github.com/pranshul-kaushik/YT-Caption/assets/52193416/7eb451c0-92f2-404e-a3f0-4f00c749f225" alt="image" width="400" height="400">
  - Example: Tina Channel
    - <img src="https://github.com/pranshul-kaushik/YT-Caption/assets/52193416/cb33b3d9-b1ef-4c23-92a3-71efac7415c3" alt="image" width="400" height="400">
2. ~~Slider to chunk the captions better on UI~~ ( UPDATED ) **Chunk size will be decided based on the time that caption text was visible on the screen**
3. Application can get a YT video url
4. SNS service to send Email with the Topic Modeling result
