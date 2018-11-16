# ---------------------------------------------------------------------------
# SemesterProject_source.py
#
# Author(s):  Joseph Brewer / Jaxon White
# Creation Date: 11/14/2018
#
# Development Environment:
#   Pycharm
#   Python 3.7
#
# This script is a general visualization tool used in conjunction with
# the ongoing water-related-energy study, under the CUASHI research
# umbrella, focusing on the Living & Learning Community at Utah State.
# Based on input, it queries an InfluxDB database, where
# water consumption data and associated water temperature data are stored.
# Based on user input, the script performs a variety of tasks, including:
#   - comparison of water-related energy use between buildings
#   - outputs a variety of visualizations for water-related energy use
#   - performs some basic statistical analysis on water-related energy use.
#
# ----------------------------------------------------------------------------

from tkinter import *
from tkinter.ttk import Frame, Button, Style


class Example(Frame):
    def __init__(master):
        super().__init__()

        master.initUI()

    def initUI(master):

        master.master.title("MILTON")

        master.style = Style()
        master.style.theme_use("default")








        frame = Frame(master, relief = RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        master.pack(fill=BOTH, expand=1)


        quitButton = Button(master, text="Quit", command=master.quit)
        quitButton.pack(side=RIGHT, padx=5, pady=5)
        runButton = Button(master, text="Run")  # add "command=execute"
        runButton.pack(side=RIGHT)








def main():
    root = Tk()
    root.geometry("700x600+300+300")






    app = Example()
    root.mainloop()

if __name__=='__main__':
    main()

