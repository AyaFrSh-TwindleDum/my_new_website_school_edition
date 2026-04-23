import streamlit as st

# 1. Initialize Memory
if 'task_list' not in st.session_state:
    st.session_state.task_list = []

# Colors
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

# 3. Sidebar (Photo and Stats)
with st.sidebar:
    st.header("⚙️ Settings")
    # THE RESTORED PHOTO
    st.image("https://cdn-icons-png.flaticon.com/512/4345/4345573.png", width=100)
    
    st.write("---")
    st.header("📊 Task Stats")
    st.metric("Tasks to do", len(st.session_state.task_list))
    
    if st.button("🗑️ Clear All Tasks"):
        st.session_state.task_list = []
        st.rerun()

# 4. Main App
st.header("📝 Sorted To-Do List")

# 5. Input Section
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name of task", placeholder="e.g. Study for finals")
    start_time = st.time_input("Start time")
    end_time = st.time_input("Finish time")

with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    motivation = st.select_slider("Motivation Level", options=["Sloth", "Human", "Robot"])

# 6. Logic to Add and SORT Task
if st.button("Add Task"):
    if name:
        new_task = {
            "name": name,
            "priority": priority,
            "start": start_time.strftime('%H:%M'),
            "end": end_time.strftime('%H:%M'),
            "motivation": motivation
        }
        st.session_state.task_list.append(new_task)
        
        # Sort by priority: High (1), Medium (2), Low (3)
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        st.session_state.task_list.sort(key=lambda x: priority_map[x["priority"]])
        
        st.success(f"Task '{name}' added!")
    else:
        st.error("Please enter a task name first!")

st.divider()

# 7. Display List
st.subheader("Priority Queue")

if not st.session_state.task_list:
    st.info("The list is empty. Time for a break?")
else:
    for task in st.session_state.task_list:
        # Dynamic border colors based on urgency
        if task['priority'] == "High":
            border_color = "#D9534F" # Red
        elif task['priority'] == "Medium":
            border_color = "#F0AD4E" # Orange
        else:
            border_color = title_color # Original Brown
            
        st.markdown(f"""
            <div class="task-card" style="border-left-color: {border_color};">
                <h4 style="margin:0;">{task['name']}</h4>
                <p style="margin:5px 0 0
