import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, SympifyError

# --- 페이지 설정 ---
st.set_page_config(
    page_title="다기능 계산기 & 그래프",
    layout="wide"
)

st.title("🔢 다기능 계산기 & 📈 다항함수 그래프 웹앱")
st.markdown("---")

# --- 탭 구성 ---
tab1, tab2 = st.tabs(["🧮 계산기", "📊 함수 그래프"])

with tab1:
    st.header("🧮 계산기")

    # --- 계산 함수 정의 ---
    def calculate(num1, operation, num2=None):
        """
        선택된 연산에 따라 계산을 수행하는 함수.
        이항 연산(사칙, 모듈러, 지수)과 단항 연산(로그)을 모두 처리합니다.
        """
        try:
            # 사칙연산, 모듈러 연산, 지수 연산 (이항 연산)
            if operation == '+':
                return num1 + num2
            elif operation == '-':
                return num1 - num2
            elif operation == '*':
                return num1 * num2
            elif operation == '/':
                if num2 == 0:
                    st.error("오류: 0으로 나눌 수 없습니다.")
                    return None
                return num1 / num2
            elif operation == '% (모듈러)':
                return num1 % num2
            elif operation == '** (지수)':
                return num1 ** num2
            
            # 로그 연산 (단항 연산)
            elif operation == 'log (밑 10)':
                if num1 <= 0:
                    st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                    return None
                return math.log10(num1)
            
            # 자연로그 연산 (추가)
            elif operation == 'ln (자연로그)':
                if num1 <= 0:
                    st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                    return None
                return math.log(num1) # math.log()는 자연로그 (밑 e)입니다.

        except TypeError:
            st.error("오류: 유효한 숫자를 입력하세요.")
            return None
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")
            return None

    # --- UI 구성 ---

    # 1. 숫자 입력 및 연산자 선택
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.subheader("입력")
        
        # 연산 선택
        operation = st.selectbox(
            "**수행할 연산을 선택하세요**",
            ('+', '-', '*', '/', '% (모듈러)', '** (지수)', 'log (밑 10)', 'ln (자연로그)'),
            key='calculator_operation_select' # 키 추가
        )
        
        # 연산에 따라 입력 필드 다르게 표시
        if operation in ['log (밑 10)', 'ln (자연로그)']:
            # 단항 연산 (로그)
            num1 = st.number_input("**숫자 (진수)**", value=10.0, step=0.1, key='calculator_num1_log')
            num2 = None # 사용하지 않음
            st.caption("로그 연산은 **첫 번째 입력 값**을 진수로 사용합니다.")
        else:
            # 이항 연산 (사칙, 모듈러, 지수)
            num1 = st.number_input("**첫 번째 숫자 (Operand 1)**", value=10.0, step=0.1, key='calculator_num1')
            num2 = st.number_input("**두 번째 숫자 (Operand 2)**", value=5.0, step=0.1, key='calculator_num2')
        
    with col2:
        st.subheader("연산")
        st.markdown(f"## {operation}")

    with col3:
        st.subheader("결과")
        
        # 2. 계산 버튼
        if st.button("계산하기 🟰", key='calculate_button', help="입력된 값으로 계산을 수행합니다.", use_container_width=True):
            
            # 3. 계산 및 결과 표시
            result = calculate(num1, operation, num2)
            
            if result is not None:
                st.success(f"**결과:**")
                st.markdown(f"## `{result:.4f}`") # 소수점 4자리까지 표시
            
    st.markdown("---")

    # --- 기능 설명 ---
    st.info("""
    ### ✨ 계산기 기능
    * **사칙연산:** `+`, `-`, `*`, `/` (더하기, 빼기, 곱하기, 나누기)
    * **모듈러 연산:** `% (나머지)`
    * **지수 연산:** `** (거듭제곱)`
    * **로그 연산:** `log (밑 10)` (상용로그), `ln (자연로그)` (밑 $e$)
    """)

