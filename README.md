# YT-Caption
YT-Caption will scrape captions from Youtube for N number of Machine Learning Tasks like Topic Modeling, Sentiment Analysis, etc.

# To Run the App

- Get your `GOOGLE_API_KEY`
- Create a `.env` file with same keys as `local.env` but populate your values
- Build docker image `sudo docker build -t yt-caption:latest .`
- Run the container `docker run -p 8501:8501 yt-caption:latest`

And you are good to go!
