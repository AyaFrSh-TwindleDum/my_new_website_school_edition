import streamlit as st

# 1. PAGE CONFIG - Sets the browser tab name and icon
st.set_page_config(
    page_title="School Task Manager", 
    page_icon="📝", 
    layout="centered"
)

# 2. Initialize Memory (Session State)
if 'task_list' not in st.session_state:
    st.session_state.task_list = []
if 'done_count' not in st.session_state:
    st.session_state.done_count = 0

# Colors
bg_color = "#c2c395"
title_color = "#4C3D19"
card_color = "#fdfae1"

# 3. CSS Styling
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
        margin-bottom: 5px;
        color: #333;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Sidebar (Photo and Stats)
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
st.write("My superb website will now evaluate your laziness.")

# 6. Input Section
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name of task", placeholder="e.g. Math Homework")
    start_time = st.time_input("Start time")
    end_time = st.time_input("Finish time")

with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    motivation = st.select_slider("Motivation Level", options=["Sloth", "Human", "Robot"])

# 7. Logic to Add, SORT, and FEEDBACK
if st.button("Add Task"):
    if name:
        # Create Task Object
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
        
        # --- YOUR LOGIC-BASED FEEDBACK ---
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
    st.info("No tasks left! Time for a break?")
else:
    for i, task in enumerate(st.session_state.task_list):
        # Pick border color based on urgency
        if task['priority'] == "High":
            b_color = "#D9534F"
        elif task['priority'] == "Medium":
            b_color = "#F0AD4E"
        else:
            b_color = title_color
            
        # Draw the card
        st.markdown(
            f"""
            <div class="task-card" style="border-left-color: {b_color};">
                <h4 style="margin:0;">{task['name']}</h4>
                <p style="margin:5px 0 0 0;">
                    ⏰ <b>Time:</b> {task['start']} – {task['end']} | 
                    🚩 <b>Priority:</b> {task['priority']} | 
                    ⚡ <b>Mode:</b> {task['motivation']}
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Finish button
        if st.button(f"Mark Done: {task['name']}", key=f"done_{i}"):
            st.session_state.task_list.pop(i)
            st.session_state.done_count += 1
            st.rerun()
