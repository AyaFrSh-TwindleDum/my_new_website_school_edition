import streamlit as st

# Define your colors
bg_color = "#c2c395"
title_color = "#4C3D19"

# Inject CSS
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
st.write("My superb website will now evaluate your laziness.")

# Input fields
name = st.text_input("Name of task")
priority = st.select_slider("Priority of task", options=["Low", "Medium", "High"])
time_val = st.time_input("Time of task")

# The Button Logic
if st.button("Submit Task"):
    if name: # Check if the user actually typed a name
        st.divider()
        st.subheader("Task Summary")
        st.write(f"**Task:** {name}")
        st.write(f"**Priority:** {priority}")
        st.write(f"**Scheduled Time:** {time_val.strftime('%H:%M')}")
        
        # A little "laziness evaluation" joke
        if priority == "Low":
            st.warning("Low priority? Classic procrastination move.")
        else:
            st.success("High priority! Look at you being productive.")
    else:
        st.error("Please enter a task name first!")
