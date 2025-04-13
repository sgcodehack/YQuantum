import time
import random
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Pauli, Statevector
from qiskit_aer import AerSimulator
import numpy as np

MAX_QUBITS = 20

def qhash(b: bytes, single_shot = False):
    # create circuit
    flag = False
    num_qubits = min(len(b) // 2, MAX_QUBITS) # 2 bytes = 1 qubit
    
    if len(b) < MAX_QUBITS: # if there are less bytes than maximum qubits, no need to reduce number of qubits
        flag = True
        num_qubits = len(b)
    
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # rotate qubits -> superposition
    for i in range(0, num_qubits):
        curr = 0
        if flag:
            curr = b[i]
        else:
            curr = b[2 * i]
        
        phi = (curr / 255) * np.pi  # scale to [0, π]
        qc.ry(phi, i)
    
    # entangle qubits
    # layer 1: entangle every adjacent qubit
    for i in range(0, num_qubits - 1):
        qc.cx(i, i + 1)
    
    # layer 2: encode phase
    for i in range(0, num_qubits - 1, 2):
        curr = 0
        if flag:
            curr = b[i]
        else:
            curr = b[2 * i]
        
        phi = (curr / 255) * np.pi
        qc.crz(phi, i, i + 1)
    
    # layer 3: encode amplitude
    for i in range(0, num_qubits):
        for j in range(0, num_qubits):
            if j != i and j != i - 1 and j != i + 1:
                phi = np.pi / 2
                qc.cry(phi, i, j)
                
    qc.append(QFT(num_qubits = num_qubits, do_swaps = False), qc.qubits)

    # create output
    output = 0
    
    if single_shot: # blockchain
        qc.measure(range(num_qubits), range(num_qubits))
        
        sim = AerSimulator()
        
        compiled = transpile(qc, sim)
        
        result = sim.run(compiled, shots = 1).result()
        counts = result.get_counts()
        
        output = list(counts.keys())[0]
    else: # password
        sv = Statevector.from_instruction(qc)
        
        probs = np.abs(sv.data) ** 2
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        
        expectation = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(num_qubits)]
        output = list([min(int(((val + 1) / 2) * 256), 255) for val in expectation]) # scales up from -1 to 1 to 0 to 255
    
    pass
    
    return [output, entropy]

def test(cases, lower, upper):
    collisions = []
    hash_book = {}
    
    total = 0

    for length in range(lower, upper + 1):
        for _ in range(cases):
            input = random.getrandbits(length * 8).to_bytes(length, byteorder='big')
            
            start = time.time()
            hash = tuple(qhash(input)[0])
            end = time.time()
            
            total += end - start
            
            if hash in hash_book and input != hash_book[hash]:
                collisions.append(input)
            
            hash_book[hash] = input
    
    return [collisions, total / ((upper + 1 - lower) * cases)]

def main():
    while(True):
        
        choice = input("Test or find entropy?(t/e): ")
        
        if choice == 't':
            cases = int(input("Number of test cases: "))
            print("Please enter your bounds for the number of bytes. Limited from 1 to 32.")
            lower = int(input("Lower bound on number of bytes: "))
            upper = int(input("Upper bound on the number of bytes: "))
            collisions, avg = test(cases, lower, upper)
        
            print("avg time: ", avg, "\namount of collisions: ", len(collisions), "\ncollisions(input string in hexadecimal): ")
            
            for i in range(len(collisions)):
                print(collisions[i].hex())
                
            break
        elif choice == 'e':
            length = int(input("Enter the amount of bytes(1 - 32): "))
            bytestring = random.getrandbits(length * 8).to_bytes(length, byteorder='big')
            
            print("hexadecimal representation of input: ", bytestring.hex())
            print("entropy: ", qhash(bytestring)[1])
            
            break
        else:
            print("Not a correct choice")
   
if __name__ == "__main__":
   main()