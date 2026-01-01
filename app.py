import streamlit as st

from pension.config import MONTHLY_CONTRIBUTION
from pension.simulation import run_simulation

st.title("国民年金シミュレーター (Japanese Pension Simulator)")

st.subheader("このシミュレーターについて")

st.text("海外に転出した日本人は、国民年金への加入が任意となります。このシミュレーターでは、任意加入して国民年金を受給した場合と、任意加入せずにその分を投資に回した場合の将来価値を比較します。")

st.text("入力パラメーターは、年金の支払い期間と受給期間、日本の金利、海外での投資リターン、為替レート、支払い期間と受給期間を除く各パラメーターの標準偏差です。また、国民年金を日本円で受け取るか、外貨に両替するかを選択できます。これらのインプットをもとに、国民年金の現在価値と投資の価値の平均値、そして年金が投資を上回る確率を計算します。")

st.markdown(":small[このシミュレーターでは、国民年金の月額支払額を2025年度の17,510円、満額受給額を831,700円として計算しています。なお、障害年金・遺族年金および各種手数料については考慮していません。本シミュレーターは、作者による日本の国民年金制度に関する理解をもとに作成されていますが、内容に誤りや不備やございましたら、ご指摘いただけますと幸いです。]")

st.subheader("シミュレーター")

currency = st.radio(
    "年金を受け取る通貨 (Output currency)",
    options=["JPY", "Foreign currency"],
    format_func=lambda x: "日本円 (JPY)" if x == "JPY" else "外貨建て (Foreign currency)",
)

years_of_contribution = st.slider("年金の支払い期間 (Years of contribution)", 1, 40, 25)
years_to_receive = st.slider("年金の受給期間 (Years to receive pension)", 1, 40, 25)
annual_interest_rate = st.number_input(f"{'日本' if currency == 'JPY' else '海外'}の金利 (%) (Interest rate)", 0.0, 15.0, 1.0)
annual_interest_rate_sd = st.number_input(f"{'日本' if currency == 'JPY' else '海外'}の金利 (%) 標準偏差", 0.0, 15.0, 0.5)
annual_return = st.number_input("海外での投資リターン (%) (Foreign investment return)", 0.0, 30.0, 5.0)
annual_return_sd = st.number_input("海外での投資リターン (%) 標準偏差", 0.0, 30.0, 2.5)
exchange_rate = st.number_input("為替レート (¥) (Exchange rate)", 0.0, 1000.0, 200.0)
exchange_rate_sd = st.number_input("為替レート (¥) 標準偏差", 0.0, 1000.0, 20.0)

with st.spinner("シミュレーション実行中..."):
    fig, pension_better_ratio, mean_pension, mean_investment = run_simulation(
            years_to_receive=years_to_receive,
            interest_rate_mean=annual_interest_rate,
            interest_rate_sd=annual_interest_rate_sd,
            years_of_contribution=years_of_contribution,
            exchange_rate_mean=exchange_rate,
            exchange_rate_sd=exchange_rate_sd,
            return_mean=annual_return,
            return_sd=annual_return_sd,
            currency_jpy=(currency == "JPY"),
        )

    st.metric("年金の現在価値の平均値", f"{'¥' if currency == 'JPY' else '$'}{mean_pension:,.0f}")
    st.metric("投資の価値の平均値", f"{'¥' if currency == 'JPY' else '$'}{mean_investment:,.0f}")
    st.pyplot(fig)
    st.metric(
        "国民年金が投資を上回る確率",
        f"{pension_better_ratio:.2%}",
    )

