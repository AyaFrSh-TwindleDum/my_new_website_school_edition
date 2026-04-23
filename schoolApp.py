import streamlit as st

# Define your color
bg_color = "#c2c395"

# Inject CSS with markdown
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.write("my superb website")
st.header("the best website you will ever see")
st.subheader("so what is this website...?")
name = st.text_input("your name?")
