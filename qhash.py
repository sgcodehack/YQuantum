from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Pauli, Statevector
from qiskit_aer import AerSimulator
import numpy as np

def qhash(b: bytes, single_shot):
    #create circuit
    k = len(b)
    qc = QuantumCircuit(k, k)
    
    #rotate qubits -> superposition
    for i in range(k):
        theta = (b[i] / 255) * np.pi  #scale to [0, π]
        qc.ry(theta, i)
    
    #entangle qubits
    #layer 1: entangle every adjacent qubit
    for i in range(0, k - 1):
        qc.cx(i, i + 1)
    
    #layer 2: encode phase
    for i in range(0, k - 1, 2):
        qc.cz(i, i + 1)
    
    #layer 3: encode amplitude
    for i in range(0, k):
        for j in range(0, k):
            if j != i and j != i - 1 and j != i + 1:
                phi = np.pi / 2
                qc.cry(phi, i, j)


    #create output
    output = 0
    
    if single_shot: #blockchain
        qc.measure(range(k), range(k))
        
        sim = AerSimulator()
        
        compiled = transpile(qc, sim)
        
        result = sim.run(compiled, shots = 1).result()
        counts = result.get_counts()
        
        output = list(counts.keys())[0]
    else: #password
        sv = Statevector.from_instruction(qc)
        
        expectation = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(k)]
        output = list([min(int(((val + 1) / 2) * 256), 255) for val in expectation]) # scales up from -1 to 1 to 0 to 255
    
    return output

def main():
    print(qhash(bytes(range(0, 260, 20)), single_shot = False))

if __name__ == "__main__":
    main()
