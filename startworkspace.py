#! /usr/bin/env python3

'''Simple script to start a django server, and open the workspace.'''
import os

if __name__ == '__main__':
    #os.system("start cmd /K cd .\\")
    os.startfile(".\\")
    os.system('start cmd /K "env\\Scripts\\activate.bat & python manage.py runserver"')
