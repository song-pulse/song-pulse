# song-pulse

## How to use
1) Install python and fastapi
2) TODO: describe docker 
3) clone this repo and run it (TODO: docker command for run backend here)

## Introduction
The goal of song-pulse is to keep the stress level of software engineers working in an open office space at a constantly good level. It should be at a level where developers are focused, but not stressed or bored. Therefore song-pulse adapts the music they are listening to in order to keep them at the right stress level. 
It should help getting them into the "flow". 
To achieve that this app uses a stress measuring sensor called Empatica E4 (https://www.empatica.com/) and a Spotify Integration for the music. 
The E4 device measures physiological data such as body temperature or heart rate variability. This data is used to get the stress level of the developer. 
After the stress level is assessed the music gets adapted using an RL algorithm. 

## Functionalities
- Receiving Data from E4 device
- Clean data from E4 (from movements etc)
- Create individual stress baselines for each user
- Learn through reinforcement learning which music leads to good stress states
- Compute music adaptions to bring the developer to the right stress state (according to results from RL)
- Spotify integration

## Preprocessing and Data Cleaning
We get the raw data from the E4. This data needs to be cleaned in order to minimize outer influences such as big physical movements. 
Additionally, we compute individual stress baselines for each user according to the collected E4 data. 

## Machine Learning (Reinforcement Learning)
Reinforcement Learning is used to learn about the individual behavior of the developers in terms of their music preferences and how they influence their stress level. This algorithm computes for every developer and every stress state the best possible music adaption in order to keep the developers stress in the baseline.
