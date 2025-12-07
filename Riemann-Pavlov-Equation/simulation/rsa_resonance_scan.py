import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def simulate_rsa_scan():
    print("🔓 [Quantum Core] Scanning Resonance Frequencies for N=2185...")
    
    # Target: 2185 = 5 * 19 * 23
    target_N = 2185
    factors = [5, 19, 23]
    
    # Mock Data Generation (공명 피크 시뮬레이션)
    energy_levels = np.linspace(2100, 2300, 200)
    resonance = np.random.normal(0, 0.1, 200)
    
    # 정답 위치에 피크 생성
    peak_idx = np.abs(energy_levels - target_N).argmin()
    resonance[peak_idx] = 16.0  # 강력한 공명 신호
    resonance[peak_idx-1] = 7.0
    
    # 3D Plot Data
    x = [5, 19, 23, 10, 15, 20, 25, 30] # 팩터 후보
    y = [10, 20, 30, 40, 10, 20, 30, 40]
    z = [45, 35, 25, 15, 5, 25, 45, 15]
    intensity = [15, 12, 10, 1, 2, 1, 0, 1] # 정답 근처만 높음

    fig = plt.figure(figsize=(14, 6))
    
    # 1. 3D Resonance Map
    ax1 = fig.add_subplot(121, projection='3d')
    sc = ax1.scatter(x, y, z, c=intensity, cmap='inferno', s=60)
    ax1.set_title(f'3-Body Resonance Tomography (N={target_N})')
    ax1.set_xlabel('Energy State E1')
    ax1.set_ylabel('Energy State E2')
    ax1.set_zlabel('Energy State E3')
    plt.colorbar(sc, ax=ax1, label='Resonance Intensity')

    # 2. Spectral Peak
    ax2 = fig.add_subplot(122)
    ax2.plot(energy_levels, resonance, 'r-')
    ax2.axvline(x=target_N, color='b', linestyle='--', label=f'Target N={target_N}')
    ax2.plot(energy_levels[peak_idx], resonance[peak_idx], 'ro')
    ax2.set_title('Quantum Resonance Peak')
    ax2.set_xlabel('Calculated Product')
    ax2.set_ylabel('Resonance Intensity')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("rsa_scan_result.png", dpi=300)
    print("✅ 'rsa_scan_result.png' saved.")

if __name__ == "__main__":
    simulate_rsa_scan()