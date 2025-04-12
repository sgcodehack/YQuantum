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


Let the classical input $$\( x \in \{0,1\}^{n \cdot k} \)$$ be divided into $$n$$ blocks of $$k$$ bits.


### 1. Encoding via Parametric Superposition

Each input block $$\( x^{(i)} \)$$ is mapped to a rotation angle:

$$
\theta_i = \pi \cdot \frac{\text{int}(x^{(i)})}{2^k}
$$

This angle defines the single-qubit rotation around the Y-axis:

$$
R_y(\theta_i) =
\begin{bmatrix}
\cos\left(\frac{\theta_i}{2}\right) & -\sin\left(\frac{\theta_i}{2}\right) \\
\sin\left(\frac{\theta_i}{2}\right) & \cos\left(\frac{\theta_i}{2}\right)
\end{bmatrix}
$$

The gate is applied to the initial qubit state $$\( |0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix} \)\$$, resulting in:

$$
\[
|\psi_i\rangle = R_y(\theta_i) |0\rangle =
\cos\left(\frac{\theta_i}{2}\right)|0\rangle + \sin\left(\frac{\theta_i}{2}\right)|1\rangle
\]
$$

Each qubit is now in a superposition dependent on its corresponding input block.

To build the full quantum state, we apply this to all qubits and take the tensor product:

$$
|\Psi_1\rangle = |\psi_1\rangle \otimes |\psi_2\rangle \otimes \cdots \otimes |\psi_n\rangle
$$

This creates a global superposition that encodes the classical input \( x \) in the quantum amplitudes of the system.
--- 

### 2. Entanglement Dynamics

We apply a set of two-qubit gates:

- $$\( \text{CNOT}(i,i+1) \)$$: propagates influence linearly
- $$\( \text{CZ}(i,i+2) \)$$: introduces interference-sensitive control
- $$\( \text{CRY}(\theta_{ij}) \)$$: conditional rotation with input-dependent parameters

#### Entanglement Operator
### **Entanglement Operator Structure**

The entanglement operator $$\( U_{\text{ent}} \)$$ is constructed using a **layered approach** designed to rapidly build complex correlations and simulate chaotic dynamics:

#### **Layer 1: Local Entanglement**
- Nearest-neighbor entanglement is applied using $$\( \text{CNOT}(i, i+1) \)$$ gates arranged in a **linear** or **ladder pattern** across the qubits.
- This ensures that information propagates efficiently between adjacent qubits and establishes local correlations.

