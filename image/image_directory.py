from PyQt5.QtWidgets import QWidget, QAction

import os

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
DOT = config['ACTION']['DOT']
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']
N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class ImageDirectory(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageDirectory, self).__init__()

        global nfm
        nfm = nodeflow_main

        global node
        node = n

        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')

class ImageDirectoryAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ImageDirectoryAction, self).__init__()

        IMAGE_DIR = attrData.get('Image_Dir')

        IMAGES = os.listdir(IMAGE_DIR)
        img_paths = []

        for img in IMAGES:
            img_paths.append(IMAGE_DIR + '/' + img)

        nfm.createAttribute(node=node, name='All Images', index=-1, preset='Image', plug=True, socket=False, dataType='img', dataAttr=img_paths)