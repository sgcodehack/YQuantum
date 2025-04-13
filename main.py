import time
import random
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Pauli, Statevector
from qiskit_aer import AerSimulator
import numpy as np

NUM_QUBITS = 16

def qhash(b: bytes, single_shot = False):
    # create circuit
    
    k = len(b)
    
    for i in range(k, NUM_QUBITS * 2):
        b += bytes([0x00])
    
    qc = QuantumCircuit(NUM_QUBITS, NUM_QUBITS)
    
    # rotate qubits -> superposition
    for i in range(0, NUM_QUBITS):
        phi = (b[2 * i] / 255) * np.pi  # scale to [0, π]
        qc.ry(phi, i)
    
    # entangle qubits
    # layer 1: entangle every adjacent qubit
    for i in range(0, NUM_QUBITS - 1):
        qc.cx(i, i + 1)
    
    # layer 2: encode phase
    for i in range(0, NUM_QUBITS - 1, 2):
        phi = (b[2 * i] / 255) * np.pi
        qc.crz(phi, i, i + 1)
    
    # layer 3: encode amplitude
    for i in range(0, NUM_QUBITS):
        for j in range(0, NUM_QUBITS):
            if j != i and j != i - 1 and j != i + 1:
                phi = np.pi / 2
                qc.cry(phi, i, j)


    #quantum fourier transform to increase the avalanche effect
    qc.append(QFT(num_qubits = NUM_QUBITS, do_swaps = False), qc.qubits)


    # create output
    output = ""
    
    sv = Statevector.from_instruction(qc)
        
    probs = np.abs(sv.data) ** 2
    entropy = -np.sum(probs * np.log2(probs + 1e-10))
    
    if single_shot: # blockchain
        qc.measure(range(NUM_QUBITS), range(NUM_QUBITS))
        
        sim = AerSimulator()
        
        compiled = transpile(qc, sim)
        
        result = sim.run(compiled, shots = 1).result()
        counts = result.get_counts()
        
        list_output = list(counts.keys())[0]
        
        #256 bit string conversion
        for i in list_output:
            output += i
            
        for _ in range(240):
            output += '0'
            
    else: # password
        expectation = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(NUM_QUBITS)]
        list_output = list([min(int(((val + 1) / 2) * 256), 255) for val in expectation]) # scales up from -1 to 1 to 0 to 255
        
        #256 bit string conversion
        for i in list_output:
            output += format(i, '08b')
        for _ in list_output:
            output += format(0, '08b')
    
    pass
    
    return [output, entropy / NUM_QUBITS]


def test(cases, lower, upper):
    collisions = []
    hash_book = {}
    
    total = 0
    normalized_entropy = 0


    for length in range(lower, upper + 1):
        for _ in range(cases):
            input = random.getrandbits(length * 8).to_bytes(length, byteorder='big')
            
            start = time.time()
            output, curr_entropy_ratio = qhash(input)
            end = time.time()
            
            total += end - start
            
            hash = tuple(output)
            normalized_entropy += curr_entropy_ratio
            
            if hash in hash_book and input != hash_book[hash]:
                collisions.append(input)
            
            hash_book[hash] = input
    
    return [collisions, total / ((upper + 1 - lower) * cases), normalized_entropy / ((upper + 1 - lower) * cases)]

def main():
    # cases = int(input("Number of test cases: "))
    # print("Please enter your bounds for the number of bytes. Limited from 1 to 32.")
    # lower = int(input("Lower bound on number of bytes: "))
    # upper = int(input("Upper bound on the number of bytes: "))
    # collisions, avg_time, avg_normalized_entropy = test(cases, lower, upper)

    # print("avg time: ", avg_time, "\navg normalized_entropy: ", avg_normalized_entropy, "\namount of collisions: ", len(collisions), "\ncollisions(input string in hexadecimal): ")
    
    # for i in range(len(collisions)):
    #     print(collisions[i].hex())
    
    length = 32 # can be any number from 1 to 32
    print(qhash(random.getrandbits(length * 8).to_bytes(length, byteorder='big'))[0])
 
if __name__ == "__main__":
  main()