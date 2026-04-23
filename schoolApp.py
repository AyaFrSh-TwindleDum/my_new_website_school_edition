import streamlit as st

# 1. Initialize Memory (Session State)
if 'task_list' not in st.session_state:
    st.session_state.task_list = []

# Define colors
bg_color = "#c2c395"
title_color = "#4C3D19"
card_color = "#fdfae1"

# 2. CSS Styling
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    h1, h2, h3 {{ color: {title_color} !important; }}
    .task-card {{
        background-color: {card_color};
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid {title_color};
        margin-bottom: 15px;
        color: #333;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Sidebar Stats
with st.sidebar:
    st.header("📊 Task Stats")
    st.metric("Tasks to do", len(st.session_state.task_list))
    st.write("---")
    if st.button("🗑️ Clear All Tasks"):
        st.session_state.task_list = []
        st.rerun()

# 4. Main Title
st.header("📝 My Superb To-Do List")
st.write("Evaluate your laziness levels below.")

# 5. Input Section (Columns for layout)
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name of task", placeholder="e.g. Conquer the world")
    time_val = st.time_input("Time of task")

with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    # Adding the motivation bar back here!
    motivation = st.select_slider("Motivation Level", options=["Sloth", "Human", "Robot"])

# 6. Add Task Button
if st.button("Add Task"):
    if name:
        # Save task data + motivation level to memory
        new_task = {
            "name": name,
            "priority": priority,
            "time": time_val.strftime('%H:%M'),
            "motivation": motivation
        }
        st.session_state.task_list.append(new_task)
        st.success(f"Task '{name}' added!")
    else:
        st.error("Please enter a task name!")

st.divider()

# 7. Display All Tasks
st.subheader("Your Task List")

if not st.session_state.task_list:
    st.info("The list is empty. Are
