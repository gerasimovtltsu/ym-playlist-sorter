# Yandex Music Playlist Sorter

This repository contains a Python program called "Yandex Music Playlist Sorter" that allows you to sort tracks in your Yandex.Music "Liked" playlist based on their genres.

## Prerequisites

Before running the program, make sure you have the following:

- Python (3.12.4 tested) installed on your machine
- Yandex.Music account credentials
- Yandex.Music API access token
- User ID and Playlist ID for the "Liked" playlist

## Get Yandex Music API TOKEN

https://yandex-music.readthedocs.io/en/main/token.html

## Installation

1. Clone this repository to your local machine:
```
git clone https://github.com/gerasimovtltsu/ym-playlist-sorter.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Set up the necessary environment variables by creating a `.env` file and adding the following:
```
TOKEN=<your-yandex-music-api-token>
USERID=<your-yandex-music-user-id>
PLAYLISTID=<your-liked-tracks-playlist-id>
```

4. Run the program:
```
python main.py
```

GET RESULT

![Alt text](image.png)

## Usage

Once you have set up the program and run it, it will initiate the Yandex.Music client and fetch tracks from the specified "Liked" playlist. The tracks will then be sorted into different playlists based on their genres. The newly created playlists will be private.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.
