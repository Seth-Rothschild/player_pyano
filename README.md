# About
This is a flask app which allows a user to play a midi file. This is meant for use with a Yamaha Disklavier where the idea is that it can run on a Raspberry Pi and be controlled on the local network.

# Installation
First, install [miniforge](https://github.com/conda-forge/miniforge) after which you can create a conda environment and install the dependencies with 
```
make install
```

You can then run the app with `make start` and navigate to `localhost:5000` in your browser.
