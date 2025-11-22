
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import requests

@st.cache_resource


def currency():

    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url).json()

    rates = response.get("rates", {})

    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    df_sorted = df.sort_values("Rate", ascending=False).head(20)

    st.title("Valuuttakurssit (USD → muut valuutat)")
    st.dataframe(df_sorted)

    fig = px.bar(df_sorted, x="Currency", y="Rate", title="Top 20 valuuttakurssia USD:sta")
    st.plotly_chart(fig)

def mySql():

    # Initialize connection.
    conn = st.connection('mysql', type='sql')

    # Perform query.
    df = conn.query('SELECT pvm, lt FROM temperatures LIMIT 100;', ttl=600)
    return df

def mySql2():

    conn = mysql.connector.connect(host='localhost', user='MY_USER',
    password='MY_USER_PASSWORD', database='weather_db')
    df = pd.read_sql('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50',
    conn)
    conn.close()
    return df

def main():
    st.title("Plot data from MySql")
    st.write("Temperatures")

    data = mySql()  # df sisältää sarakkeet pvm ja lt

    # Plotly-kaavion luonti
    fig = px.line(
        data,
        x="pvm",
        y="lt",
        title="Lämpötila / celsius",
        labels={"pvm": "Päivämäärä", "lt": "Lämpötila (°C)"},
    )

    st.plotly_chart(fig, use_container_width=True)
    st.title('Viikkotehtävä 4')
    data2 = mySql2()
    st.title('Säädata Oulusta')
    st.dataframe(data2)

    currency()

if __name__ == "__main__":
    main()