import sys

if __name__ == "__main__":
    try:
        # these imports are here so that if one does not have a certain package installed
        # it will be caught as an exception and be shown on screen
        from PyQt5 import QtWidgets
        from Application.Presenters.MainPresenter import MainPresenter

        app = QtWidgets.QApplication(sys.argv)
        mainPresenter = MainPresenter(app)
        sys.exit(app.exec_())

    except SystemExit as exception:
        raise
    except BaseException as exception:
        # using Tk for displaying the exception as it comes with Python
        import tkinter
        from tkinter import messagebox
        import traceback

        exc_type, exc_value, exc_traceback = sys.exc_info()

        rootTk = tkinter.Tk()
        rootTk.withdraw()  # hide main window

        # under Windows, transient windows (such as messagebox) don’t show show up in the taskbar
        # this is a workaround
        # https://stackoverflow.com/a/45769196
        if rootTk._windowingsystem == 'win32':
            # windows showerror
            top = tkinter.Toplevel(rootTk)
            top.iconify()
            messagebox.showerror("Exception thrown",
                                 '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            top.destroy()
        else:
            # non-windows showerror
            messagebox.showerror("Exception thrown",
                                 '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

        rootTk.destroy()
