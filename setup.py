#! python
#coding=utf-8
#setup.py
import os
os.environ['TCL_LIBRARY'] = "C:/Program Files/Python_3.6/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Program Files/Python_3.6/tcl/tk8.6"
import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(
    name = "Snake",
    version = "0.1",
    options={"build_exe": {"packages":["pygame"], 
                           "include_files":["images/apple.png","images/snake_head.png","sounds/crunch.wav", "fonts/CloisterBlack.ttf"]}},
    description = "Snake Game, made with Python + PyGame",
    author = "Nikos J. Lazaridis",
    executables = executables
)