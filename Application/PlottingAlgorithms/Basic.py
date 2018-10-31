from Application.Models.PlottingData import PlottingData

@PlotterFunction(image='both', title="Plot row values")
def plot_row_values(image):
    if image is None:
        return None  # throw exception?

    return PlottingData(

    )
