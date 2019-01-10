import sys

if __name__ == "__main__":
    try:
        # these imports are here so that if one does not have a certain package installed
        # it will be caught as an exception and be shown on screen
        from PyQt5 import QtWidgets
        from Application.ViewModels.MainVM import MainVM

        app = QtWidgets.QApplication(sys.argv)
        mainViewModel = MainVM(app)
        sys.exit(app.exec_())
    except Exception as exception:
        # using Tk for displaying the exception as it comes with Python
        import tkinter
        from tkinter import messagebox
        import traceback

        exc_type, exc_value, exc_traceback = sys.exc_info()

        tkMainWindow = tkinter.Tk()
        tkMainWindow.withdraw()  # hide main window
        messagebox.showerror("Exception thrown", '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
