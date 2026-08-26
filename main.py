```python
import streamlit as st
import pandas as pd

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="SEOUL HEAT INDEX",
    page_icon="🔥",
    layout="wide"
)

# =========================================================
# CSS - 다크 & 네온 스타일
# =========================================================
st.markdown("""
<style>

    /* 전체 배경 */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #2b1700 0%, transparent 30%),
            radial-gradient(circle at 90% 20%, #351000 0%, transparent 30%),
            #080808;
        color: #ffffff;
    }

    /* 기본 폰트 */
    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    /* 상단 여백 */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* 메인 타이틀 */
    .hero {
        padding: 20px 0 35px 0;
    }

    .hero-small {
        color: #ff7a00;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 4px;
        margin-bottom: 8px;
    }

    .hero-title {
        font-size: 58px;
        font-weight: 900;
        letter-spacing: -3px;
        line-height: 1;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #ffb347, #ff5e00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #999999;
        font-size: 16px;
        margin-top: 15px;
    }

    /* 구분선 */
    .line {
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #ff6500,
            transparent
        );
        margin: 20px 0 30px 0;
    }

    /* 카드 */
    .card {
        background: linear-gradient(
            145deg,
            rgba(255, 102, 0, 0.16),
            rgba(255, 255, 255, 0.035)
        );
        border: 1px solid rgba(255, 110, 0, 0.35);
        border-radius: 20px;
        padding: 28px;
        box-shadow:
            0 0 30px rgba(255, 80, 0, 0.08),
            inset 0 1px rgba(255,255,255,0.08);
    }

    /* 最热年 */
    .winner-card {
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(255, 80, 0, 0.35),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                rgba(255, 90, 0, 0.25),
                rgba(255, 180, 0, 0.05)
            );

        border: 1px solid rgba(255, 120, 30, 0.65);
        border-radius: 24px;
        padding: 35px;
        box-shadow:
            0 0 45px rgba(255, 70, 0, 0.14),
            inset 0 1px rgba(255,255,255,0.1);
    }

    .winner-label {
        color: #ff9b42;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 3px;
    }

    .winner-year {
        font-size: 76px;
        font-weight: 950;
        line-height: 1;
        margin: 10px 0;
        color: white;
    }

    .winner-temp {
        font-size: 30px;
        font-weight: 800;
        color: #ff8a24;
    }

    .winner-text {
        color: #aaaaaa;
        margin-top: 10px;
    }

    /* 섹션 제목 */
    .section-title {
        font-size: 25px;
        font-weight: 850;
        margin: 35px 0 15px 0;
    }

    /* 순위 */
    .rank-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 16px 20px;
        margin-bottom: 10px;
        transition: 0.2s;
    }

    .rank-card:hover {
        border-color: rgba(255,100,0,0.5);
        background: rgba(255,100,0,0.06);
    }

    .rank-number {
        font-size: 22px;
        font-weight: 900;
        color: #ff7b00;
    }

    .rank-year {
        font-size: 20px;
        font-weight: 800;
    }

    .rank-temp {
        font-size: 20px;
        font-weight: 800;
        color: #ff9a3c;
        float: right;
    }

    /* Streamlit 입력창 */
    div[data-baseweb="input"],
    div[data-baseweb="select"] {
        background-color: #151515 !important;
    }

    /* metric */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 16px;
    }

    /* 데이터프레임 */
    div[data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }

    /* 작은 글씨 */
    .muted {
        color: #777777;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# 데이터 불러오기
# =========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("seoul.csv")

    df["날짜"] = df["날짜"].astype(str).str.strip()
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    df["최고기온"] = pd.to_numeric(
        df["최고기온"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["날짜", "평균기온"]
    )

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">

    <div class="hero-small">
        SEOUL WEATHER DATA
    </div>

    <div class="hero-title">
        WHEN WAS SEOUL<br>
        THE HOTTEST?
    </div>

    <div class="hero-description">
        원하는 날짜를 선택하고, 같은 기간의 역대 기온을 비교해보세요.
    </div>

</div>

<div class="line"></div>
""", unsafe_allow_html=True)


# =========================================================
# 날짜 선택
# =========================================================
st.markdown(
    '<div class="section-title">📅 분석 기간</div>',
    unsafe_allow_html=True
)

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "START",
        value=pd.Timestamp("2020-06-01").date()
    )

with date_col2:
    end_date = st.date_input(
        "END",
        value=pd.Timestamp("2020-08-31").date()
    )


if start_date > end_date:
    st.error("START 날짜가 END 날짜보다 늦습니다.")
    st.stop()


# =========================================================
# 기간 데이터 계산
# =========================================================
start_month = start_date.month
start_day = start_date.day

end_month = end_date.month
end_day = end_date.day


def get_period_data(data):

    results = []

    for year in sorted(data["연도"].unique()):

        try:

            start = pd.Timestamp(
                year=year,
                month=start_month,
                day=start_day
            )

            end = pd.Timestamp(
                year=year,
                month=end_month,
                day=end_day
            )

            period = data[
                (data["날짜"] >= start) &
                (data["날짜"] <= end)
            ]

            if len(period) >= 5:

                results.append({
                    "연도": int(year),
                    "평균기온": period["평균기온"].mean(),
                    "최고기온": period["최고기온"].max(),
                    "측정일수": len(period)
                })

        except:

            continue

    return pd.DataFrame(results)


result = get_period_data(df)


if result.empty:
    st.warning("선택한 기간에 비교할 수 있는 데이터가 없습니다.")
    st.stop()


# =========================================================
# 결과 계산
# =========================================================
result["평균기온"] = result["평균기온"].round(1)
result["최고기온"] = result["최고기온"].round(1)

hottest = result.loc[
    result["평균기온"].idxmax()
]


# =========================================================
# WINNER
# =========================================================
st.markdown(
    '<div class="section-title">🔥 THE HOTTEST YEAR</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="winner-card">

    <div class="winner-label">
        #1 HOTTEST YEAR
    </div>

    <div class="winner-year">
        {int(hottest["연도"])}
    </div>

    <div class="winner-temp">
        {hottest["평균기온"]:.1f} °C
    </div>

    <div class="winner-text">
        선택한 기간의 평균기온이 가장 높았던 해입니다.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 핵심 수치
# =========================================================
st.markdown(
    '<div class="section-title">📌 KEY NUMBERS</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "평균기온",
        f'{hottest["평균기온"]:.1f} °C'
    )

with c2:
    st.metric(
        "기간 최고기온",
        f'{hottest["최고기온"]:.1f} °C'
    )

with c3:
    st.metric(
        "비교한 연도",
        f'{len(result)}년'
    )


# =========================================================
# 그래프
# =========================================================
st.markdown(
    '<div class="section-title">📈 YEAR BY YEAR</div>',
    unsafe_allow_html=True
)

chart = result.sort_values("연도").set_index("연도")

st.bar_chart(
    chart["평균기온"],
    height=420
)

st.markdown(
    '<div class="muted">선택한 날짜 구간의 연도별 평균기온</div>',
    unsafe_allow_html=True
)


# =========================================================
# TOP 5
# =========================================================
st.markdown(
    '<div class="section-title">🏆 HOTTEST TOP 5</div>',
    unsafe_allow_html=True
)

top5 = result.sort_values(
    "평균기온",
    ascending=False
).head(5).reset_index(drop=True)


for i, row in top5.iterrows():

    rank = i + 1

    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"
    else:
        medal = f"{rank}"

    st.markdown(f"""
    <div class="rank-card">

        <span class="rank-number">
            {medal}
        </span>

        &nbsp;&nbsp;

        <span class="rank-year">
            {int(row["연도"])}년
        </span>

        <span class="rank-temp">
            {row["평균기온"]:.1f} °C
        </span>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 상세 데이터
# =========================================================
with st.expander("📋 전체 데이터 보기"):

    table = result.sort_values(
        "평균기온",
        ascending=False
    ).copy()

    table.columns = [
        "연도",
        "기간 평균기온 (°C)",
        "기간 최고기온 (°C)",
        "측정일수"
    ]

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<br><br>

<div style="
    text-align:center;
    color:#555;
    font-size:12px;
    padding:30px;
">

    SEOUL HEAT INDEX<br>
    Weather Data Visualization

</div>
""", unsafe_allow_html=True)
```
