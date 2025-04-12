# YQuantum, Superquantum Challenge
📝 Description of the challenge: Develop quantum-enhanced hash functions for applications in blockchain and cryptocurrencies.

# 🔐 Superquantum Hash — A Native Quantum Hashing Scheme for Crypto

This project implements a **quantum-native hash function** designed for future-proof applications in blockchain and cryptography. Unlike post-quantum approaches that attempt to retrofit classical primitives, this algorithm is fully built on the principles of quantum computing: **superposition, entanglement, phase evolution**, and **measurement collapse**.

The system generates a **deterministic, irreversible, and input-sensitive fingerprint**, derived entirely from quantum circuit behavior.

---
## 🧠 Overview

Hash functions are central to cryptographic systems, including block headers in Bitcoin, Merkle trees, commitments, and digital signatures. They require:

- Determinism
- Avalanche effect (small change → large output change)
- Resistance to inversion and collision
- Compact representation

This project explores how a quantum system, via circuit-level encoding and controlled entanglement, can naturally express these properties — without relying on classical assumptions.

---
## 📐 Quantum Hash Function – Mathematical Description

Let the classical input be \( x \in \{0,1\}^{n \cdot k} \), which is partitioned into \( n \) blocks of \( k \) bits.
![formula](./imgs/theta_formula.png)
