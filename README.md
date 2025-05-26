# Quantum Feedback Simulator

A Qiskit-based simulation of quantum systems with feedback mechanisms, visualizing qubit states on the Bloch sphere after multiple feedback iterations.

![Sample Output](docs/sample_output.png)

## Features
- Simulates quantum feedback loops with configurable iterations
- Visualizes qubit states on Bloch spheres
- Provides detailed quantum state interpretations
- Supports both pure and mixed states

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quantum-feedback-simulator.git
   cd quantum-feedback-simulator
   Install dependencies:

bash
pip install -r src/requirements.txt
Usage
Run the simulation:

bash
python src/quantum_feedback.py
When prompted, enter the number of feedback iterations (1-10).

Output Interpretation
The program displays:

Bloch sphere visualizations for each qubit

Probabilities of |0⟩ and |1⟩ states

X, Y, Z components of the Bloch vector

Purity measurement (0.5 for maximally mixed states)

State classification (Pure/Mixed)