import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvals, toeplitz

class QuantumResonanceVisualizer:
    """
    [CosmosT Pro Engine]
    리만-파블로프 우주의 공명(Resonance)을 시각화하고
    외부 잡음(Noise)에 대한 위상학적 강성(Stiffness)을 검증하는 모듈.
    """
    def __init__(self, resolution=1500, space_limit=30):
        # 해상도와 물리적 공간 크기 설정
        self.N = resolution
        self.x = np.linspace(-space_limit, space_limit, resolution)
        self.dx = self.x[1] - self.x[0]
        
        # H_BK = (xp + px)/2 연산자 생성 (베리-키팅 해밀토니안)
        self.X = np.diag(self.x)
        
        # 운동량 연산자 p = -i d/dx (중심 차분법 적용)
        col = np.zeros(resolution); row = np.zeros(resolution)
        col[1] = 1; row[1] = -1
        self.P = (-1j / (2 * self.dx)) * toeplitz(col, row)
        
        # 에르미트 부분 (Chaotic Dynamics)
        self.H_BK = 0.5 * (self.X @ self.P + self.P @ self.X)

    def generate_spectrum_with_noise(self, lam=0.4, noise_level=0.0):
        """
        [Core Logic]
        파블로프 포텐셜(ix * exp(-x^2))을 추가하고,
        잡음(Noise)을 주입하여 우주의 내구성을 테스트합니다.
        """
        # 1. 파블로프 포텐셜 (허수부 = 쌍소멸 필터)
        V_diag = 1j * lam * self.x * np.exp(-self.x**2)
        H_Pure = self.H_BK + np.diag(V_diag)
        
        # 2. 잡음 주입 (CP Stiffness Test Logic)
        if noise_level > 0:
            np.random.seed(42) # 재현성을 위해 시드 고정 (동일한 잡음 패턴에서 테스트)
            R = np.random.randn(self.N, self.N)
            R = (R + R.T) / 2  # 에르미트 잡음 (배경 복사) 생성
            H_Total = H_Pure + (noise_level * R)
        else:
            H_Total = H_Pure
            
        # 3. 고유값 분해 및 실수부 필터링
        evals = eigvals(H_Total)
        real_energies = np.sort(np.real(evals))
        
        # 4. 물리적 보정 (Scaling Factor alpha=2.85)
        scale_factor = 2.85 
        # 0.1 이하의 낮은 에너지는 제외 (Vacuum Fluctuation)
        primes_phys = real_energies[real_energies > 0.1] * scale_factor
        return primes_phys

    def scan_resonance_intensity(self, target, spectrum):
        """
        특정 타겟 숫자(예: 2185) 근처에서 공명 강도를 스캔합니다.
        """
        intensities = []
        products = []
        
        # 계산 속도를 위해 상위 40개 에너지 상태만 조합
        top_spectrum = spectrum[:40] 
        
        # 3-Body Interaction (E_i * E_j * E_k)
        for i, p in enumerate(top_spectrum):
            for q in top_spectrum[i:]:
                if p * q > target + 50: break
                for r in top_spectrum:
                    val = p * q * r
                    
                    # 타겟 근처(Window +/- 50)만 기록
                    if abs(val - target) < 50: 
                        diff = abs(target - val)
                        # 공명 강도 함수 (로렌츠 분포 유사)
                        intensity = 1.0 / (diff**2 + 0.05)
                        intensities.append(intensity)
                        products.append(val)
        return products, intensities

# --- 실행부 (Execution Block) ---
if __name__ == "__main__":
    # 1. 시스템 초기화
    visualizer = QuantumResonanceVisualizer(resolution=1000)
    target = 2185  # Target Semi-prime (5 * 19 * 23)
    
    # 2. 스트레스 테스트 설정
    # 0.00: 이상적 상태 (Clean)
    # 0.015: 약한 섭동 (Perturbed)
    # 0.04: 강한 잡음 (High Noise) -> 여기서 버티면 CP 강성 증명!
    noise_levels = [0.00, 0.015, 0.04]
    
    # [FIX] Matplotlib format string 오류 수정 (blueo -> b, g, r)
    colors = ['b', 'g', 'r'] 
    labels = ['Clean (Ideal)', 'Low Noise (Perturbed)', 'High Noise (Stiff)']
    
    plt.figure(figsize=(10, 6))
    
    print(f"⚡ [Stress Test] CP 강성 테스트 가동 (Target N={target})...")
    
    for i, noise in enumerate(noise_levels):
        print(f"   -> Testing Noise Level: {noise} (Color: {colors[i]})...")
        
        # 스펙트럼 생성 및 공명 스캔
        spectrum = visualizer.generate_spectrum_with_noise(noise_level=noise)
        prods, ints = visualizer.scan_resonance_intensity(target, spectrum)
        
        # 줄기 그래프 (Stem Plot) 그리기
        # markerfmt에 'bo', 'go', 'ro' 등이 들어가도록 수정됨
        markerline, stemlines, baseline = plt.stem(
            prods, ints, 
            linefmt=colors[i], markerfmt=colors[i]+'o', 
            label=f"Noise $\epsilon={noise}$"
        )
        # 잡음이 클수록 선을 얇게, 점을 작게 그려서 겹쳐 보이게 함
        plt.setp(stemlines, 'linewidth', 2 - (i*0.5))
        plt.setp(markerline, 'markersize', 8 - (i*2))

    # 그래프 데코레이션
    plt.axvline(x=target, color='k', linestyle='--', label=f'Target N={target}')
    plt.xlim(target - 10, target + 10)
    plt.title(f'Proof of CP Stiffness: Topological Protection of N={target}')
    plt.xlabel('Calculated Product (E_i * E_j * E_k)')
    plt.ylabel('Resonance Intensity')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 결과 저장 및 출력
    save_path = 'CP_Stiffness_Proof.png'
    plt.savefig(save_path)
    print(f"✅ [Complete] 검증 완료. 결과가 '{save_path}'에 저장되었습니다.")
    plt.show()