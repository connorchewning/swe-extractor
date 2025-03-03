# swe-extractor
This marimo notebook is meant as an example of what is possible when building marimo notebook based apps. It is a Marimo based app to read raster files and export a binary version based on a user defined threshold. Feel free to adapt the code for you use case.

# Installation

This repo is not intended to be installed as a package, but installing the package should ensure the necessary dependencies needed (not tested).

1) Clone this repository

2) Activate the envornment you wish to run the app in

2) If the needed dependencies are not already installed within your environment, install these or install the repo with
```sh
pip install -e path-to-swe-extractor
```

# Run the app

1) Run the app with marimo
```sh
marimo run swe-extract-app.py
```

2) Select the image and export folders
![](images\file_selection.png)

3) Cycle through, edit thresholds and save results
![](images\threshold.png)