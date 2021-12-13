![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kruksik-dev/CV2_blobs_detector)
[![Python 3.9](https://img.shields.io/badge/python-3.9-green.svg)](https://www.python.org/downloads/release/python-360/)

# Blobs detector 

A simple detector that detects circular imperfections in photos for counting.

The program was created to facilitate the work of counting cancer cells. To this end, some optimization has been made based on the initial images that were processed. Therefore, it has the function:

`def remove_background_gray(img)`

It is used to remove the background from those specific photos. The program will also run without it, so you can comment it if necessary


## Usage/Examples

The files that we want to process should be placed in the target_pictures folder. 

All the necessary libraries will be installed when the program is started, so it is not necessary to install them manually.

```python
python detector.py
```

Processed photos will appear in the results folder, and additionally the results will be saved in the output.csv file in the root path.