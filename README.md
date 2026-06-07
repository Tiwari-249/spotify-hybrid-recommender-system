# Spotify Hybrid Music Recommender System

A hybrid music recommendation system that suggests Spotify songs using both content-based filtering and collaborative filtering. The project includes data preprocessing, feature transformation, recommendation logic, an interactive Streamlit app, DVC-based data versioning, Docker containerization, automated testing, and AWS CI/CD deployment.

## Overview

This project recommends songs based on a selected song and artist. It supports two recommendation modes:

- **Content-Based Filtering:** Recommends songs using metadata, audio features, tags, artist, year, key, time signature, and other song-level attributes.
- **Hybrid Recommendation:** Combines content-based similarity with collaborative filtering based on user listening history and play counts.

If the selected song exists in the collaborative filtering dataset, the system uses the hybrid recommender. Otherwise, it falls back to content-based recommendations.

## Features

- Song and artist-based search
- Top 5, 10, 15, or 20 recommendations
- Hybrid recommendation engine
- Content-based filtering using cosine similarity
- Collaborative filtering using user-track interaction data
- Diversity slider to control the balance between personalized and diverse recommendations
- Spotify preview audio playback
- Streamlit web interface
- DVC pipeline for reproducible data processing
- Dockerized application
- Pytest-based app health check
- GitHub Actions CI/CD pipeline
- AWS deployment using ECR, S3, CodeDeploy, and EC2

## Tech Stack

- **Language:** Python
- **ML/Data Processing:** Pandas, NumPy, Scikit-learn, SciPy, Dask
- **Recommendation Methods:** Content-based filtering, collaborative filtering, hybrid weighted similarity
- **Frontend/App:** Streamlit
- **Data Versioning:** DVC
- **Testing:** Pytest, Requests
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud Deployment:** AWS ECR, AWS S3, AWS CodeDeploy, AWS EC2

## Project Structure

```text
spotify-hybrid-recommender-system/
│
├── app.py
├── data_cleaning.py
├── content_based_filtering.py
├── collaborative_filtering.py
├── hybrid_recommendations.py
├── transform_filtered_data.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── dvc.yaml
├── dvc.lock
├── appspec.yml
│
├── data/
│   ├── Music Info.csv.dvc
│   └── User Listening History.csv.dvc
│
├── deploy/
│   └── scripts/
│       ├── install_dependencies.sh
│       └── start_docker.sh
│
└── .github/
    └── workflows/
        └── ci.yaml
