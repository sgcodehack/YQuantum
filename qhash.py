import math
import random
from qiskit import QuantumCircuit, transpile
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

   # create output
   output = 0
  
   if single_shot: # blockchain
       qc.measure(range(num_qubits), range(num_qubits))
      
       sim = AerSimulator()
      
       compiled = transpile(qc, sim)
      
       result = sim.run(compiled, shots = 1).result()
       counts = result.get_counts()
      
       output = list(counts.keys())[0]
   els