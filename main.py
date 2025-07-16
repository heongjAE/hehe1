import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

import platform



# --- 폰트 및 Matplotlib 스타일 설정 ---

@st.cache_resource

def setup_matplotlib():

    """운영체제에 따라 한글 폰트를 설정하고 Matplotlib 스타일을 적용합니다."""

    if platform.system() == 'Darwin': # Mac

        plt.rcParams['font.family'] = 'AppleGothic'

    elif platform.system() == 'Windows': # Windows

        plt.rcParams['font.family'] = 'Malgun Gothic'

    else: # Linux (Ubuntu 등)

        # Linux 환경에서 'NanumGothic'이 설치되어 있어야 합니다.

        # 설치: sudo apt-get update && sudo apt-get install fonts-nanum-extra

        plt.rcParams['font.family'] = 'NanumGothic'



    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

    plt.style.use('dark_background') # 어두운 배경 스타일 적용



setup_matplotlib() # 앱 시작 시 한 번만 실행되도록 캐싱





# --- 전체 페이지 스타일 설정 (HTML/CSS 인라인 삽입) ---

# CSS를 사용하여 Streamlit 기본 스타일을 오버라이드하고 커스텀 디자인 적용

st.markdown(

    """

    <style>

    /* 전체 바디 배경 설정 */

    body {

        background-color: #000000; /* 어두운 배경색 */

        background-image: url('https://upload.wikimedia.wikimedia.org/wikipedia/commons/thumb/c/c5/ESO_-_The_Milky_Way_over_Paranal_%28by_Y.Beletsky%29.jpg/1280px-ESO_-_The_Milky_Way_over_Paranal_%28by_Y.Beletsky%29.jpg'); /* 은하수 배경 이미지 */

        background-repeat: no-repeat;

        background-size: cover;

        background-position: center center;

        background-attachment: fixed; /* 스크롤 시 배경 고정 */

    }

    

    /* Streamlit 앱 컨테이너 스타일 */

    .stApp {

        background-color: rgba(0, 0, 0, 0.5); /* 반투명 검정 배경 */

        color: white;

        padding: 20px;

        border-radius: 10px;

    }

    

    /* 사이드바 스타일 */

    .stSidebar {

        background-color: rgba(26, 26, 46, 0.8); /* 반투명 어두운 파랑 */

        color: white;

        border-right: 1px solid #0f0f2a;

        padding: 15px;

        border-radius: 10px;

    }

    .stSidebar .stNumberInput, .stSidebar .stSlider {

        color: #b0e0e6; /* 연한 하늘색 */

    }

    .stSidebar label {

        color: #87CEEB; /* 밝은 하늘색 */

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



    /* 제목 (h1) 스타일 */

    h1 {

        background: linear-gradient(to right, #00BFFF, #87CEFA, #4682B4); /* 파란색 그라데이션 */

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        font-size: 3em;

        text-shadow: 0 0 15px rgba(135, 206, 250, 0.7); /* 빛나는 효과 */

        padding-bottom: 10px;

    }



    /* 부제목 (h2, h3) 스타일 */

    h2, h3 {

        color: #ADD8E6; /* 더 밝은 파란색 */

        text-shadow: 0 0 8px rgba(173, 216, 230, 0.5);

    }

    

    /* 일반 텍스트, 마크다운, 정보 박스 텍스트 스타일 */

    p, .stMarkdown, .stInfo {

        color: #E0FFFF; /* 아주 밝은 시안색 */

    }



    /* 사이드바 설정 설명 텍스트 스타일 (네모 박스 및 글자색 변경) */

    .stSidebar .setting-description {

        font-size: 0.85em; /* 글씨 크기 줄이기 */

        color: #B0E0E6; /* 새로운 글자색 (밝은 파랑) */

        background-color: rgba(30, 30, 60, 0.7); /* 배경색 (어두운 파랑/보라) */

        border: 1px solid #4682B4; /* 테두리 (중간 파랑) */

        border-radius: 5px; /* 모서리 둥글게 */

        padding: 8px 10px; /* 내부 여백 */

        margin-top: -5px; /* 위젯과의 간격 조정 */

        margin-bottom: 15px; /* 다음 위젯과의 간격 */

        line-height: 1.4;

    }



    /* 정보 박스 스타일 */

    .stInfo {

        background-color: rgba(10, 17, 40, 0.7);

        border-left: 5px solid #4682B4;

        border-radius: 5px;

        padding: 10px;

    }



    /* 슬라이더 값 텍스트 색상 */

    .stSlider > div > div > div > div {

        color: #87CEFA;

    }

    

    /* 숫자 입력 필드 스타일 */

    .stNumberInput input {

        color: #b0e0e6;

        background-color: rgba(15, 15, 42, 0.7);

        border: 1px solid #4682B4;

        border-radius: 5px;

    }

    

    /* 체크박스 스타일 */

    .stCheckbox > label > div:first-child {

        border-color: #87CEFA !important;

    }

    .stCheckbox > label > div:first-child > div {

        background-color: #4682B4 !important;

    }

    .stCheckbox label span {

        color: #E0FFFF;

    }



    /* 수평선 스타일 */

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



        background: linear-gradient(to right, #1A2A4A, #2A3A5A, #3A4A6A); /* 어둡고 깊은 파란색 그라데이션 */

        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);

    }

    

    .stButton > button:hover {

        background: linear-gradient(to right, #4682B4, #6A9CC9, #8DBBDD); /* 밝은 파란색 그라데이션 */

        transform: translateY(-3px); /* 약간 위로 이동 */

        box-shadow: 0 6px 20px rgba(70, 130, 180, 0.7); /* 더 강한 그림자 효과 */

    }



    /* Streamlit 버튼 텍스트 스타일 */

    .stButton > button > div > span {

        background-image: linear-gradient(to right, #00BFFF, #87CEFA, #ADD8E6); /* 글자색 그라데이션 */

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        color: transparent; /* fallback */

        text-shadow: 0 0 8px rgba(135, 206, 250, 0.6); /* 글자 그림자 효과 */

        font-weight: bold;

    }



    .stButton > button:hover > div > span {

        background-image: none; /* hover 시 글자 그라데이션 제거 */

        -webkit-background-clip: unset;

        -webkit-text-fill-color: unset;

        color: white; /* hover 시 글자색 흰색으로 변경 */

        text-shadow: none; /* 그림자 효과 제거 */

    }

    </style>

    """,

    unsafe_allow_html=True

)



