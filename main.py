import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageDraw
import platform

# --- 폰트 및 Matplotlib 스타일 설정 ---
@st.cache_resource
def setup_matplotlib():
    # 운영체제에 따라 한글 폰트 설정
    if platform.system() == 'Darwin': # Mac
        plt.rcParams['font.family'] = 'AppleGothic'
    elif platform.system() == 'Windows': # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else: # Linux (Ubuntu 등)
        # Linux의 경우 'NanumGothic' 설치 필요:
        # sudo apt-get update
        # sudo apt-get install fonts-nanum-extra
        plt.rcParams['font.family'] = 'NanumGothic'

    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    plt.style.use('dark_background') # 어두운 배경 스타일 적용

setup_matplotlib() # 앱 시작 시 한 번만 실행되도록 캐싱


# --- 전체 페이지 스타일 설정 (HTML/CSS 인라인 삽입) ---
# 이 부분은 변경 없음 (스타일은 이미 잘 적용되어 있습니다)
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/ESO_-_The_Milky_Way_over_Paranal_%28by_Y.Beletsky%29.jpg/1280px-ESO_-_The_Milky_Way_over_Paranal_%28by_Y.Beletsky%29.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }
    
    .stApp {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    
    .stSidebar {
        background-color: rgba(26, 26, 46, 0.8);
        color: white;
        border-right: 1px solid #0f0f2a;
        padding: 15px;
        border-radius: 10px;
    }
    .stSidebar .stNumberInput, .stSidebar .stSlider {
        color: #b0e0e6;
    }
    .stSidebar label {
        color: #87CEEB;
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

    h1 {
        background: linear-gradient(to right, #00BFFF, #87CEFA, #4682B4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        text-shadow: 0 0 15px rgba(135, 206, 250, 0.7);
        padding-bottom: 10px;
    }

    h2, h3 {
        color: #ADD8E6;
        text-shadow: 0 0 8px rgba(173, 216, 230, 0.5);
    }
    
    p, .stMarkdown, .stInfo {
        color: #E0FFFF;
    }
    .stInfo {
        background-color: rgba(10, 17, 40, 0.7);
        border-left: 5px solid #4682B4;
        border-radius: 5px;
        padding: 10px;
    }

    .stSlider > div > div > div > div {
        color: #87CEFA;
    }
    
    .stNumberInput input {
        color: #b0e0e6;
        background-color: rgba(15, 15, 42, 0.7);
        border: 1px solid #4682B4;
        border-radius: 5px;
    }
    
    .stCheckbox > label > div:first-child {
        border-color: #87CEFA !important;
    }
    .stCheckbox > label > div:first-child > div {
        background-color: #4682B4 !important;
    }
    .stCheckbox label span {
        color: #E0FFFF;
    }

    hr {
        border-top: 1px dashed #4682B4;
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
impact_parameter = st.sidebar.slider("충격 매개변수", min_value=0.0, max_value=2.0, value=0.5, step=0.05)


# 행성 설정 (선택 사항)
st.sidebar.subheader("행성 (Planet - 선택 사항)")
has_planet = st.sidebar.checkbox("행성 포함", value=False)
if has_planet:
    planet_mass_ratio = st.sidebar.slider("행성 질량비 (렌즈 별 질량 대비)", min_value=0.0001, max_value=0.1, value=0.001, format="%.4f")
    planet_orbit_radius = st.sidebar.slider("행성 궤도 반지름 (Einstein Radius 단위)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)
    planet_phase = st.sidebar.slider("행성 초기 위상 (도)", min_value=0, max_value=360, value=0, step=10)
else:
    # 행성이 없을 때 기본값 설정 (명시적으로)
    planet_mass_ratio = 0.0
    planet_orbit_radius = 0.0
    planet_phase = 0

st.sidebar.write("---")
st.sidebar.info("참고: 이 시뮬레이터의 밝기 곡선과 이미지 시뮬레이션은 개념적인 모델에 기반하며, 실제 천체 물리 계산과 다를 수 있습니다.")

# --- 3. 시뮬레이션 로직 (가상 모델) ---
# 함수를 캐싱하여 동일 입력에 대한 재계산 방지
@st.cache_data
def calculate_magnification_data(lens_m, planet_m_ratio, planet_orb, phase, velocity, impact_param, has_p):
    time_points = np.linspace(-15, 15, 300) # 시간 축 (일)
    
    # 이것은 매우 단순화된 가상 모델입니다.
    magnification = 1.0 + np.exp(-(time_points / (50 / velocity))**2) * (lens_m * 0.5)

    if has_p and planet_m_ratio > 0:
        planet_influence_time = time_points - (planet_orb * np.cos(np.deg2rad(phase))) / (velocity / 10)
        magnification += np.exp(-( (planet_influence_time - 2)**2 / (0.5 + planet_m_ratio * 100)) ) * (planet_m_ratio * 50)
        
        if impact_param < 0.1:
            magnification *= (1 + (0.5 - impact_param) * 0.5)

    return time_points, magnification

# 밝기 계산
time_points, magnifications = calculate_magnification_data(
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

# 그래프 생성 함수 (캐싱하여 재렌더링 효율화)
@st.cache_resource
def plot_light_curve(time_points, magnifications):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time_points, magnifications, label="광원 별 밝기", color='#87CEEB')
    ax.set_xlabel("시간 (일)", fontsize=12)
    ax.set_ylabel("상대 밝기 / 증폭률", fontsize=12)
    ax.set_title("중력 마이크로렌징 밝기 곡선", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7, color='#4682B4')
    ax.set_ylim(min(0.8, np.min(magnifications) * 0.9), max(2.5, np.max(magnifications) * 1.1))
    ax.legend(labelcolor='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    return fig

fig_light_curve = plot_light_curve(time_points, magnifications)
st.pyplot(fig_light_curve)
plt.close(fig_light_curve) # 중요: 그래프 객체를 닫아 메모리 누수 방지

st.write("---")

# --- 5. 이미지 시뮬레이션 ---
st.subheader("이미지 왜곡 시뮬레이션 (개념적)")
st.write("""
    아래 이미지는 **렌즈 별(중앙의 검은 점)**이 배경 광원 별의 빛을 휘게 하여
    어떻게 보일 수 있는지 개념적으로 보여줍니다. 
    실제 마이크로렌징 현상은 빛을 여러 경로로 휘게 하여 광원 별이 여러 개로 보이거나
    아인슈타인 링과 같은 형태로 왜곡될 수 있습니다.
""")

# 이미지 생성 함수 (캐싱하여 재렌더링 효율화)
@st.cache_resource
def create_microlensing_image_cached(impact_param, resolution=400):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.set_facecolor('black')
    ax.set_facecolor('black')

    source_radius = 0.1
    source_color = '#FFFF00'

    lens_radius = 0.03
    lens_color = 'white'

    if impact_param < 0.1:
        ring_radius = 0.5 + (0.1 - impact_param) * 2
        
        img_size = resolution
        img = Image.new('RGB', (img_size, img_size), color = 'black')
        draw = ImageDraw.Draw(img)
        
        center = img_size // 2
        
        for i in range(20):
            radius = ring_radius * (img_size / 2) * (1 - i*0.02)
            current_color = (255, 255, 0, int(255 * (1 - i/20)**2))
            draw.ellipse((center - radius, center - radius, center + radius, center + radius), 
                         outline=(current_color[0], current_color[1], current_color[2]), width=max(1, int(i/2)))

        draw.ellipse((center - ring_radius * (img_size / 2) * 0.9, center - ring_radius * (img_size / 2) * 0.9,
                      center + ring_radius * (img_size / 2) * 0.9, center + ring_radius * (img_size / 2) * 0.9), 
                     outline=source_color, width=max(1, int(img_size / 100)))

        ax.imshow(np.array(img), extent=[-1.5, 1.5, -1.5, 1.5], zorder=0)
        
    elif impact_param < 0.5:
        circle1 = Circle((source_radius * 2 * (1 - impact_param), 0), source_radius * 1.5 * (1 - impact_param/0.5), color=source_color, alpha=0.8)
        ax.add_patch(circle1)
        circle2 = Circle((-source_radius * 1 * (1 - impact_param), 0), source_radius * 0.5 * (1 - impact_param/0.5), color=source_color, alpha=0.5)
        ax.add_patch(circle2)
    else:
        circle = Circle((0, 0), source_radius, color=source_color)
        ax.add_patch(circle)
    
    lens_circle = Circle((0, 0), lens_radius, color=lens_color, zorder=10)
    ax.add_patch(lens_circle)
    
    return fig

fig_image_sim = create_microlensing_image_cached(impact_parameter)
st.pyplot(fig_image_sim)
plt.close(fig_image_sim) # 중요: 그래프 객체를 닫아 메모리 누수 방지

st.write("---")

# --- 6. 시뮬레이션 설명 (텍스트) ---
st.subheader("시뮬레이션 설명")
st.write(f"""
- **렌즈 별 질량:** {lens_mass} 태양 질량
- **광원 별 질량:** {source_mass} 태양 질량
- **렌즈의 상대 속도:** {lens_velocity} km/s
- **충격 매개변수:** {impact_parameter} (렌즈와 광원의 가장 가까운 거리)
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
