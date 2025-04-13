import math
import random
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Pauli, Statevector
from qiskit_aer import AerSimulator
import numpy as np

MAX_QUBITS = 20

def qhash(b: bytes, single_shot = False):
   # create circuit
   num_qubits = min(len(b) // 2, MAX_QUBITS)
  
   qc = QuantumCircuit(num_qubits, num_qubits)
  
   # rotate qubits -> superposition
   for i in range(0, num_qubits):
       phi = (b[2 * i] / 255) * np.pi  # scale to [0, π]
       qc.ry(phi, i)
  
   # entangle qubits
   # layer 1: entangle every adjacent qubit
   for i in range(0, num_qubits - 1):
       qc.cx(i, i + 1)
  
   # layer 2: encode phase
   for i in range(0, num_qubits - 1, 2):
       phi = (b[2 * i] / 255) * np.pi
       qc.crz(phi, i, i + 1)
  
   # layer 3: encode amplitude
   for i in range(0, num_qubits):
       for j in range(0, num_qubits):
           if j != i and j != i - 1 and j != i + 1:
               phi = np.pi / 2
               qc.cry(phi, i, j)

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
      
       expectation = [sv.expectation_value(Pauli("Z"), [i]).real for i in range(num_qubits)]
       output = list([min(int(((val + 1) / 2) * 256), 255) for val in expectation]) # scales up from -1 to 1 to 0 to 255
  
   return output

def test(cases):
    collisions = []
    hash_book = {}

    for length in range(1, 10):
        for reps in range(cases):
            input = random.getrandbits(length * 8).to_bytes(length, byteorder='big')
            hash = tuple(qhash(input))
            
            if hash in hash_book and input != hash_book[hash]:
                collisions.append(input)
                
            
            hash_book[hash] = input
    
    return collisions

def main():
   collisions = test(50)
   
   print(len(collisions))
   for i in range(len(collisions)):
       print(collisions[i].hex())
   
   


if __name__ == "__main__":
   main()