# --- 시뮬레이션 계산 로직 (캐싱) ---

@st.cache_data

def calculate_magnification_data(lens_m: float, planet_m_ratio: float, planet_orb: float, phase: int, velocity: float) -> tuple[np.ndarray, np.ndarray]:

    """

    중력 마이크로렌징 현상에 따른 광원 별의 밝기 변화를 계산합니다.



    Args:

        lens_m (float): 렌즈 별의 질량 (태양 질량).

        planet_m_ratio (float): 행성 질량비 (렌즈 별 질량 대비).

        planet_orb (float): 행성 궤도 반지름 (Einstein Radius 단위).

        phase (int): 행성의 초기 위상 (도).

        velocity (float): 렌즈 별의 상대 속도 (km/s).



    Returns:

        tuple[np.ndarray, np.ndarray]: 시간 포인트와 해당 시간의 밝기 변화 (증폭률) 배열.

    """

    time_points = np.linspace(-15, 15, 300) # -15일에서 +15일까지 300개의 시간 포인트

    

    # 기본 렌즈 별에 의한 밝기 변화 (가우시안 함수 형태)

    # 50/velocity는 이벤트 지속 시간에 영향을 줍니다.

    magnification = 1.0 + np.exp(-(time_points / (50 / velocity))**2) * (lens_m * 0.5)



    # 행성 포함 시 추가적인 밝기 변화 모델링

    if planet_m_ratio > 0:

        # 행성 영향의 시간적 위치

        # planet_orb * cos(phase)는 행성의 궤도 위치에 따른 시간 지연/선행을 모의합니다.

        # velocity / 10은 시간 스케일을 맞추기 위한 조정값입니다.

        planet_influence_time = time_points - (planet_orb * np.cos(np.deg2rad(phase))) / (velocity / 10)

        

        # 행성에 의한 추가 밝기 변화 (또 다른 가우시안 형태의 작은 피크 또는 딥)

        # planet_m_ratio * 100은 행성 질량비에 따른 폭을, planet_m_ratio * 50은 높이를 조절합니다.

        magnification += np.exp(-( (planet_influence_time - 2)**2 / (0.5 + planet_m_ratio * 100)) ) * (planet_m_ratio * 50)

        

    return time_points, magnification



