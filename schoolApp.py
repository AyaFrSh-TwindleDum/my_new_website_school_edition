import streamlit as st

# Define your color
bg_color = "#c2c395"
title_color = "#4C3D19"

# Inject CSS with markdown
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    
    }}
    h1, h2, h3 {{
        color: {title_color} !important;
    }}
    </style>
   
    """,
    unsafe_allow_html=True
)
st.header("To Do List")
name = st.text_input("name of task")
prioraty= st.text_input("prioraty of task")
time = st.text_input("time of task"
st.write("my superb website")
