import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageDraw
import platform

# --- 한글 폰트 설정 ---
if platform.system() == 'Darwin': # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows': # Windows
    plt.rcParams['font.family'] = 'Malgun Gothic'
else: # Linux (Ubuntu 등)
    # Ubuntu의 경우 'NanumGothic' 설치 필요:
    # sudo apt-get update
    # sudo apt-get install fonts-nanum-extra
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# --- 폰트 캐시 삭제 (에러 방지) ---
# Matplotlib 폰트 설정 변경 후 캐시를 지워줘야 반영되는 경우가 있습니다.
# 이 코드는 앱 실행 시 한 번만 실행되도록 캐싱됩니다.
@st.cache_resource
def clear_matplotlib_cache():
    plt.style.use('dark_background') # 어두운 배경 스타일 적용
    # Matplotlib 폰트 캐시를 지웁니다.
    # import matplotlib.font_manager as fm
    # fm._load_fontmanager(try_read_cache=False) # 이 방식은 최신 버전에서 다르게 작동할 수 있습니다.
    # 간단히 font_manager를 리로드하는 대신, 스트림릿 재실행 시 폰트가 적용되도록 합니다.
    # 필요한 경우, 터미널에서 `rm -rf ~/.cache/matplotlib` 실행 후 재실행.
clear_matplotlib_cache()


