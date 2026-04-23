import streamlit as st

# 1. Page Config (Adds a title and icon to the browser tab)
st.set_page_config(page_title="Superb To-Do", page_icon="📝")

# Define your colors
bg_color = "#c2c395"
title_color = "#4C3D19"
card_color = "#fdfae1" # A light cream for the task card

# 2. Enhanced CSS
st.markdown(
    f"""
    <style>
    /* App Background */
    .stApp {{
        background-color: {bg_color};
    }}
    
    /* Header Styles */
    h1, h2, h3 {{
        color: {title_color} !important;
        font-family: 'Helvetica', sans-serif;
    }}

    /* Custom Task Card Styling */
    .task-card {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid {title_color};
        color: #333333;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Sidebar Decoration
with st.sidebar:
    st.title("Settings")
    st.image("https://cdn-icons-png.flaticon.com/512/4345/4345573.png", width=100)
    st.write("---")
    motivation = st.select_slider("Current Motivation Level", options=["Sloth", "Human", "Robot"])

# 4. Main App Layout
st.header("📝 To Do List")
st.write("My superb website will now evaluate your laziness.")

# Using Columns to make the layout look cleaner
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name of task", placeholder="e.g. Save the world")
    time_val = st.time_input("Time of task")

with col2:
    priority = st.select_slider("Priority of task", options=["Low", "Medium", "High"])

st.divider()

# 5. The Button & Results Logic
if st.button("Submit Task"):
    if name: 
        # Using HTML in Markdown to apply the 'task-card' class defined above
        st.markdown(f"""
            <div class="task-card">
                <h3>Task: {name}</h3>
                <p><b>Scheduled for:</b> {time_val.strftime('%H:%M')}<br>
                <b>Urgency:</b> {priority}<br>
                <b>Effort Mode:</b> {motivation}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Logic-based feedback
        if priority == "Low" and motivation == "Sloth":
            st.warning("Low priority and Sloth mode? This task is never happening, is it?")
        elif priority == "High":
            st.success("High priority! Let's get to work.")
        else:
            st.info("You've got this!")
    else:
        st.error("Please enter a task name first!")
