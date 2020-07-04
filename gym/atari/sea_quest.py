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

class BreakOut(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(BreakOut, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Program', preset='String', socket=True, plug=True, dataType='str', dataAttr='Seaquest-v0')
        nodeflow_main.createAttribute(node=n, name='Episode', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=20)
        nodeflow_main.createAttribute(node=n, name='Length', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1000)

        nodeflow_main.createAttribute(node=n, name='Observation', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Reward', preset='Float', socket=True, plug=True, dataType='flt', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Done', preset='Bool', socket=True, plug=True, dataType='bool', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Info', preset='String', socket=True, plug=True, dataType='str', dataAttr='')


class BreakOutAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(BreakOutAction, self).__init__()

        import gym

        PROGRAM = attrData.get('Program')
        EPISODE = int(attrData.get('Episode'))
        LENGTH = int(attrData.get('Length'))

        env = gym.make(PROGRAM)
        for i_episode in range(EPISODE):
            observation = env.reset()
            for t in range(LENGTH):
                env.render()
                #print(observation)
                action = env.action_space.sample()
                observation, reward, done, info = env.step(action)
                if done:
                    print("Episode finished after {} timesteps".format(t + 1))
                    break
        env.close()