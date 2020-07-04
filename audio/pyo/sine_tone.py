from PyQt5.QtWidgets import QWidget, QAction

from pyo import *

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

class SineTone(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(SineTone, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Volume', preset='Float', socket=True, plug=True, dataType='flt', dataAttr='')

class SineToneAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(SineToneAction, self).__init__()

        VOL = attrData.get('Volume')

        # Creates and boots the server.
        # The user should send the "start" command from the GUI.
        s = Server().boot()
        # Drops the gain by 20 dB.
        s.amp = VOL

        # Creates a sine wave player.
        # The out() method starts the processing
        # and sends the signal to the output.
        a = Sine().out()

        # Opens the server graphical interface.
        s.gui(locals())