with tab2:
    st.header("📊 다항함수 그래프 그리기")
    st.info("""
    'x'를 변수로 사용하여 다항함수를 입력하세요. (예: `x**2 + 2*x - 1`)
    지원되는 연산: `+`, `-`, `*`, `/`, `**` (거듭제곱), `sqrt()`, `sin()`, `cos()`, `tan()`, `log()`, `exp()` 등.
    """)

    # --- 함수 입력 ---
    function_str = st.text_input(
        "**함수 f(x)를 입력하세요**",
        value="x**2",
        help="예: x**2 + 2*x - 1, sin(x), exp(x)",
        key='function_input'
    )

    # --- x 범위 설정 ---
    col_x_min, col_x_max = st.columns(2)
    with col_x_min:
        x_min = st.number_input("**x 최소값**", value=-5.0, step=0.5, key='x_min_input')
    with col_x_max:
        x_max = st.number_input("**x 최대값**", value=5.0, step=0.5, key='x_max_input')

    # --- 그래프 그리기 버튼 ---
    if st.button("그래프 그리기 📈", key='draw_graph_button', use_container_width=True):
        if x_min >= x_max:
            st.error("오류: x 최소값은 x 최대값보다 작아야 합니다.")
        else:
            try:
                x = symbols('x')
                
                # 안전하게 사용자 입력을 수식으로 변환
                # eval 대신 sympy.sympify를 사용하여 안전성 강화
                expr = sympify(function_str)
                
                # x 값 생성
                x_vals = np.linspace(x_min, x_max, 500)
                
                # y 값 계산
                # sympy.lambdify를 사용하면 더욱 효율적일 수 있으나,
                # 여기서는 간단하게 반복문으로 처리
                y_vals = [expr.subs(x, val) for val in x_vals]
                
                # Plotly 그래프 생성
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'f(x) = {function_str}'))
                
                fig.update_layout(
                    title=f'함수 그래프: {function_str}',
                    xaxis_title='x',
                    yaxis_title='f(x)',
                    hovermode='x unified',
                    template="plotly_white", # 깔끔한 배경
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)

            except SympifyError:
                st.error("오류: 유효한 다항함수 형식이 아닙니다. 'x'를 변수로 사용하고, 올바른 연산자를 사용했는지 확인하세요.")
                st.caption("예시: `x**2 + 3*x - 5`, `sin(x)`, `exp(x)`")
            except Exception as e:
                st.error(f"그래프를 그리는 중 오류가 발생했습니다: {e}")

#import streamlit as st
import math

# --- 페이지 설정 ---
st.set_page_config(
    page_title="다기능 계산기",
    layout="wide"
)

st.title("🔢 다기능 계산기 웹앱")
st.markdown("---")

# --- 계산 함수 정의 ---

def calculate(num1, operation, num2=None):
    """
    선택된 연산에 따라 계산을 수행하는 함수.
    이항 연산(사칙, 모듈러, 지수)과 단항 연산(로그)을 모두 처리합니다.
    """
    try:
        # 사칙연산, 모듈러 연산, 지수 연산 (이항 연산)
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                st.error("오류: 0으로 나눌 수 없습니다.")
                return None
            return num1 / num2
        elif operation == '% (모듈러)':
            return num1 % num2
        elif operation == '** (지수)':
            return num1 ** num2
        
        # 로그 연산 (단항 연산)
        elif operation == 'log (밑 10)':
            if num1 <= 0:
                st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                return None
            return math.log10(num1)
        
        # 자연로그 연산 (추가)
        elif operation == 'ln (자연로그)':
            if num1 <= 0:
                st.error("오류: 로그의 진수는 0보다 커야 합니다.")
                return None
            return math.log(num1) # math.log()는 자연로그 (밑 e)입니다.

    except TypeError:
        st.error("오류: 유효한 숫자를 입력하세요.")
        return None
    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다: {e}")
        return None

# --- UI 구성 ---

# 1. 숫자 입력 및 연산자 선택
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("입력")
    
    # 연산 선택
    operation = st.selectbox(
        "**수행할 연산을 선택하세요**",
        ('+', '-', '*', '/', '% (모듈러)', '** (지수)', 'log (밑 10)', 'ln (자연로그)')
    )
    
    # 연산에 따라 입력 필드 다르게 표시
    if operation in ['log (밑 10)', 'ln (자연로그)']:
        # 단항 연산 (로그)
        num1 = st.number_input("**숫자 (진수)**", value=10.0, step=0.1)
        num2 = None # 사용하지 않음
        st.caption("로그 연산은 **첫 번째 입력 값**을 진수로 사용합니다.")
    else:
        # 이항 연산 (사칙, 모듈러, 지수)
        num1 = st.number_input("**첫 번째 숫자 (Operand 1)**", value=10.0, step=0.1)
        num2 = st.number_input("**두 번째 숫자 (Operand 2)**", value=5.0, step=0.1)
    
with col2:
    st.header("연산")
    st.markdown(f"## {operation}")

with col3:
    st.header("결과")
    
    # 2. 계산 버튼
    if st.button("계산하기 🟰", key='calculate_button', help="입력된 값으로 계산을 수행합니다.", use_container_width=True):
        
        # 3. 계산 및 결과 표시
        result = calculate(num1, operation, num2)
        
        if result is not None:
            st.success(f"**결과:**")
            st.markdown(f"## `{result:.4f}`") # 소수점 4자리까지 표시
        
st.markdown("---")

# --- 기능 설명 ---
st.info("""
### ✨ 구현된 기능
* **사칙연산:** `+`, `-`, `*`, `/` (더하기, 빼기, 곱하기, 나누기)
* **모듈러 연산:** `% (나머지)`
* **지수 연산:** `** (거듭제곱)`
* **로그 연산:** `log (밑 10)` (상용로그), `ln (자연로그)` (밑 $e$)
""")

#
