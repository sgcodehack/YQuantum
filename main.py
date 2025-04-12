from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Statevector
import numpy as np

def qhash(b: bytes):
    #create circuit
    k = len(b)
    qc = QuantumCircuit(k)
    
    #rotate qubits
    for i in range(k):
        theta = (b[i] / 255) * np.pi  #scale to [0, π]
        qc.ry(theta, i)
    
    #entangle qubits
    #layer 1: entangle every adjacent qubit
    for i in range(0, k - 1):
        qc.cx(i, i + 1, )
    
    #layer 2: vary theta
    for i in range(0, k - 1, 2):
        phi = theta = (b[i] / 255) * np.pi
        qc.cry(phi, i, i + 1)
    
    #layer 3: change phase
    for i in range(0, k - 1, 3):
        qc.cz(i, i + 1)

    #measure
    sv = Statevector.from_instruction(qc)
    expectation = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(k)]
    
    output = bytearray([min(int(((val + 1) / 2) * 256), 255) for val in expectation])
    
    return output
    

def main():
    print(list(qhash(bytes(range(0, 260, 20)))))

if __name__ == "__main__":
    main()