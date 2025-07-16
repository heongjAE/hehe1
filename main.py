import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageDraw
import platform

# --- 폰트 및 Matplotlib 스타일 설정 ---
@st.cache_resource
def setup_matplotlib():
    if platform.system() == 'Darwin': # Mac
        plt.rcParams['font.family'] = 'AppleGothic'
    elif platform.system() == 'Windows': # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else: # Linux (Ubuntu 등)
        plt.rcParams['font.family'] = 'NanumGothic'

    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('dark_background')

setup_matplotlib()


# --- 전체 페이지 스타일 설정 (HTML/CSS 인라인 삽입) ---
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

    /* 메인 페이지 버튼 스타일 (배경색 그라데이션 및 호버 효과 강화) */
    .stButton > button {
        display: block;
        width: 100%;
        padding: 20px;
        margin: 20px auto;
        font-size: 1.5em;
        font-weight: bold;
        border: 2px solid #4682B4;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        text-decoration: none;

        /* 버튼 배경에 그라데이션 적용 */
        background: linear-gradient(to right, #1A2A4A, #2A3A5A, #3A4A6A);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #4682B4, #6A9CC9, #8DBBDD);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(70, 130, 180, 0.7);
    }

    /* Streamlit이 버튼 텍스트를 렌더링하는 방식 때문에 추가적인 CSS 필요 */
    .stButton > button > div > span {
        background-image: linear-gradient(to right, #00BFFF, #87CEFA, #ADD8E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        text-shadow: 0 0 8px rgba(135, 206, 250, 0.6);
        font-weight: bold;
    }

    .stButton > button:hover > div > span {
        background-image: none;
        -webkit-background-clip: unset;
        -webkit-text-fill-color: unset;
        color: white;
        text-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 시뮬레이션 계산 로직 (캐싱) ---
@st.cache_data
def calculate_magnification_data(lens_m, planet_m_ratio, planet_orb, phase, velocity, impact_param, has_p):
    time_points = np.linspace(-15, 15, 300)
    magnification = 1.0 + np.exp(-(time_points / (50 / velocity))**2) * (lens_m * 0.5)

    if has_p and planet_m_ratio > 0:
        planet_influence_time = time_points - (planet_orb * np.cos(np.deg2rad(phase))) / (velocity / 10)
        magnification += np.exp(-( (planet_influence_time - 2)**2 / (0.5 + planet_m_ratio * 100)) ) * (planet_m_ratio * 50)
        
        if impact_param < 0.1:
            magnification *= (1 + (0.5 - impact_param) * 0.5)
    return time_points, magnification

# --- Matplotlib 그래프 생성 함수 (캐싱) ---
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

    # 중력 렌즈 (중앙의 흰 점)
    lens_circle = Circle((0, 0), lens_radius, color=lens_color, zorder=10)
    ax.add_patch(lens_circle)

    # 광원 별의 왜곡된 이미지 표현
    if impact_param < 0.1: # 아인슈타인 링에 가까운 경우
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
        
    elif impact_param < 0.5: # 이미지가 분리되거나 늘어나는 경우
        # 두 개의 왜곡된 이미지 (개념적 표현)
        circle1 = Circle((source_radius * 2 * (1 - impact_param), 0), source_radius * 1.5 * (1 - impact_param/0.5), color=source_color, alpha=0.8)
        ax.add_patch(circle1)
        circle2 = Circle((-source_radius * 1 * (1 - impact_param), 0), source_radius * 0.5 * (1 - impact_param/0.5), color=source_color, alpha=0.5)
        ax.add_patch(circle2)
    else: # 왜곡이 거의 없는 경우 (원래 광원 별)
        circle = Circle((0, 0), source_radius, color=source_color)
        ax.add_patch(circle)
    
    return fig

# --- 페이지 전환 콜백 함수 ---
def set_page(page_name):
    st.session_state.page = page_name

# --- 1. 메인 페이지 함수 ---
def main_page():
    st.title("🌌 우주 시뮬레이터")
    st.write("환영합니다! 아래 버튼을 눌러 시뮬레이션을 시작하거나 설명을 확인하세요.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "🚀 중력 마이크로렌징 시뮬레이션 시작",
            key="start_simulation_button",
            on_click=set_page,
            args=('simulation',),
            use_container_width=True
        )

    with col2:
        st.button(
            "📚 시뮬레이션 설명 보기",
            key="view_explanation_button",
            on_click=set_page,
            args=('explanation',),
            use_container_width=True
        )

# --- 2. 시뮬레이션 페이지 함수 ---
def simulation_page():
    st.title("✨ 중력 마이크로렌징 시뮬레이터")
    st.write("""
        이 앱은 **중력 마이크로렌징** 현상으로 인한 광원 별의 밝기 변화를 시뮬레이션하고,
        렌즈 별에 의한 **광원 별 이미지의 개념적 왜곡**을 보여줍니다.
        아래 설정을 변경하여 밝기 곡선과 이미지 시뮬레이션이 어떻게 변하는지 확인해 보세요!
    """)

    st.write("---")

    # --- 2. 시뮬레이션 설정 입력 받기 ---
    st.sidebar.header("설정")

    source_mass = st.sidebar.number_input("광원 별 질량 (태양 질량)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    lens_mass = st.sidebar.number_input("렌즈 별 질량 (태양 질량)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
    lens_velocity = st.sidebar.slider("렌즈 상대 속도 (km/s)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
    impact_parameter = st.sidebar.slider("충격 매개변수", min_value=0.0, max_value=2.0, value=0.5, step=0.05)
    
    st.sidebar.subheader("행성 (Planet - 선택 사항)")
    has_planet = st.sidebar.checkbox("행성 포함", value=False)
    if has_planet:
        planet_mass_ratio = st.sidebar.slider("행성 질량비 (렌즈 별 질량 대비)", min_value=0.0001, max_value=0.1, value=0.001, format="%.4f")
        planet_orbit_radius = st.sidebar.slider("행성 궤도 반지름 (Einstein Radius 단위)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)
        planet_phase = st.sidebar.slider("행성 초기 위상 (도)", min_value=0, max_value=360, value=0, step=10)
    else:
        planet_mass_ratio = 0.0
        planet_orbit_radius = 0.0
        planet_phase = 0

    st.sidebar.write("---")
    st.sidebar.info("참고: 이 시뮬레이터의 밝기 곡선과 이미지 시뮬레이션은 개념적인 모델에 기반하며, 실제 천체 물리 계산과 다를 수 있습니다.")

    time_points, magnifications = calculate_magnification_data(
        lens_mass, planet_mass_ratio, planet_orbit_radius, planet_phase,
        lens_velocity, impact_parameter, has_planet
    )

    # --- 4. 배경별 광도 변화 (밝기 곡선) 그래프 그리기 ---
    st.subheader("📈 배경별 광도 변화 (밝기 곡선)")
    st.write("""
        이 그래프는 렌즈 별이 배경 광원 별 앞을 지나갈 때,
        **배경 광원 별의 밝기가 시간 경과에 따라 어떻게 변하는지** 보여줍니다.
        중력 렌즈 효과로 인해 밝기가 일시적으로 증가하는 피크가 나타납니다.
        행성이 존재하면 이 피크에 미세한 추가적인 밝기 변화가 나타날 수 있습니다.
    """)
    fig_light_curve = plot_light_curve(time_points, magnifications)
    st.pyplot(fig_light_curve)
    plt.close(fig_light_curve)

    st.write("---")

    # --- 5. 중력렌즈 시스템 시각화 (이미지 왜곡) ---
    st.subheader("🌌 중력렌즈 시스템 시각화 (광원 별 이미지 왜곡)")
    st.write("""
        아래 이미지는 **중력 렌즈 시스템**을 개념적으로 보여줍니다.
        중앙의 작은 흰 점은 **렌즈 별**을 나타내며, 주변의 노란색/주황색 영역은
        렌즈 별의 중력에 의해 **배경 광원 별의 빛이 휘어져 보이는 모습**을 시뮬레이션한 것입니다.
        충격 매개변수 값에 따라 아인슈타인 링이나 여러 개의 이미지로 왜곡될 수 있습니다.
    """)

    fig_image_sim = create_microlensing_image_cached(impact_parameter)
    st.pyplot(fig_image_sim)
    plt.close(fig_image_sim)

    st.write("---")

    # 메인으로 돌아가기 버튼
    st.button(
        "⬅️ 메인 화면으로 돌아가기",
        key="back_to_main_sim",
        on_click=set_page,
        args=('main',)
    )

# --- 3. 시뮬레이션 설명 페이지 함수 ---
def explanation_page():
    st.title("📚 시뮬레이션 설명")
    st.write("""
    이 페이지에서는 중력 마이크로렌징 시뮬레이터의 작동 원리와 각 매개변수에 대한 자세한 설명을 제공합니다.
    """)
    st.markdown("---")

    st.subheader("중력 마이크로렌징이란?")
    st.write("""
    **중력 마이크로렌징(Gravitational Microlensing)**은 아인슈타인의 일반 상대성 이론에 의해 예측되는 현상으로,
    무거운 천체(렌즈 별)가 배경의 밝은 천체(광원 별) 앞을 지나갈 때, 렌즈 별의 중력이 광원 별에서 오는 빛을 휘게 하여
    광원 별의 밝기가 일시적으로 증가하거나, 이미지가 왜곡되어 여러 개로 보이는 현상을 말합니다.
    """)

    st.subheader("시뮬레이션 매개변수 설명")
    st.write("""
    - **광원 별 질량 (Source Star Mass):** 배경에 있는 빛을 내는 별의 질량입니다. 시뮬레이션에서는 밝기 변화의 스케일에 영향을 줍니다.
    - **렌즈 별 질량 (Lens Star Mass):** 중력 렌즈 역할을 하는 별의 질량입니다. 이 질량이 클수록 빛을 더 강하게 휘게 하여 밝기 변화가 커집니다.
    - **상대 속도 (Relative Velocity):** 렌즈 별이 광원 별 앞을 지나가는 상대적인 속도입니다. 속도가 빠를수록 밝기 변화 현상이 짧은 시간 동안 발생합니다.
    - **충격 매개변수 (Impact Parameter):** 렌즈 별과 광원 별의 시선 방향 상의 가장 가까운 거리를 나타냅니다. 이 값이 작을수록 (0에 가까울수록) 렌즈 별과 광원 별이 더 정확히 정렬되어 밝기 증가 폭이 커지고 왜곡이 심해집니다.
    - **행성 포함 (Planet Inclusion):** 렌즈 별에 행성이 동반되어 있는지 여부를 설정합니다.
        - **행성 질량비 (Planet Mass Ratio):** 렌즈 별 질량 대비 행성의 질량 비율입니다. 이 비율이 클수록 행성에 의한 추가적인 밝기 변화 신호가 뚜렷해집니다.
        - **행성 궤도 반지름 (Planet Orbit Radius):** 행성이 렌즈 별 주위를 도는 궤도의 크기입니다.
        - **행성 초기 위상 (Planet Initial Phase):** 시뮬레이션 시작 시 행성의 궤도 상의 초기 위치를 각도로 나타냅니다.
    """)

    st.subheader("시뮬레이션 결과 해석")
    st.info("""
    **밝기 곡선:** 렌즈 별이 배경 광원 별 앞을 지나갈 때 밝기가 일시적으로 증가하는 피크가 발생합니다.
    행성이 존재하면 이 피크에 짧고 특징적인 변동(추가 피크 또는 딥)을 만들어냅니다.

    **이미지 왜곡:**
    - **충격 매개변수가 0에 가까울수록 (중앙 정렬):** 광원 별의 빛이 렌즈 별 주변으로 강하게 휘어져 **아인슈타인 링**과 같은 원형 또는 부분적인 링 형태로 보일 수 있습니다.
    - **충격 매개변수가 0.1~0.5 (가까이 지나갈 때):** 광원 별의 이미지가 길게 **늘어나거나 두 개의 분리된 이미지**로 보일 수 있습니다.
    - **충격 매개변수가 클수록 (멀리 떨어져 있을 때):** 왜곡이 거의 없으며, 광원 별은 원래의 원형에 가깝게 보입니다.
    """)

    st.write("---")
    # 메인으로 돌아가기 버튼
    st.button(
        "⬅️ 메인 화면으로 돌아가기",
        key="back_to_main_exp",
        on_click=set_page,
        args=('main',)
    )

# --- 앱의 진입점 (페이지 라우팅) ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'simulation':
    simulation_page()
elif st.session_state.page == 'explanation':
    explanation_page()

st.caption("© 2025 중력 마이크로렌징 시뮬레이터")