# --- Matplotlib 그래프 생성 함수 (캐싱) ---

@st.cache_resource

def plot_light_curve(time_points: np.ndarray, magnifications: np.ndarray) -> plt.Figure:

    """

    마이크로렌징 밝기 곡선을 Matplotlib으로 그립니다.



    Args:

        time_points (np.ndarray): 시간 포인트 배열.

        magnifications (np.ndarray): 각 시간 포인트에서의 밝기 변화 (증폭률) 배열.



    Returns:

        plt.Figure: 생성된 Matplotlib Figure 객체.

    """

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(time_points, magnifications, label="광원 별 밝기", color='#87CEEB') # 그래프 선 색상

    ax.set_xlabel("시간 (일)", fontsize=12, color='white')

    ax.set_ylabel("상대 밝기 / 증폭률", fontsize=12, color='white')

    ax.set_title("중력 마이크로렌징 밝기 곡선", fontsize=14, color='white')

    ax.grid(True, linestyle='--', alpha=0.7, color='#4682B4') # 그리드 스타일

    

    # y축 범위 자동 조정 (최소 0.8, 최대 2.5를 기준으로 데이터에 맞게 확장)

    ax.set_ylim(min(0.8, np.min(magnifications) * 0.9), max(2.5, np.max(magnifications) * 1.1))

    

    ax.legend(labelcolor='white') # 범례 글자색

    ax.tick_params(axis='x', colors='white') # x축 틱 색상

    ax.tick_params(axis='y', colors='white') # y축 틱 색상

    

    return fig



# --- 페이지 전환 콜백 함수 ---

def set_page(page_name: str):

    """

    Streamlit 세션 상태를 업데이트하여 페이지를 전환합니다.



    Args:

        page_name (str): 전환할 페이지의 이름 ('main', 'simulation', 'explanation').

    """

    st.session_state.page = page_name



# --- 1. 메인 페이지 함수 ---

def main_page():

    """앱의 시작 화면을 렌더링합니다."""

    st.title("🌌 우주 시뮬레이터")

    st.write("환영합니다! 아래 버튼을 눌러 시뮬레이션을 시작하거나 설명을 확인하세요.")

    st.markdown("---")



    # 두 개의 컬럼으로 버튼 배치

    col1, col2 = st.columns(2)



    with col1:

        st.button(

            "🚀 중력 마이크로렌징 시뮬레이션 시작",

            key="start_simulation_button",

            on_click=set_page,

            args=('simulation',), # 콜백 함수에 'simulation' 페이지 이름 전달

            use_container_width=True # 컨테이너 너비에 맞춤

        )



    with col2:

        st.button(

            "📚 시뮬레이션 설명 보기",

            key="view_explanation_button",

            on_click=set_page,

            args=('explanation',), # 콜백 함수에 'explanation' 페이지 이름 전달

            use_container_width=True

        )



# --- 2. 시뮬레이션 페이지 함수 ---

