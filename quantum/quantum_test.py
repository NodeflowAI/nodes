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

class QuantumTest(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(QuantumTest, self).__init__()

        SHOTS = 1000
        SIMULATOR = 'qasm_simulator'

        nodeflow_main.createAttribute(node=n, name='Token', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Shots', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHOTS)
        nodeflow_main.createAttribute(node=n, name='Simulator', preset='String', socket=True, plug=True, dataType='str', dataAttr=SIMULATOR)



class QuantumTestAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(QuantumTestAction, self).__init__()

        SHOTS = int(attrData.get('Shots'))
        SIMULATOR = attrData.get('Simulator')

        import numpy as np
        from qiskit import (
            QuantumCircuit,
            execute,
            Aer)
        from qiskit.visualization import plot_histogram

        # Use Aer's qasm_simulator
        simulator = Aer.get_backend(SIMULATOR)

        # Create a Quantum Circuit acting on the q register
        circuit = QuantumCircuit(2, 2)

        # Add a H gate on qubit 0
        circuit.h(0)

        # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
        circuit.cx(0, 1)

        # Map the quantum measurement to the classical bits
        circuit.measure([0, 1], [0, 1])

        # Execute the circuit on the qasm simulator
        job = execute(circuit, simulator, shots=SHOTS)

        # Grab results from the job
        result = job.result()

        # Returns counts
        counts = result.get_counts(circuit)
        print("\nTotal count for 00 and 11 are:", counts)

        # Draw the circuit
        circuit.draw()

        plot_histogram(counts)
