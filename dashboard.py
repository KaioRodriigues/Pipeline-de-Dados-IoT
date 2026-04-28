import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL)


def carregar_dados(sql):
    return pd.read_sql(sql, engine)


st.set_page_config(page_title="Dashboard de Temperaturas IoT", layout="wide")

st.title("Dashboard de Temperaturas IoT")
st.write("Os dados exibidos vêm de leituras de temperatura registradas por dispositivos IoT.")

try:
    dados = carregar_dados("SELECT * FROM temperature_readings ORDER BY timestamp DESC")
    media_dispositivo = carregar_dados("SELECT * FROM avg_temp_por_dispositivo ORDER BY avg_temp DESC")
    leituras_hora = carregar_dados("SELECT * FROM leituras_por_hora ORDER BY hora")
    temp_dia = carregar_dados("SELECT * FROM temp_max_min_por_dia ORDER BY dia")
except Exception as erro:
    st.error("Nao foi possivel carregar os dados do PostgreSQL.")
    st.info("Confira se o Docker esta rodando e se o pipeline ja foi executado.")
    st.exception(erro)
    st.stop()

if dados.empty:
    st.warning("A tabela ainda nao possui dados.")
    st.stop()

total_leituras = len(dados)
media_geral = dados["temperature"].mean()
maior_temp = dados["temperature"].max()
menor_temp = dados["temperature"].min()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de leituras", f"{total_leituras}")
col2.metric("Media geral", f"{media_geral:.2f} °C")
col3.metric("Maior temperatura", f"{maior_temp:.2f} °C")
col4.metric("Menor temperatura", f"{menor_temp:.2f} °C")

st.subheader("Media de temperatura por dispositivo")
fig1 = px.bar(
    media_dispositivo,
    x="device_id",
    y="avg_temp",
    labels={"device_id": "Dispositivo", "avg_temp": "Media de temperatura"},
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Quantidade de leituras por hora")
fig2 = px.line(
    leituras_hora,
    x="hora",
    y="total_leituras",
    markers=True,
    labels={"hora": "Hora do dia", "total_leituras": "Total de leituras"},
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Temperatura maxima e minima por dia")
fig3 = px.line(
    temp_dia,
    x="dia",
    y=["temp_max", "temp_min"],
    markers=True,
    labels={"dia": "Dia", "value": "Temperatura", "variable": "Tipo"},
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Amostra dos dados")
st.dataframe(dados.head(50), use_container_width=True)
