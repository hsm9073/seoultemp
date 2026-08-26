import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SEOUL HEAT",
    page_icon="🔥",
    layout="wide"
)

# =========================
# 디자인
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, #351700 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #301000 0%, transparent 30%),
        #080808;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 45px;
}

.hero-small {
    color: #ff7900;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 5px;
}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    line-height: 1;
    margin-top: 10px;
    background: linear-gradient(90deg, white, #ffb347, #ff5c00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-text {
    color: #888;
    margin-top: 18px;
    font-size: 16px;
}

.line {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #ff6500,
        transparent
    );
    margin: 35px 0;
}

.section {
    font-size: 25px;
    font-weight: 900;
    margin: 30px 0 15px 0;
}

.winner {
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(255,80,0,.35),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            rgba(255,90,0,.25),
            rgba(255,180,0,.05)
        );
    border: 1px solid rgba(255,120,30,.6);
    border-radius: 25px;
    padding: 35px;
    box-shadow: 0 0 45px rgba(255,70,0,.15);
}

.winner-label {
    color: #ff9a3d;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 3px;
}

.winner-year {
    font-size: 75px;
    font-weight: 900;
    margin: 5px 0;
}

.winner-temp {
    font-size: 30px;
    font-weight: 800;
    color: #ff8424;
}

.winner-description {
    color: #999;
    margin-top: 8px;
}

.rank {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 15px;
    padding: 17px 22px;
    margin: 9px 0;
}

.rank-number {
    color: #ff7900;
    font-weight: 900;
    font-size: 21px;
}

.rank-year {
    font-size: 20px;
    font-weight: 800;
}

.rank-temp {
    float: right;
    color: #ff9a3d;
    font-size: 20px;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 데이터 불러오기
# =========================
@st.cache_data
def load_data():

    df = pd.read_csv("seoul.csv")

    # 날짜
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 숫자로 변환
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

    return df


df = load_data()


# =========================
# 제목
# =========================
st.markdown("""
<div class="hero-small">
SEOUL WEATHER DATA
</div>

<div class="hero-title">
WHEN WAS SEOUL<br>
THE HOTTEST?
</div>

<div class="hero-text">
원하는 날짜를 선택하면 같은 기간의 역대 기온을 비교합니다.
</div>

<div class="line"></div>
""", unsafe_allow_html=True)


# =========================
# 날짜 선택
# =========================
st.markdown(
    '<div class="section">📅 ANALYSIS PERIOD</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "시작 날짜",
        value=pd.Timestamp("2020-06-01").date()
    )

with col2:
    end_date = st.date_input(
        "종료 날짜",
        value=pd.Timestamp("2020-08-31").date()
    )


if start_date > end_date:
    st.error("⚠️ 시작 날짜가 종료 날짜보다 늦습니다.")
    st.stop()


# =========================
# 같은 월/일을 모든 연도에 적용
# =========================
start_month = start_date.month
start_day = start_date.day

end_month = end_date.month
end_day = end_date.day


results = []

for year in sorted(df["연도"].unique()):

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

        period = df[
            (df["날짜"] >= start) &
            (df["날짜"] <= end)
        ]

        if len(period) >= 5:

            results.append({
                "연도": int(year),
                "평균기온": period["평균기온"].mean(),
                "최고기온": period["최고기온"].max(),
                "측정일수": len(period)
            })

    except:
        pass


result = pd.DataFrame(results)


if result.empty:
    st.warning("선택한 기간의 데이터가 없습니다.")
    st.stop()


# =========================
# 결과 계산
# =========================
result["평균기온"] = result["평균기온"].round(1)
result["최고기온"] = result["최고기온"].round(1)

hottest = result.loc[
    result["평균기온"].idxmax()
]


# =========================
# 가장 더운 해
# =========================
st.markdown(
    '<div class="section">🔥 THE HOTTEST YEAR</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="winner">

<div class="winner-label">
#1 HOTTEST YEAR
</div>

<div class="winner-year">
{int(hottest["연도"])}년
</div>

<div class="winner-temp">
{hottest["평균기온"]:.1f} °C
</div>

<div class="winner-description">
선택한 기간 동안 평균기온이 가장 높았던 해
</div>

</div>
""", unsafe_allow_html=True)


# =========================
# 핵심 정보
# =========================
st.markdown(
    '<div class="section">📌 KEY NUMBERS</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "기간 평균기온",
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
        f'{len(result)}개'
    )


# =========================
# 그래프
# =========================
st.markdown(
    '<div class="section">📊 YEAR BY YEAR</div>',
    unsafe_allow_html=True
)

chart_data = result.sort_values("연도")

st.bar_chart(
    chart_data,
    x="연도",
    y="평균기온",
    height=450
)


# =========================
# TOP 5
# =========================
st.markdown(
    '<div class="section">🏆 HOTTEST TOP 5</div>',
    unsafe_allow_html=True
)

top5 = result.sort_values(
    "평균기온",
    ascending=False
).head(5)


for i, row in enumerate(
    top5.itertuples(index=False),
    start=1
):

    if i == 1:
        medal = "🥇"
    elif i == 2:
        medal = "🥈"
    elif i == 3:
        medal = "🥉"
    else:
        medal = str(i)

    st.markdown(f"""
    <div class="rank">

        <span class="rank-number">
        {medal}
        </span>

        &nbsp;&nbsp;

        <span class="rank-year">
        {row.연도}년
        </span>

        <span class="rank-temp">
        {row.평균기온:.1f} °C
        </span>

    </div>
    """, unsafe_allow_html=True)


# =========================
# 전체 데이터
# =========================
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


# =========================
# 하단
# =========================
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
