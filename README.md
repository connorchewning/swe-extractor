# swe-extractor
A Marimo based app package with pixi to read raster files and export a binary version based on a user defined threshold.

# Quick Start
There are two ways to install and run the swe-extractor app.

## Pixi (Recomended)

1) If not already installed, install pixi: https://github.com/prefix-dev/pixi

2) Clone this repository

3) Navigate to the repository within the terminal

4) Run the app or open the marimo notebook for editing
```sh
pixi run app
```
```sh
pixi run edit_app
```

## Run the script as a marimo notebook

1) Clone this repository

2) Activate the envornment you wish to run the app in

2) Ensure the needed dependencies are installed in your environment. Dependencies can be found in the "pixi.toml" file

### Run the app
1) Navigate to the cloned repo

2) Run the app with marimo within the terminal
```sh
marimo run swe-extract-app.py
```


# App Snapshots
2) Select the image and export folders
![](images/file_selection.png)

3) Cycle through, edit thresholds and save results
![](images/threshold.png)