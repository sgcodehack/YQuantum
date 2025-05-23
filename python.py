from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import RYGate, RZGate, CXGate, CZGate, CRYGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import Counter

# Helper function to convert bitstring to rotation angle
def bitstring_to_angle(bitstring):
    return (np.pi * int(bitstring, 2)) / (2 ** len(bitstring))

# Superquantum Hash Function
def superquantum_hash(input_bits, k=2):
    n = len(input_bits) // k
    blocks = [input_bits[i*k:(i+1)*k] for i in range(n)]
    qc = QuantumCircuit(n, n)

    # Encoding
    for i in range(n):
        theta = bitstring_to_angle(blocks[i])
        qc.ry(theta, i)

    # Local entanglement
    for i in range(n - 1):
        qc.cx(i, i + 1)

    # Non-local entanglement
    for i in range(n - 2):
        qc.cz(i, i + 2)
        qc.cry(np.pi / 2, i, i + 2)

    # Phase Encoding
    for i in range(n):
        phi = bitstring_to_angle(blocks[i])
        qc.rz(phi, i)

    # Measurement
    qc.measure(range(n), range(n))
    
    backend = AerSimulator()
    result = backend.run(qc, shots = 1).result()
    counts = result.get_counts(qc)
    return list(counts.keys())[0]

# Uniformity Testing
def test_uniformity(samples=1000, input_len=8):
    outputs = []
    for _ in range(samples):
        rand_input = ''.join(np.random.choice(['0','1'], size=input_len))
        out = superquantum_hash(rand_input)
        outputs.append(out)
    freq = dict(Counter(outputs))
    plot_histogram(freq)
    plt.title("Output Distribution - Uniformity Test")
    plt.show()
    return freq

# Avalanche Effect Testing
def test_avalanche_effect(base_input):
    base_hash = superquantum_hash(base_input)
    diffs = []
    for i in range(len(base_input)):
        flipped = list(base_input)
        flipped[i] = '1' if base_input[i] == '0' else '0'
        flipped_input = ''.join(flipped)
        new_hash = superquantum_hash(flipped_input)
        # Hamming distance
        diff = sum([1 for a, b in zip(base_hash, new_hash) if a != b])
        diffs.append(diff)
    plt.plot(diffs)
    plt.title("Avalanche Effect: Bit Flip Impact")
    plt.xlabel("Bit Flipped")
    plt.ylabel("Hamming Distance")
    plt.show()
    return diffs

# Timing Benchmark
def benchmark_timing(samples=100, input_len=8):
    times = []
    for _ in range(samples):
        input_bits = ''.join(np.random.choice(['0','1'], size=input_len))
        start = time.time()
        _ = superquantum_hash(input_bits)
        end = time.time()
        times.append(end - start)
    print(f"Average Time per Hash: {np.mean(times)*1000:.3f} ms")
    plt.hist(times, bins=20)
    plt.title("Timing Distribution")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency")
    plt.show()

# Example Demonstration
if __name__ == '__main__':
    print("Example Hash Output for input '11001010':")
    print(superquantum_hash('11001010'))

    print("\n--- Uniformity Test ---")
    test_uniformity(samples=200)

    print("\n--- Avalanche Effect Test ---")
    test_avalanche_effect(list('11001010'))

    print("\n--- Timing Benchmark ---")
    benchmark_timing(samples=50)
