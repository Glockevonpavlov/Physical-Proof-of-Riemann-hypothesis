import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig

def visualize_pt_symmetry():
    print("⚛️ [Quantum Core] Generating Bifurcation Graph...")
    
    E0 = 10.0
    V = 5.0
    lambdas = np.linspace(0, 10, 100)
    
    real_parts = []
    imag_parts = []
    
    for lam in lambdas:
        H = np.array([[E0 + 1j * lam, V], [V, E0 - 1j * lam]])
        evals, _ = eig(H)
        evals = np.sort(evals)
        real_parts.append(evals.real)
        imag_parts.append(evals.imag)
        
    real_parts = np.array(real_parts)
    imag_parts = np.array(imag_parts)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Real Part
    ax1.plot(lambdas, real_parts[:, 0], 'b-', label='Energy 1')
    ax1.plot(lambdas, real_parts[:, 1], 'r-', label='Energy 2')
    ax1.axvline(x=V, color='k', linestyle='--', label='Exceptional Point')
    ax1.set_ylabel('Real Energy')
    ax1.set_title('PT-Symmetry Phase Transition (Bifurcation)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.text(1, E0, "Unbroken Phase\n(Real)", ha='center')
    ax1.text(8, E0, "Broken Phase\n(Complex)", ha='center')

    # Imaginary Part
    ax2.plot(lambdas, imag_parts[:, 0], 'b--')
    ax2.plot(lambdas, imag_parts[:, 1], 'r--')
    ax2.axvline(x=V, color='k', linestyle='--')
    ax2.set_ylabel('Imaginary Energy')
    ax2.set_xlabel('Coupling Strength (lambda)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("bifurcation_graph.png", dpi=300)
    print("✅ 'bifurcation_graph.png' saved.")

if __name__ == "__main__":
    visualize_pt_symmetry()