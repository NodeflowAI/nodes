from PyQt5.QtWidgets import QWidget, QAction

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

class CartPole(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CartPole, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Program', preset='String', socket=True, plug=True, dataType='str', dataAttr='CartPole-v0')
        nodeflow_main.createAttribute(node=n, name='Length', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1000)

class CartPoleAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(CartPoleAction, self).__init__()

        import gym

        PROGRAM = attrData.get('Program')
        LENGTH = int(attrData.get('Length'))

        env = gym.make(PROGRAM)
        env.reset()
        for _ in range(LENGTH):
            env.render()
            env.step(env.action_space.sample())  # take a random action
        env.close()