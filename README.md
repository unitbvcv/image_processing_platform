# Image Processing Tool
## Features
This tool allows you to load a color/grayscale image and apply image processing algorithms on it, showing you the result in a different panel.

You can also plot different functions based on the images. There is also a magnifier avaiable.

Image processing and plotting algorithms are easy to integrate with the app.

## Requirements
- Python >= 3.5
- [PyQt5](https://pypi.org/project/PyQt5/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [numpy](https://pypi.org/project/numpy/)
- [pyqtgraph](https://pypi.org/project/pyqtgraph/)

## Installation
Install all the dependencies using the following command in a Command Prompt/Terminal (make sure you have the path to Python in the Environment Variables - PATH):

`pip install pyqt5 opencv-python numpy pyqtgraph`

## Usage
### Starting the application
Run the `ImageProcessingFramework.pyw` script using Python.

### UI Introduction

### Adding image processing algorithms

### Adding plotting algorithms

### Customizing the application settings

## Frequently Asked Questions
> The app throws an "Import Error: DLL load failed: The specified module could not be found" exception

This is an opencv-python issue. Read the project's FAQ [here](https://pypi.org/project/opencv-python/).