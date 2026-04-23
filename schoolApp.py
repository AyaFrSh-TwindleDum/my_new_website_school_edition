import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(
    page_title="School Task Manager", 
    page_icon="📝", 
    layout="centered"
)

# 2. Initialize Memory
if 'task_list' not in st.session_state:
    st.session_state.task_list = []
if 'done_count' not in st.session_state:
    st.session_state.done_count = 0

# Updated Color Palette
sidebar_bg = "#B0E0E6"   # Powder Blue
main_bg = "#C19A6B"      # Camel
title_rocky = "#708090"  # Rocky (Slate Gray)
card_color = "#FDF5E6"   # Old Lace (Warm off-white)

# 3. CSS Styling
st.markdown(
    f"""
    <style>
    /* Main Background (Camel) */
    .stApp {{
        background-color: {main_bg};
    }}
    
    /* Sidebar Background (Powder Blue) */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}

    /* Title and Header Colors (Rocky) */
    h1, h2, h3, h4 {{
        color: {title_rocky} !important;
        font-family: 'Georgia', serif;
        font-weight: bold;
    }}

    /* Label and regular text colors for readability on Camel */
    .stMarkdown p, label, .stHeader {{
        color: #3E2723 !important; /* Dark Chocolate Brown */
    }}

    .task-card {{
        background-color: {card_color};
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid {title_rocky};
        margin-bottom: 5px;
        color: #333;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.image("https://cdn-icons-png.flaticon.com/512/4345/4345573.png", width=100)
    
    st.write("---")
    st.header("📊 Task Stats")
    st.metric("Tasks Left", len(st.session_state.task_list))
    st.metric("Tasks Done", st.session_state.done_count)
    
    if st.button("🗑️ Clear Everything"):
        st.session_state.task_list = []
        st.session_state.done_count = 0
        st.rerun()

# 5. Main App Header
st.header("📝 My School Task Manager")
st.write("A solid, rocky foundation for your productivity.")

# 6. Input Section
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name of task", placeholder="e.g. History Essay")
    start_time = st.time_input("Start time")
    end_time = st.time_input("Finish time")

with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    motivation = st.select_slider("Motivation Level", options=["Sloth", "Human", "Robot"])

# 7. Logic to Add, SORT, and FEEDBACK
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
        
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        st.session_state.task_list.sort(key=lambda x: priority_map[x["priority"]])
        
        if priority == "Low" and motivation == "Sloth":
            st.warning("Low priority and Sloth mode? This task is never happening, is it?")
        elif priority == "High":
            st.success("High priority! Let's get to work.")
        else:
            st.info("You've got this!")
    else:
        st.error("Please enter a task name first!")

st.divider()

# 8. Display List
st.subheader("Your Priority List")

if not st.session_state.task_list:
    st.info("Your list is currently empty.")
else:
    for i, task in enumerate(st.session_state.task_list):
        # Card border colors
        if task['priority'] == "High":
            b_color = "#D9534F" # Bold Red
        elif task['priority'] == "Medium":
            b_color = "#F0AD4E" # Warning Orange
        else:
            b_color = title_rocky # Rocky Gray
            
        st.markdown(
            f"""
            <div class="task-card" style="border-left-color: {b_color};">
                <h4 style="margin:0; color: {title_rocky};">{task['name']}</h4>
                <p style="margin:5px 0 0 0;">
                    ⏰ <b>Time:</b> {task['start']} – {task['end']} | 
                    🚩 <b>Priority:</b> {task['priority']} | 
                    ⚡ <b>Mode:</b> {task['motivation']}
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button(f"Mark Done: {task['name']}", key=f"done_{i}"):
            st.session_state.task_list.pop(i)
            st.session_state.done_count += 1
            st.rerun()
