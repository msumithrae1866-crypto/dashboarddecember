import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

st.title("📊 Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    
    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("🔍 Basic Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    st.subheader("🔦 Column Selection for Visualization")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_x = st.selectbox("Select X-axis", options=numeric_cols)
    selected_y = st.selectbox("Select Y-axis", options=numeric_cols)

    chart_type = st.radio("Choose Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart"])

    if chart_type == "Scatter Plot":
        fig = px.scatter(df, x=selected_x, y=selected_y)
    elif chart_type == "Line Chart":
        fig = px.line(df, x=selected_x, y=selected_y)
    else:
        fig = px.bar(df, x=selected_x, y=selected_y)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔗 Correlation Heatmap")
    fig_corr = px.imshow(df.corr(), text_auto=True)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("📌 Pivot Table")
    all_columns = df.columns.tolist()
    pivot_index = st.selectbox("Select Row Field", options=all_columns)
    pivot_values = st.selectbox("Select Value Field", options=numeric_cols)

    pivot_df = df.pivot_table(index=pivot_index, values=pivot_values, aggfunc="mean").reset_index()
    st.dataframe(pivot_df)

else:
    st.info("👆 Upload a CSV file to start the dashboard.")
