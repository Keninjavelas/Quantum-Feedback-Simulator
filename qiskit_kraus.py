from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Kraus, DensityMatrix, partial_trace, purity
from qiskit.visualization import plot_bloch_vector
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_reset_kraus(gamma=0.1):
    """Generate Kraus operators for amplitude damping channel"""
    K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]])
    K1 = np.array([[0, np.sqrt(gamma)], [0, 0]])
    return Kraus([K0, K1])

def get_user_input():
    """Get and validate user input for number of iterations"""
    while True:
        try:
            n = int(input("Enter number of iterations (rounds of feedback, 1-10): "))
            if 1 <= n <= 10:
                return n
            print("Please enter a value between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def build_circuit(n_iterations):
    """Build the quantum circuit with feedback mechanism"""
    qc = QuantumCircuit(3)  # Qubits: 0,1 = system, 2 = ancilla
    
    # Initial state preparation
    qc.h([0, 1])  # Create superposition
    qc.reset(2)    # Initialize ancilla to |0⟩
    
    # Feedback loop
    for _ in range(n_iterations):
        # Random measurement outcome (simulated)
        y = np.random.choice([0, 1])
        
        # Apply feedback operations
        if y == 0:
            qc.cx(0, 2)  # CNOT system qubit 0 to ancilla
            qc.h(1)      # Hadamard on qubit 1
        else:
            qc.cx(1, 2)  # CNOT system qubit 1 to ancilla
            qc.rx(np.pi, 0)  # X-rotation on qubit 0
        
        # Apply noisy reset to ancilla
        reset_kraus = get_reset_kraus().to_instruction()
        qc.append(reset_kraus, [2])
    
    return qc

def calculate_bloch_vector(dm):
    """Calculate Bloch vector components for a density matrix"""
    # Pauli matrices
    sigma_x = np.array([[0, 1], [1, 0]])
    sigma_y = np.array([[0, -1j], [1j, 0]])
    sigma_z = np.array([[1, 0], [0, -1]])
    
    # Calculate expectation values
    x = np.real(np.trace(np.dot(dm, sigma_x)))
    y = np.real(np.trace(np.dot(dm, sigma_y)))
    z = np.real(np.trace(np.dot(dm, sigma_z)))
    
    return [x, y, z]

def interpret_qubit(dm, index):
    """Generate interpretation of qubit state"""
    probs = np.diag(dm.data.real)  # Get diagonal elements for probabilities
    p = purity(dm)
    bloch_vector = calculate_bloch_vector(dm)
    
    return {
        'bloch_vector': bloch_vector,
        'interpretation': (
            f"Qubit {index} Interpretation:\n"
            f"  • Prob(|0⟩) ≈ {probs[0]:.2f}\n"
            f"  • Prob(|1⟩) ≈ {probs[1]:.2f}\n"
            f"  • X-component: {bloch_vector[0]:.2f}\n"
            f"  • Y-component: {bloch_vector[1]:.2f}\n"
            f"  • Z-component: {bloch_vector[2]:.2f}\n"
            f"  • Purity: {p:.2f}\n"
            f"  • Nature: {'Pure' if np.isclose(p, 1.0, atol=0.05) else 'Mixed'}"
        )
    }

def visualize_results(results, n_iterations):
    """Create visualization of the results"""
    fig = plt.figure(figsize=(14, 6))
    
    for i, result in enumerate(results):
        ax = fig.add_subplot(1, 2, i+1, projection='3d')
        plot_bloch_vector(result['bloch_vector'], ax=ax)
        ax.set_title(f"Qubit {i} Bloch Sphere")
        ax.text2D(0.5, -0.15, result['interpretation'],
                 transform=ax.transAxes,
                 fontsize=9, ha='center', va='top',
                 bbox=dict(facecolor='white', alpha=0.8))
    
    plt.suptitle(f"Quantum State After {n_iterations} Feedback Iteration(s)", fontsize=14)
    plt.tight_layout()
    plt.show()

def main():
    n = get_user_input()
    qc = build_circuit(n)
    qc.save_density_matrix()
    
    sim = Aer.get_backend('aer_simulator_density_matrix')
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    final_rho = result.data()['density_matrix']
    
    # Trace out ancilla and analyze system qubits
    system_rho = partial_trace(final_rho, [2])
    qubit0_rho = partial_trace(system_rho, [1])
    qubit1_rho = partial_trace(system_rho, [0])
    
    results = [
        interpret_qubit(qubit0_rho, 0),
        interpret_qubit(qubit1_rho, 1)
    ]
    
    visualize_results(results, n)

if __name__ == "__main__":
    np.random.seed(42)  # For reproducible results
    main()