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

Examples present in the application in [PointwiseOperations.py](Application/ImageProcessingAlgorithms/PointwiseOperations.py) 
and [Thresholding.py](Application/ImageProcessingAlgorithms/Thresholding.py).

Adding algorithms will be done in the folder ImageProcessingAlgorithms.

The tool will automatically import all files that do not start with `_` (underscore). At the moment, the tool 
does not distinguish between files and packages, so packages will be included as well. If you want
to include files from packages, do so in a `__init__.py` file in your package.

In an imported file, algorithms shall be put in functions and they must be decorated with
the `@RegisterAlgorithm` decorator. Functions that do not have this decorator will not be 
registered by the tool. At the moment, the decorator works exclusively on functions (not on classes).

Requirements for a function to be registered correctly:
- your module/package must import numpy and the `@RegisterAlgorithm` decorator
- it must receive at least one parameter (name doesn't matter)
- it must return None or a numpy.ndarray (representing an image)
- the `@RegisterAlgorithm` decorator will receive the following 2 parameters in this order:
    1) a unique name for the algorithm (string)
    2) a menu or menu path in which it will reside in the UI (string)

Notes on the above mentioned:
- the parameter that will be passed to the function is a copy of the original image (the one on the left panel)
as a numpy.ndarray 
- the name of the algorithm will be shown in the UI 
- if the menu that is given does not exist in the UI, it will automatically be created. If it exists, the function is appended 
to the menu's list of actions. A menu path may consist of several menus that will also be created (nested, of course) 
automatically if they don't exist. Menu names in menu paths must be unique, even across other menus. So a nested menu 
in File cannot have the same name as another nested menu in Tools for example.

Optional parameters for the RegisterAlgorithm decorator (after the two mandatory ones):
- before: None or string; if the menu in which the algorithm will be added is populated, we can mention above ("before")
which element to add it. If the element's name doesn't exist, the algorithm will be appended to the end of the list.
- fromMainModel: list of strings; if data from the mainModel is needed, members of the MainModel class can be specified as strings,
and they will be sent to the function as named arguments (the function's parameters' names must match the names written
in the list which in turn must be the same names of the MainModel class attributes). Especially useful
for getting clicks (left or right).
- other named parameters

#### Reading user inputs for an algorithm
Some algorithms require the user to provide one or more inputs. Similar to the `@RegisterAlgorithm` decorator which
tells the tool what to do, there is another useful decorator called `@InputDialog`. This decorator instructs the program
to show an input dialog before calling the function to get user input and pass this user input to the function.

Requirements for a function to use `@InputDialog`:
- your module/package must import the `@InputDialog` decorator
- the function must have the `@RegisterAlgorithm` decorator; order of decorators doesn't mater; 

The `@InputDialog` decorator can accept any number of named parameters. Each parameter's name will be shown on a 
separate line with a textbox to its right.

Notes:
- parameters' names of the decorator must match parameters' names of the function
- parameters' values shall be callable entities (classes, functions or lambdas) that accept one parameter
- for each parameter, its value - the callable - will be called with the textbox's text (string) as the only parameter; 
the returned value of the callable will be transmitted to the function; ints, floats, strings or bools are the general
use case for this, but the user can define it's own classes and parse the string given for data (even xml or json parsers
are possible)

#### Displaying text results or errors
Some algorithms don't produce an image, but have other results which should be displayed to the user.
In the same fashion, the tool provides the `@OutputDialog` decorator. It will instruct the tool to show a text dialog 
when the function returns.

Requirements for a function to use `@OutputDialog`:
- your module/package must import the `@OutputDialog` decorator
- the function must have the `@RegisterAlgorithm` decorator; order of decorators doesn't mater; 

The `@OutputDialog` decorator accepts one mandatory string parameter: the dialog's title.

The displayed message will be OPTIONALLY* transmitted in the return value of the function in the following manners:
1) as the only return value:  `return "My message"`
2) as a second value in an iterable: `return image, "My message"`
    - the first case is equivalent to: `None, "My message"`
    - the message is removed from the iterable after it is displayed; after the removal, if the iterable contains just one element, the 
    element is returned to the tool, not the iterable; if the iterable contains more than one element, the first one is 
    transmitted as the result of the function and the rest of the iterable is discarded

*you can still transmit just the image if you wish so

### Adding plotting algorithms

Examples present in the tool [here](Application/PlottingAlgorithms/Basic.py).

One of the ways to extract information about an image is to plot different data or functions based on the image. The tool
comes with three basic algorithms in the PlottingAlgorithms package. You can add your own algorithms in this package. 
Same conventions apply to importing plotting algorithms (see above section): those who start with an underscore are
not imported, no distinction between modules and packages etc.

Plotting algorithms will be put in functions decorated with `@PlotterFunction`. It does not work on classes.
These functions will be registered by the tool and will be integrated in the UI automatically. It will be present in the
"Plot Function" drop down list in the Plotter window.

Requirements for a function to be registered correctly:
- your module/package must import the `@PlotterFunction` decorator and the `PlottingData` class
- it must receive at least one parameter (name doesn't matter)
- it must return a list
- the `@PlotterFunction` decorator will receive a unique name for the algorithm (string); it will be shown in the UI

Optional decorator parameters:
- fromMainModel: list of strings; if data from the mainModel is needed, members of the MainModel class can be specified as strings,
and they will be sent to the function as named arguments (the function's parameters' names must match the names written
in the list which in turn must be the same names of the MainModel class attributes). Especially useful
for getting clicks (left or right).
- computeOnImageChanged: bool; set this to true if you want to compute the plot function when the image in the panel 
changes; this function is called only once; especially useful for functions that do not depend on user
interaction or other outside data;
- computeOnClick: bool; set this to true if your data changes based on user clicks;
- other named parameters

Plotting functions are called in a lazy fashion. They are not called until they are selected in the drop-down list.

The values that you want to plot are stored in a `PlottingData` object. A plotting function must return a list of 
`PlottingData` objects. This allows one function to have multiple plots for comparison. 
Each `PlottingData` object contains:
- name: string; mandatory; this will be shown in the legend of the plotting window;
- y: iterable; mandatory; this is an iterable (list, tuple, generator, numpy.ndarray etc.) of values that will be 
plotted on the Y axis
- x: iterable; this is an iterable (list, tuple, generator, numpy.ndarray etc.) of values that will be 
plotted on the X axis; if not provided, the default is equivalent to `range(len(y))` (done by pyqtgraph library)
- pen: string or tuple of 4 ints; this sets the color of the plot; supported formats are RGBA and strings ('w' for white,
'b' for black, 'r' for red, 'g' for green, 'b' for green); see pyqtgraph library for details


### Customizing the application settings

## Frequently Asked Questions
> The app throws an "Import Error: DLL load failed: The specified module could not be found" exception

This is an opencv-python issue. Read the project's FAQ [here](https://pypi.org/project/opencv-python/).