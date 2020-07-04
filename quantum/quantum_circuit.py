from PyQt5.QtWidgets import QWidget, QAction

import numpy as np
from qiskit import *

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

class QuantumCircuit(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(QuantumCircuit, self).__init__()

        QUBITS = 3
        nodeflow_main.createAttribute(node=n, name='Qubits', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=QUBITS)

class QuantumCircuitAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(QuantumCircuitAction, self).__init__()

        QUBITS = int(attrData.get('Qubits'))


        # Create a Quantum Circuit acting on a quantum register of three qubits
        circ = QuantumCircuit(QUBITS)

        # Add a H gate on qubit 0, putting this qubit in superposition.
        circ.h(0)
        # Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
        # the qubits in a Bell state.
        circ.cx(0, 1)
        # Add a CX (CNOT) gate on control qubit 0 and target qubit 2, putting
        # the qubits in a GHZ state.
        circ.cx(0, 2)

        circ.draw('mpl')