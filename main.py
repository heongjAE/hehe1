import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 앱 제목 및 설명 ---
st.title("✨ 중력 마이크로렌징 시뮬레이터")
st.write("""
    이 앱은 **중력 마이크로렌징** 현상으로 인한 광원 별의 밝기 변화를 시뮬레이션합니다.
    전경의 렌즈 별과 행성이 배경 별의 빛을 휘게 하여 밝기가 일시적으로 증가하는 현상입니다.
    아래 설정을 변경하여 밝기 곡선이 어떻게 변하는지 확인해 보세요!
""")

st.write("---")

# --- 2. 시뮬레이션 설정 입력 받기 ---
st.sidebar.header("설정")

# 광원 별 설정
st.sidebar.subheader("광원 별 (Source Star)")
source_mass = st.sidebar.number_input("질량 (태양 질량)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# 렌즈 별 설정
st.sidebar.subheader("렌즈 별 (Lens Star)")
lens_mass = st.sidebar.number_input("질량 (태양 질량)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
lens_velocity = st.sidebar.slider("상대 속도 (km/s)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
impact_parameter = st.sidebar.slider("충격 매개변수 (Einstein Radius 단위)", min_value=0.0, max_value=2.0, value=0.5, step=0.05)


# 행성 설정 (선택 사항)
st.sidebar.subheader("행성 (Planet - 선택 사항)")
has_planet = st.sidebar.checkbox("행성 포함", value=False)
if has_planet:
    planet_mass_ratio = st.sidebar.slider("행성 질량비 (렌즈 별 질량 대비)", min_value=0.0001, max_value=0.1, value=0.001, format="%.4f")
    planet_orbit_radius = st.sidebar.slider("행성 궤도 반지름 (Einstein Radius 단위)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)
    planet_phase = st.sidebar.slider("행성 초기 위상 (도)", min_value=0, max_value=360, value=0, step=10)
else:
    planet_mass_ratio = 0
    planet_orbit_radius = 0
    planet_phase = 0

st.sidebar.write("---")
st.sidebar.info("참고: 이 시뮬레이터의 밝기 곡선은 개념적인 모델에 기반하며, 실제 천체 물리 계산과 다를 수 있습니다.")

# --- 3. 시뮬레이션 로직 (가상 모델) ---

# 시간 축 (일)
time_points = np.linspace(-15, 15, 300) # -15일에서 +15일까지 300개 지점

# 가상 밝기 계산 함수 (실제 마이크로렌징 수식 아님)
# 실제 마이크로렌징은 복잡한 렌즈 방정식을 풀어야 합니다.
def calculate_magnification(t, lens_m, planet_m_ratio, planet_orb, phase, velocity, impact_param, has_p):
    # 이것은 매우 단순화된 가상 모델입니다.
    # 실제 마이크로렌징 피크를 흉내냅니다.
    magnification = 1.0 + np.exp(-(t / (50 / velocity))**2) * (lens_m * 0.5) # 렌즈 별에 의한 기본 피크

    if has_p and planet_m_ratio > 0:
        # 행성에 의한 추가적인 작은 변동 (피크 또는 딥)
        # 행성 위치에 따라 피크가 약간 이동하거나 두 번째 피크가 나타나는 것을 흉내
        planet_influence_time = t - (planet_orb * np.cos(np.deg2rad(phase))) / (velocity / 10) # 가상의 시간 지연
        magnification += np.exp(-( (planet_influence_time - 2)**2 / (0.5 + planet_m_ratio * 100)) ) * (planet_m_ratio * 50)
        
        # 충격 매개변수가 0에 가까울수록 피크가 더 높고 행성 영향이 강한 것처럼 시뮬레이션
        if impact_param < 0.1:
            magnification *= (1 + (0.5 - impact_param) * 0.5) # 중심 통과 시 밝기 더 높게

    return magnification

# 밝기 계산
magnifications = calculate_magnification(
    time_points,
    lens_mass,
    planet_mass_ratio,
    planet_orbit_radius,
    planet_phase,
    lens_velocity,
    impact_parameter,
    has_planet
)


# --- 4. 밝기 곡선 그래프 그리기 ---
st.subheader("밝기 곡선")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time_points, magnifications, label="광원 별 밝기", color='blue')
ax.set_xlabel("시간 (일)", fontsize=12)
ax.set_ylabel("상대 밝기 / 증폭률", fontsize=12)
ax.set_title("중력 마이크로렌징 밝기 곡선", fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_ylim(min(0.8, np.min(magnifications) * 0.9), max(2.5, np.max(magnifications) * 1.1)) # Y축 범위 자동 조정
ax.legend()

# 스트림릿에 그래프 표시
st.pyplot(fig)

st.write("---")

# --- 5. 시뮬레이션 설명 (텍스트) ---
st.subheader("시뮬레이션 설명")
st.write(f"""
- **렌즈 별 질량:** {lens_mass} 태양 질량
- **광원 별 질량:** {source_mass} 태양 질량
- **렌즈의 상대 속도:** {lens_velocity} km/s
- **충격 매개변수:** {impact_parameter} (렌즈와 광원의 가장 가까운 거리, 아인슈타인 반경 대비)
""")

if has_planet:
    st.write(f"""
    - **행성 포함:** 예
    - **행성 질량비:** {planet_mass_ratio:.4f} (렌즈 별 질량 대비)
    - **행성 궤도 반지름:** {planet_orbit_radius} (아인슈타인 반경 대비)
    - **행성 초기 위상:** {planet_phase}도
    """)
else:
    st.write("- **행성 포함:** 아니요")

st.info("""
**참고:** 밝기 곡선의 피크는 렌즈 별이 배경 광원 별 앞을 지나갈 때 발생합니다.
행성이 렌즈 별 주변을 공전하며 이 피크에 추가적인 짧은 변동(피크 또는 딥)을 만들어냅니다.
이러한 작은 변동을 통해 행성의 존재와 특성을 유추할 수 있습니다.
""")

st.write("---")
st.caption("© 2025 중력 마이크로렌징 시뮬레이터")
