import streamlit as st

# Define your color
bg_color = "#c2c395"
title_color = "#DDBAAE"

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

st.write("my superb website")
st.header("the best website you will ever see")
st.subheader("so what is this website...?")
name = st.text_input("your name?")
