from PyQt5.QtWidgets import QWidget, QAction
from PyQt5 import QtCore

import os
from PIL import Image, ImageEnhance

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

class ImageContrast(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageContrast, self).__init__()

        try:
            nodeflow_main.createAttribute(node=n, name='Image_Adjust', preset='Image', socket=True, plug=True, dataType='img', dataExpr=save_path)
        except:
            pass
        nodeflow_main.createAttribute(node=n, name='Image_Name', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Contrast', preset='Float', socket=True, plug=True, dataType='flt', dataAttr='')

class ImageContrastAction(QAction):
    """Model Create"""
    signal_Contrast = QtCore.pyqtSignal(object)

    def __init__(self, attrData, config):
        super(ImageContrastAction, self).__init__()

        IMAGE = attrData.get('Image_Name')
        CONTRAST = int(attrData.get('Contrast'))
        IMAGES = config.get('IMAGES')

        global save_path
        save_path = IMAGES + 'Contrast_' + os.path.basename(IMAGE)

        print(save_path)

        im = Image.open(IMAGE)
        enhancer = ImageEnhance.Contrast(im)
        enhanced_im = enhancer.enhance(CONTRAST)
        self.signal_Contrast.emit(enhanced_im)
        enhanced_im.show()
