import streamlit as st

st.title("🔎 Consulta")

st.caption("MVP (Sprint 0): tela placeholder. No Sprint 3 virará a consulta real no banco.")

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Marca", ["(exemplo) Ford", "(exemplo) Toyota", "(exemplo) Fiat"])
with col2:
    model = st.selectbox("Modelo", ["(exemplo) Ka", "(exemplo) Corolla", "(exemplo) Argo"])

if st.button("Consultar"):
    st.success(f"Consulta simulada: {brand} / {model}")
    st.write("Resultado (mock): R$ 0,00")
