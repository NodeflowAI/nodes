from PyQt5.QtWidgets import QWidget, QAction

from gym import envs

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

class AtariGames(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(AtariGames, self).__init__()

        print(envs.registry.all())
        for game in envs.registry.all():
            name = (str(game).replace("EnvSpec(", "").replace(")", ""))
            nodeflow_main.createAttribute(node=n, name=name, preset='String', socket=True, plug=True, dataType='str', dataAttr=name)


class AtariGamesAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(AtariGamesAction, self).__init__()