import streamlit as st

# 1. INITIALIZE MEMORY (Session State)
# This code only runs once when the app starts.
if 'task_list' not in st.session_state:
    st.session_state.task_list = []

# Define colors
bg_color = "#c2c395"
title_color = "#4C3D19"

# 2. CSS STYLING
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    h1, h2, h3 {{ color: {title_color} !important; }}
    .task-card {{
        background-color: #fdfae1;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid {title_color};
        margin-bottom: 10px;
        color: #333;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. SIDEBAR (Counter)
with st.sidebar:
    st.header("📊 Stats")
    # Show how many tasks are in our 'memory'
    st.metric("Total Tasks", len(st.session_state.task_list))
    
    if st.button("🗑️ Clear All Tasks"):
        st.session_state.task_list = []
        st.rerun()

# 4. INPUT SECTION
st.header("To Do List")
st.write("Add your tasks below. I'll remember them (until you refresh the page).")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name of task", key="name_input")
    time_val = st.time_input("Time of task")
with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])

# 5. THE BUTTON LOGIC (Adding to memory)
if st.button("Add Task"):
    if name:
        # Create a dictionary for the new task
        new_entry = {
            "name": name,
            "priority": priority,
            "time": time_val.strftime('%H:%M')
        }
        # Append the task to our session_state list
        st.session_state.task_list.append(new_entry)
    else:
        st.error("Please enter a task name first!")

st.divider()

# 6. DISPLAY SECTION (Showing all tasks)
st.subheader("Current Tasks")

if not st.session_state.task_list:
    st.info("No tasks added yet. Get to work!")
else:
    # We loop through the list in reverse so the newest task is at the top
    for task in reversed(st.session_state.task_list):
        st.markdown(f"""
            <div class="task-card">
                <strong>{task['name']}</strong><br>
                <small>⏰ {task['time']} | 🚩 {task['priority']} Priority</small>
            </div>
        """, unsafe_allow_html=True)