# --- 전체 페이지 스타일 설정 (HTML/CSS 인라인 삽입) ---
st.markdown(
    """
    <style>
    /* 전체 배경을 검정색으로 하고 은하수 느낌 패턴 추가 */
    body {
        background-color: #000000; /* 완전 검정 */
        background-image: url('https://www.transparenttextures.com/patterns/stardust.png'); /* 별 먼지 패턴 */
        background-repeat: repeat;
        background-size: 150px 150px; /* 패턴 크기 조절 */
    }
    
    /* 전체 앱 컨테이너의 배경도 투명하게 또는 어둡게 */
    .stApp {
        background-color: rgba(0, 0, 0, 0); /* 투명하게 */
        color: white; /* 기본 글자색 흰색으로 */
    }
    
    /* 사이드바 배경 및 글자색 */
    .stSidebar {
        background-color: #1a1a2e; /* 어두운 남색 계열 */
        color: white;
        border-right: 1px solid #0f0f2a;
    }
    .stSidebar .stNumberInput, .stSidebar .stSlider {
        color: #b0e0e6; /* 밝은 청록색 */
    }
    .stSidebar label {
        color: #87CEEB; /* 하늘색 */
        font-weight: bold;
    }
    .stSidebar .stButton>button {
        background-color: #2a2a4a;
        color: #b0e0e6;
        border: 1px solid #4682B4;
    }
    .stSidebar .stButton>button:hover {
        background-color: #4682B4;
        color: white;
    }

    /* 제목 (h1) 그라데이션 */
    h1 {
        background: linear-gradient(to right, #00BFFF, #87CEFA, #4682B4); /* 밝은 파란색 그라데이션 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        text-shadow: 0 0 10px rgba(135, 206, 250, 0.5); /* 그림자 효과 */
    }

    /* 다른 제목 (h2, h3) 색상 */
    h2, h3 {
        color: #ADD8E6; /* 연한 파란색 */
        text-shadow: 0 0 5px rgba(173, 216, 230, 0.3);
    }
    
    /* 일반 텍스트 및 정보 상자 */
    p, .stMarkdown, .stInfo {
        color: #E0FFFF; /* 밝은 하늘색 */
    }
    .stInfo {
        background-color: #0A1128; /* 정보 상자 배경색 (더 어둡게) */
        border-left: 5px solid #4682B4;
    }

    /* 슬라이더 값 표시 색상 */
    .stSlider > div > div > div > div {
        color: #87CEFA; /* 밝은 파란색 */
    }
    
    /* 인풋 필드 글자색 */
    .stNumberInput input {
        color: #b0e0e6; /* 밝은 청록색 */
        background-color: #0f0f2a; /* 어두운 배경 */
        border: 1px solid #4682B4;
    }
    
    /* 체크박스 색상 */
    .stCheckbox > label > div:first-child {
        border-color: #87CEFA !important; /* 체크박스 테두리 */
    }
    .stCheckbox > label > div:first-child > div {
        background-color: #4682B4 !important; /* 체크박스 선택 시 */
    }
    .stCheckbox label span {
        color: #E0FFFF; /* 체크박스 텍스트 색상 */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- 1. 앱 제목 및 설명 ---
st.title("✨ 중력 마이크로렌징 시뮬레이터")
st.write("""
    이 앱은 **중력 마이크로렌징** 현상으로 인한 광원 별의 밝기 변화를 시뮬레이션하고,
    렌즈 별에 의한 **광원 별 이미지의 개념적 왜곡**을 보여줍니다.
    아래 설정을 변경하여 밝기 곡선과 이미지 시뮬레이션이 어떻게 변하는지 확인해 보세요!
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
st.sidebar.info("참고: 이 시뮬레이터의 밝기 곡선과 이미지 시뮬레이션은 개념적인 모델에 기반하며, 실제 천체 물리 계산과 다를 수 있습니다.")

# --- 3. 시뮬레이션 로직 (가상 모델) ---

# 시간 축 (일)
time_points = np.linspace(-15, 15, 300) # -15일에서 +15일까지 300개 지점

# 가상 밝기 계산 함수 (실제 마이크로렌징 수식 아님)
def calculate_magnification(t, lens_m, planet_m_ratio, planet_orb, phase, velocity, impact_param, has_p):
    # 이것은 매우 단순화된 가상 모델입니다.
    magnification = 1.0 + np.exp(-(t / (50 / velocity))**2) * (lens_m * 0.5)

    if has_p and planet_m_ratio > 0:
        planet_influence_time = t - (planet_orb * np.cos(np.deg2rad(phase))) / (velocity / 10)
        magnification += np.exp(-( (planet_influence_time - 2)**2 / (0.5 + planet_m_ratio * 100)) ) * (planet_m_ratio * 50)
        
        if impact_param < 0.1:
            magnification *= (1 + (0.5 - impact_param) * 0.5)

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

fig_light_curve, ax_light_curve = plt.subplots(figsize=(10, 5))
ax_light_curve.plot(time_points, magnifications, label="광원 별 밝기", color='#87CEEB') # 그래프 선 색상 변경
ax_light_curve.set_xlabel("시간 (일)", fontsize=12)
ax_light_curve.set_ylabel("상대 밝기 / 증폭률", fontsize=12)
ax_light_curve.set_title("중력 마이크로렌징 밝기 곡선", fontsize=14)
ax_light_curve.grid(True, linestyle='--', alpha=0.7, color='#4682B4') # 그리드 색상 변경
ax_light_curve.set_ylim(min(0.8, np.min(magnifications) * 0.9), max(2.5, np.max(magnifications) * 1.1))
ax_light_curve.legend(labelcolor='white') # 범례 글자색 흰색
# Matplotlib 텍스트 색상 수동 조정 (plt.style.use('dark_background')가 처리 못하는 부분)
ax_light_curve.tick_params(axis='x', colors='white')
ax_light_curve.tick_params(axis='y', colors='white')
ax_light_curve.xaxis.label.set_color('white')
ax_light_curve.yaxis.label.set_color('white')
ax_light_curve.title.set_color('white')


st.pyplot(fig_light_curve)

st.write("---")

# --- 5. 이미지 시뮬레이션 ---
st.subheader("이미지 왜곡 시뮬레이션 (개념적)")
st.write("""
    아래 이미지는 **렌즈 별(중앙의 검은 점)**이 배경 광원 별의 빛을 휘게 하여
    어떻게 보일 수 있는지 개념적으로 보여줍니다. 
    실제 마이크로렌징 현상은 빛을 여러 경로로 휘게 하여 광원 별이 여러 개로 보이거나
    아인슈타인 링과 같은 형태로 왜곡될 수 있습니다.
""")

# 이미지 생성 함수
def create_microlensing_image(impact_param, resolution=400):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off') # 축 숨기기

    # 배경색 (Matplotlib figure의 배경을 검정색으로 설정)
    fig.set_facecolor('black')
    ax.set_facecolor('black')

    # 광원 별 (배경)
    source_radius = 0.1
    source_color = '#FFFF00' # 밝은 노란색

    # 렌즈 별 (중앙)
    lens_radius = 0.03
    lens_color = 'white' # 렌즈 별을 흰색 점으로 표시

    # 충격 매개변수에 따른 광원 별의 왜곡된 모습 (간단한 모델)
    if impact_param < 0.1: # 렌즈에 거의 정렬될 때
        ring_radius = 0.5 + (0.1 - impact_param) * 2
        
        img_size = resolution
        img = Image.new('RGB', (img_size, img_size), color = 'black')
        draw = ImageDraw.Draw(img)
        
        center = img_size // 2
        
        # PIL을 이용한 아인슈타인 링 (밝기, 흐림 효과는 Matplotlib으로 다시 렌더링될 때 한계가 있음)
        # 더 나은 렌더링을 위해선 외부 이미지 라이브러리(ex. OpenCV) 또는 GLSL 셰이더 사용이 적합
        # 여기서는 단순히 외곽선만으로 링 효과를 냅니다.
        for i in range(20):
            radius = ring_radius * (img_size / 2) * (1 - i*0.02)
            alpha_val = int(255 * (1 - i/20)**2) # 알파값은 PIL draw.ellipse에서 직접 반영 안됨
            current_color = (255, 255, 0, alpha_val) # RGBa
            draw.ellipse((center - radius, center - radius, center + radius, center + radius), 
                         outline=(current_color[0], current_color[1], current_color[2]), width=max(1, int(i/2)))

        draw.ellipse((center - ring_radius * (img_size / 2) * 0.9, center - ring_radius * (img_size / 2) * 0.9,
                      center + ring_radius * (img_size / 2) * 0.9, center + ring_radius * (img_size / 2) * 0.9), 
                     outline=source_color, width=max(1, int(img_size / 100)))

        ax.imshow(np.array(img), extent=[-1.5, 1.5, -1.5, 1.5], zorder=0) # 배경 이미지로 깔기
        
    elif impact_param < 0.5: # 렌즈에 가까울 때
        # 길게 늘어난 초승달 모양 또는 두 개의 이미지
        circle1 = Circle((source_radius * 2 * (1 - impact_param), 0), source_radius * 1.5 * (1 - impact_param/0.5), color=source_color, alpha=0.8)
        ax.add_patch(circle1)
        circle2 = Circle((-source_radius * 1 * (1 - impact_param), 0), source_radius * 0.5 * (1 - impact_param/0.5), color=source_color, alpha=0.5)
        ax.add_patch(circle2)
    else: # 렌즈에서 멀리 떨어져 있을 때 (거의 왜곡 없음)
        circle = Circle((0, 0), source_radius, color=source_color)
        ax.add_patch(circle)
    
    # 렌즈 별 (항상 중앙에 표시)
    lens_circle = Circle((0, 0), lens_radius, color=lens_color, zorder=10)
    ax.add_patch(lens_circle)
    
    return fig

# 이미지 시뮬레이션 생성 및 표시
fig_image_sim = create_microlensing_image(impact_parameter)
st.pyplot(fig_image_sim)

st.write("---")

# --- 6. 시뮬레이션 설명 (텍스트) ---
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
**밝기 곡선:** 렌즈 별이 배경 광원 별 앞을 지나갈 때 밝기가 일시적으로 증가하는 피크가 발생합니다.
행성이 존재하면 이 피크에 짧고 특징적인 변동(추가 피크 또는 딥)을 만들어냅니다.

**이미지 왜곡:**
- **충격 매개변수가 0에 가까울수록 (중앙 정렬):** 광원 별의 빛이 렌즈 별 주변으로 강하게 휘어져 **아인슈타인 링**과 같은 원형 또는 부분적인 링 형태로 보일 수 있습니다.
- **충격 매개변수가 0.1~0.5 (가까이 지나갈 때):** 광원 별의 이미지가 길게 **늘어나거나 두 개의 분리된 이미지**로 보일 수 있습니다.
- **충격 매개변수가 클수록 (멀리 떨어져 있을 때):** 왜곡이 거의 없으며, 광원 별은 원래의 원형에 가깝게 보입니다.
""")

st.write("---")
st.caption("© 2025 중력 마이크로렌징 시뮬레이터")
