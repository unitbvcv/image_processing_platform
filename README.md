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
Adding algorithms will be done in the folder ImageProcessingAlgorithms.

The tool will automatically import all files that do not start with '_'. At the moment, the tool 
does not distinguish between files and packages, so packages will be included as well. If you want
to include files from packages, do so in a `__init__.py` file in your package.

In an imported file, algorithms shall be put in functions and they must be decorated with
the `@RegisterAlgorithm` decorator. Functions that do not have this decorator will not be 
registered by the tool. At the moment, the decorator works exclusively on functions (not on classes).

#### Requirements for a function to be registered correctly:
- your module/package must import numpy and the RegisterAlgorithm decorator
- it must receive at least one parameter (name doesn't matter)
- it must return None or a numpy.ndarray
- the `@RegisterAlgorithm` decorator will receive the following 2 parameters
    - an unique name for the algorithm (string)
    - a menu or menu path in which it will reside in the UI (string)
    
The parameter that will be passed to the function is a copy of the original image (the one on the left panel)
as a numpy.ndarray. The name of the algorithm will be shown in the UI. If the menu that is given does
not exist in the UI, it will automatically be created. If it exists, it is appended to the menu's list of action.
A menu path may consist of several menus that will also be created (nested, of course) automatically if they 
don't exist. Menu names in menu paths must be unique, even across other menus. So a nested menu in File cannot have 
the same name as another nested menu in Tools for example.

Optional parameters for the RegisterAlgorithm decorator:
- before: None or string; if the menu in which the algorithm will be added is populated, we can mention above ("before")
which element to add it. If the element's name doesn't exist, the algorithm will be appended to the end of the list.
- fromMainModel: list; if data from the mainModel is needed, members of the MainModel class can be specified as strings,
and they will be sent to the function as named arguments (the function's parameters' names must match the names written
in the list which in turn must be the same names of the MainModel class attributes). Especially useful
for getting clicks (left or right).
- other named parameters

### Adding plotting algorithms

### Customizing the application settings

## Frequently Asked Questions
> The app throws an "Import Error: DLL load failed: The specified module could not be found" exception

This is an opencv-python issue. Read the project's FAQ [here](https://pypi.org/project/opencv-python/).