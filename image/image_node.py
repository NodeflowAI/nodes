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

class ImageNode(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageNode, self).__init__()

        global nf
        nf = nodeflow_main

        global node
        node = n
        name = nn + 'Image_Dir'

        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')

class ImageNodeAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ImageNodeAction, self).__init__()

        IMAGE_DIR = attrData.get('Image_Dir')

        IMAGES = os.listdir(IMAGE_DIR)
        img_paths = []

        for img in IMAGES:
            img_name = os.path.basename(img)[:-4]
            img_path = IMAGE_DIR + '/' + img
            nf.createAttribute(node=node, name=img_name, preset='Image', socket=False, plug=True, dataType='img', dataAttr=img_path)
            img_paths.append(img_path)

        nf.createAttribute(node=node, name='All Images', index=-1,
                                      preset='Image', plug=True, socket=False, dataType='img', dataAttr=img_paths)