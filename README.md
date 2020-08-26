# song-pulse

## How to use locally
1) Install Docker (https://www.docker.com/products/docker-desktop)
2) Clone repository
3) Add your own SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to the docker-compose.yml file (get them from here https://developer.spotify.com/)
3) In the commandline use "docker-compose up --build"
4) A documentation for the API is then available under localhost:8080/docs

This sets up all the docker services necessary to run the backend. Including a database image, a radix queue and a worker image for background tasks.
To start a session, either the interactive docs or the webpage (https://github.com/song-pulse/webpage-song-pulse) can be used to create a user and add individual playlists for them.

To be able to receive data from the mobile apps locally, it is necessary to to expose the local port 8080. We used https://ngrok.com/ and an extra rule in the spotify developer project for the ngrok callback url.
The mobiles apps also have to be reprogrammed to send their data to the ngrok url.

## How to deploy
The necessary Docker images have been built and are available on Docker Hub. 
A docker-compose.yml to pull the respective images can be found in the "sciencecloud" directory. 
This also includes a frontend image based on our webpage repo which can be found here: https://github.com/song-pulse/webpage-song-pulse

## Introduction
A prototypical app that combines multiple physiological stress indicators to match the music that the developer is listening to with their current stress level.
To record the physiological data, a wrist device called Empatica E4 was used and native Android (https://github.com/song-pulse/android-song-pulse) and iOS (https://github.com/song-pulse/ios-song-pulse) Apps were developed to send the data to this backend.
It is also possible to send physiological data from other devices to the backend, but this has not beend tested.

## Functionalities
- API to set data and start processing
- Data clean up and processing to detect the state of the user (relaxed, balanced, stressed)
- Create individual stress baselines for each user
- Spotify integration to adapt the music to keep a user in a balanced state