def simulation_page():

    """중력 마이크로렌징 밝기 곡선 시뮬레이션 페이지를 렌더링합니다."""

    st.title("✨ 중력 마이크로렌징 시뮬레이터")

    st.write("""

        이 앱은 **중력 마이크로렌징** 현상으로 인한 광원 별의 밝기 변화를 시뮬레이션합니다.

        아래 설정을 변경하여 밝기 곡선이 어떻게 변하는지 확인해 보세요!

    """)



    st.write("---")



    # --- 시뮬레이션 설정 입력 받기 (사이드바) ---

    st.sidebar.header("설정")



    # 광원 별 질량 설정

    source_mass = st.sidebar.number_input("광원 별 질량 (태양 질량)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

    st.sidebar.markdown('<p class="setting-description">배경에 있는 빛을 내는 별의 질량입니다. 값이 클수록 밝기 변화의 잠재적 규모가 커집니다.</p>', unsafe_allow_html=True)



    # 렌즈 별 질량 설정

    lens_mass = st.sidebar.number_input("렌즈 별 질량 (태양 질량)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)

    st.sidebar.markdown('<p class="setting-description">중력 렌즈 역할을 하는 별의 질량입니다. 질량이 클수록 빛을 더 강하게 휘게 합니다.</p>', unsafe_allow_html=True)



    # 렌즈 상대 속도 설정

    lens_velocity = st.sidebar.slider("렌즈 상대 속도 (km/s)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

    st.sidebar.markdown('<p class="setting-description">렌즈 별이 광원 별 앞을 지나가는 상대적인 속도입니다. 빠를수록 밝기 변화 현상이 짧아집니다.</p>', unsafe_allow_html=True)

    

    st.sidebar.subheader("행성 (Planet - 선택 사항)")

    has_planet = st.sidebar.checkbox("행성 포함", value=False)

    st.sidebar.markdown('<p class="setting-description">렌즈 별에 행성이 동반되어 있는지 설정합니다.</p>', unsafe_allow_html=True)



    # 행성 포함 시 추가 설정

    if has_planet:

        planet_mass_ratio = st.sidebar.slider("행성 질량비 (렌즈 별 질량 대비)", min_value=0.0001, max_value=0.1, value=0.001, format="%.4f")

        st.sidebar.markdown('<p class="setting-description">렌즈 별 질량 대비 행성의 질량 비율입니다. 높을수록 행성 신호가 뚜렷해집니다.</p>', unsafe_allow_html=True)

        

        planet_orbit_radius = st.sidebar.slider("행성 궤도 반지름 (Einstein Radius 단위)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)

        st.sidebar.markdown('<p class="setting-description">행성이 렌즈 별 주위를 도는 궤도의 크기입니다.</p>', unsafe_allow_html=True)

        

        planet_phase = st.sidebar.slider("행성 초기 위상 (도)", min_value=0, max_value=360, value=0, step=10)

        st.sidebar.markdown('<p class="setting-description">시뮬레이션 시작 시 행성의 궤도 상 초기 위치입니다.</p>', unsafe_allow_html=True)

    else:

        planet_mass_ratio = 0.0 # 행성 없으면 질량비 0

        planet_orbit_radius = 0.0 # 행성 없으면 궤도 반지름 0

        planet_phase = 0 # 행성 없으면 위상 0



    st.sidebar.write("---")

    st.sidebar.info("참고: 이 시뮬레이터의 밝기 곡선은 개념적인 모델에 기반하며, 실제 천체 물리 계산과 다를 수 있습니다.")



    # 밝기 곡선 데이터 계산

    time_points, magnifications = calculate_magnification_data(

        lens_mass, planet_mass_ratio, planet_orbit_radius, planet_phase,

        lens_velocity

    )



    # --- 배경별 광도 변화 (밝기 곡선) 그래프 표시 ---

    st.subheader("📈 배경별 광도 변화 (밝기 곡선)")

    st.write("""

        이 그래프는 렌즈 별이 배경 광원 별 앞을 지나갈 때,

        **배경 광원 별의 밝기가 시간 경과에 따라 어떻게 변하는지** 보여줍니다.

        **중력 렌즈 효과**로 인해 밝기가 일시적으로 증가하는 피크가 나타납니다.

        행성이 존재하면 이 피크에 미세한 추가적인 밝기 변화가 나타날 수 있습니다.

    """)

    fig_light_curve = plot_light_curve(time_points, magnifications)

    st.pyplot(fig_light_curve)

    plt.close(fig_light_curve) # Matplotlib Figure 객체 닫아 메모리 관리



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

    """중력 마이크로렌징에 대한 설명을 제공하는 페이지를 렌더링합니다."""

    st.title("📚 시뮬레이션 설명")

    st.write("""

    이 페이지에서는 중력 마이크로렌징 시뮬레이터의 작동 원리와 각 매개변수에 대한 자세한 설명을 제공합니다.

    """)

    st.markdown("---")



    st.subheader("중력 마이크로렌징이란?")

    st.write("""

    **중력 마이크로렌징(Gravitational Microlensing)**은 아인슈타인의 일반 상대성 이론에 의해 예측되는 현상으로,

    무거운 천체(**렌즈 별**)가 배경의 밝은 천체(**광원 별**) 앞을 지나갈 때, 렌즈 별의 중력이 광원 별에서 오는 빛을 휘게 하여

    광원 별의 밝기가 일시적으로 증가하는 현상을 말합니다. 이 현상을 통해 행성이나 블랙홀과 같이

    직접 관측하기 어려운 천체들을 간접적으로 발견할 수 있습니다.

    """)



    st.subheader("시뮬레이션 매개변수 설명")

    st.write("""

    - **광원 별 질량 (Source Star Mass):** 배경에 있는 빛을 내는 별의 질량입니다. 시뮬레이션에서는 밝기 변화의 스케일에 영향을 줍니다.

    - **렌즈 별 질량 (Lens Star Mass):** 중력 렌즈 역할을 하는 별의 질량입니다. 이 질량이 클수록 빛을 더 강하게 휘게 하여 밝기 변화가 커집니다.

    - **상대 속도 (Relative Velocity):** 렌즈 별이 광원 별 앞을 지나가는 상대적인 속도입니다. 속도가 빠를수록 밝기 변화 현상이 짧은 시간 동안 발생합니다.

    - **행성 포함 (Planet Inclusion):** 렌즈 별에 행성이 동반되어 있는지 여부를 설정합니다.

        - **행성 질량비 (Planet Mass Ratio):** 렌즈 별 질량 대비 행성의 질량 비율입니다. 이 비율이 클수록 행성에 의한 추가적인 밝기 변화 신호가 뚜렷해집니다.

        - **행성 궤도 반지름 (Planet Orbit Radius):** 행성이 렌즈 별 주위를 도는 궤도의 크기입니다. (아인슈타인 반지름 단위)

        - **행성 초기 위상 (Planet Initial Phase):** 시뮬레이션 시작 시 행성의 궤도 상의 초기 위치를 각도로 나타냅니다.

    """)



    st.subheader("시뮬레이션 결과 해석")

    st.info("""

    **밝기 곡선:** 렌즈 별이 배경 광원 별 앞을 지나갈 때 밝기가 일시적으로 증가하는 피크가 발생합니다.

    행성이 존재하면 이 피크에 짧고 특징적인 변동(추가 피크 또는 딥)을 만들어내어 행성의 존재를 암시합니다.

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

# 세션 상태에 'page'가 없으면 'main'으로 초기화

if 'page' not in st.session_state:

    st.session_state.page = 'main'



# 현재 페이지 상태에 따라 해당 페이지 함수 호출

if st.session_state.page == 'main':

    main_page()

elif st.session_state.page == 'simulation':

    simulation_page()

elif st.session_state.page == 'explanation':

    explanation_page()



# 하단 저작권 표시

st.caption("© 2025 중력 마이크로렌징 시뮬레이터")
