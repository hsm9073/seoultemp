import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 기온 배틀",
    page_icon="🔥",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080808, #1a0b03);
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 40px;
}

.title {
    text-align: center;
    font-size: 60px;
    font-weight: 900;
    color: #ff6b00;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #999;
    font-size: 18px;
    margin-bottom: 35px;
}

.card {
    background: linear-gradient(135deg, #261006, #120b08);
    border: 1px solid #ff6500;
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 0 35px rgba(255, 90, 0, 0.15);
}

.year {
    font-size: 70px;
    font-weight: 900;
}

.temp {
    font-size: 35px;
    font-weight: 900;
    color: #ff7518;
}

.rank {
    background: #151515;
    border: 1px solid #333;
    border-radius: 15px;
    padding: 15px 20px;
    margin: 8px 0;
    font-size: 20px;
}

.rank_temp {
    float: right;
    color: #ff8a32;
    font-weight: bold;
}

.section {
    font-size: 25px;
    font-weight: bold;
    margin-top: 35px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_csv("seoul.csv")

    data["날짜"] = pd.to_datetime(
        data["날짜"],
        errors="coerce"
    )

    data["평균기온"] = pd.to_numeric(
        data["평균기온"],
        errors="coerce"
    )

    data["최고기온"] = pd.to_numeric(
        data["최고기온"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["날짜", "평균기온"]
    )

    data["연도"] = data["날짜"].dt.year

    return data


try:
    df = load_data()
except Exception as e:
    st.error("seoul.csv 파일을 읽을 수 없습니다.")
    st.error("main.py와 seoul.csv가 같은 폴더에 있는지 확인해주세요.")
    st.stop()


st.markdown(
    '<div class="title">🔥 SEOUL HEAT BATTLE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">같은 날짜, 역대 최고의 더위를 찾아라</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section">📅 날짜를 선택하세요</div>',
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
    st.error("시작 날짜가 종료 날짜보다 늦습니다.")
    st.stop()


results = []

start_month = start_date.month
start_day = start_date.day
end_month = end_date.month
end_day = end_date.day


for year in sorted(df["연도"].unique()):

    try:
        start = pd.Timestamp(
            year=int(year),
            month=start_month,
            day=start_day
        )

        end = pd.Timestamp(
            year=int(year),
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

    except Exception:
        continue


result = pd.DataFrame(results)


if result.empty:
    st.warning("선택한 날짜에 비교할 데이터가 없습니다.")
    st.stop()


result["평균기온"] = result["평균기온"].round(1)
result["최고기온"] = result["최고기온"].round(1)


hottest = result.loc[
    result["평균기온"].idxmax()
]

coldest = result.loc[
    result["평균기온"].idxmin()
]


st.markdown(
    '<div class="section">🏆 가장 더웠던 해</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="card">
        <div style="font-size:15px;color:#ff9b52;">
            🔥 HEAT CHAMPION
        </div>

        <div class="year">
            {int(hottest["연도"])}년
        </div>

        <div class="temp">
            {hottest["평균기온"]:.1f} °C
        </div>

        <div style="color:#999;margin-top:10px;">
            선택한 기간의 평균기온이 가장 높았습니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section">📊 챔피언 기록</div>',
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
        "최고기온",
        f'{hottest["최고기온"]:.1f} °C'
    )

with c3:
    st.metric(
        "가장 시원했던 해",
        f'{int(coldest["연도"])}년'
    )


st.markdown(
    '<div class="section">⚔️ 연도별 기온 대결</div>',
    unsafe_allow_html=True
)

chart_data = result.sort_values("연도")

st.bar_chart(
    chart_data,
    x="연도",
    y="평균기온",
    height=450
)


st.markdown(
    '<div class="section">🔥 HOTTEST TOP 5</div>',
    unsafe_allow_html=True
)

top5 = result.sort_values(
    "평균기온",
    ascending=False
).head(5)


medals = ["🥇", "🥈", "🥉", "4위", "5위"]

for i, row in enumerate(top5.itertuples(index=False)):

    st.markdown(
        f"""
        <div class="rank">
            {medals[i]} &nbsp;
            <b>{row.연도}년</b>
            <span class="rank_temp">
                {row.평균기온:.1f} °C
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


with st.expander("📋 전체 결과 보기"):

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


st.markdown(
    """
    <div style="
        text-align:center;
        color:#555;
        margin-top:50px;
        padding:20px;
    ">
        🔥 SEOUL HEAT BATTLE
    </div>
    """,
    unsafe_allow_html=True
)