#### **Layer 2: Non-Local Entanglement**
- To introduce **longer-range correlations** crucial for pseudo-random behavior, non-local controlled gates are applied:
  - **Controlled-Z Gates $$(\( \text{CZ}(i, i+2) \))$$**: Connect qubits $$\( i \)$$ and $$\( i+2 \)$$, introducing **phase-based interference** that depends on the states of non-adjacent qubits.
  - **Controlled-Rotation-Y Gates $$(\( \text{CRY}(\theta') \))$$**: Optionally, $$\( \text{CRY} \)$$ gates connecting non-adjacent qubits can be used to add additional conditional rotations. For simplicity, a fixed angle $$\( \theta' = \frac{\pi}{2} \)$$ can be chosen to ensure consistent dynamics without external classical dependencies.

#### **Layered Structure**
- This **combination of local and non-local interactions** ensures that changes in any input qubit rapidly influence the entire quantum state.
- The overall operator can be expressed as:

$$
U_{\text{ent}} = U_{\text{non-local}} \cdot U_{\text{local}}
$$
The entanglement operator is defined as:
$$
U_{\text{ent}} = \prod_{(i,j)} G_{ij}, \quad G_{ij} \in \{\text{CNOT}, \text{CZ}, \text{CRY}(\theta)\}
$$

#### State After Entanglement

After applying the entanglement operator, the quantum state becomes:

$$
|\Psi_2\rangle = U_{\text{ent}} |\Psi_1\rangle
$$

This step ensures that **any change in the input \( x \) causes a global deformation** of the quantum state — modeling the avalanche effect naturally.

(Note: The exact sequence and repetition of these layers would depend on specific implementation parameters, which can be tuned for desired cryptographic strength.)

---

### 3. Phase Encoding

We rotate each qubit on the Z-axis using:

$$\[
\phi_i = \pi \cdot \frac{\text{int}(x^{(i)})}{2^k}
\]$$

$$\[
R_z(\phi_i) = 
\begin{bmatrix}
e^{-i\phi_i/2} & 0 \\
0 & e^{i\phi_i/2}
\end{bmatrix}
\]$$

$$\[
|\Psi_3\rangle = \left( \bigotimes_{i=1}^{n} R_z(\phi_i) \right) |\Psi_2\rangle
\]$$

### Justification for Reusing Angles

We intentionally reuse the same angle mapping:

$$
\phi_i = \theta_i
$$

#### Applying the Rotation on the Z-Axis vs Y-Axis

This choice simplifies implementation and directly reinforces the input encoding within the **phase component** of the qubits. While seemingly straightforward, the key insight lies in applying the same input-dependent rotation on a **different axis**:

- **Y-axis Rotation**: Encodes amplitudes via $$\( R_y(\theta_i) \)$$.
- **Z-axis Rotation**: Encodes phases via $$\( R_z(\phi_i) \)$$.

When applied to an already entangled state $$\( |\Psi_2\rangle \)$$, this dual-axis approach contributes significantly to the **complexity of the final state's interference pattern**, enhancing unpredictability based on the input parameters.

---
### 4. Measurement & Single-Shot Hash Output

The final quantum state $$\( |\Psi_3\rangle \)$$, which intricately encodes the input $$\( x \)$$ through amplitude and phase relationships, is measured **once** in the computational basis.

#### Classical Bit String from Measurement

Let $$\( z \in \{0,1\}^n \)$$ represent the specific classical bit string obtained from this **single round of measurement** across all $$\( n \)$$ qubits. This measurement collapses the quantum state to a deterministic classical outcome for that computation.

#### Superquantum Hash Definition

The Superquantum Hash $$\( H(x) \)$$ is defined as:

$$
H(x) = z \quad \text{(Result of a single measurement round)}
$$

This definition ensures that the hash output is **deterministic per execution instance**:

- **Determinism**: For any specific computational instance, the measured bitstring $$\( z \)$$ represents a unique and fixed result.
- **Quantum Probabilism**: While repeated, independent runs of the process on the same input $$\( x \)$$ may yield different outcomes \( z' \) due to quantum probabilistic behavior, \( H(x) \) refers **only** to the result $$\( z \)$$ from the original computation.

#### Functional Determinism for Verification

In systems like blockchain, this deterministic behavior is critical. The validity check for $$\( H(x) \)$$ refers to the specific $$\( z \)$$ obtained during the original computation, ensuring a **fixed reference** for verification protocols.

#### Irreversibility from Measurement Collapse

The inherent irreversibility of the Superquantum Hash arises directly from the quantum measurement collapse, which destroys the original quantum state $$\( |\Psi_3\rangle \)$$. This fundamental property ensures that reversing $$\( H(x) \)$$ to retrieve the original input $$\( x \)$$ is computationally infeasible, providing cryptographic strength.

---

This approach leverages quantum mechanics to achieve a unique combination of **determinism, irreversibility, and probabilistic unpredictability**, making it suitable for secure applications in blockchain and cryptography.
---

## 🔗 Applications in Blockchain & Cryptocurrency

This design can be directly applied in multiple contexts:

- **Block Header Fingerprints**: Instead of using SHA-256 in Bitcoin, a quantum miner could propose a block whose header is hashed by this function. The hash could be verified with SWAP-tests against its quantum description.
- **qProof of Work (qPoW)**: Difficulty could be redefined via properties of the output state — e.g., entropy, fidelity with a reference state, or energy of the collapsed string.
- **Quantum-Commitments**: A user can commit to data \( x \) by generating and sending the hash \( H(x) \), while the pre-image remains unrecoverable without full system reconstruction.

---

## ⚙️ Circuit-Level Summary

This algorithm is implemented using:

- **Ry** gates for encoding classical bits as qubit rotations
- **CNOT** and **CZ** for entangling neighbors and non-neighbors
- **CRY(θ)** for conditional amplitude modulation
- **Rz(φ)** for individual phase shifts derived from input
- **Measurement** for collapse to classical bitstrings

All components are compatible with current Qiskit simulators and IBM Q devices.  
The circuit scales efficiently with input size and uses no exotic gates beyond the NISQ standard.

