import streamlit as st
import time
import random

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

# --- THE ORIGINAL COLORS ---
bg_color = "#c2c395"     
title_color = "#4C3D19"  
card_color = "#fdfae1"   

# 3. CSS Styling
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; }}
    [data-testid="stSidebar"] {{ background-color: #b5b68a; }} 
    h1, h2, h3, h4 {{ color: {title_color} !important; font-family: 'Helvetica', sans-serif; }}
    .stMarkdown p, label {{ color: {title_color} !important; }}
    .task-card {{
        background-color: {card_color};
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid {title_color};
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Sidebar (Image, REAL Timer with Stop, and Stats)
with st.sidebar:
    st.header("⚙️ Settings")
    st.image("https://cdn-icons-png.flaticon.com/512/4345/4345573.png", width=100)
    
    st.write("---")
    
    # POMODORO TIMER SECTION
    st.subheader("Pomodoro in action")
    timer_choice = st.radio("Focus Mode:", ["Study (25m)", "Break (5m)", "Quick Blast (10s)"])
    
    col_start, col_stop = st.columns(2)
    
    with col_start:
        start_clicked = st.button("▶️ Start")
    with col_stop:
        stop_clicked = st.button("⏹️ Stop") # Reruns the app to kill the loop

    if start_clicked:
        if "25m" in timer_choice:
            duration_seconds = 25 * 60
        elif "5m" in timer_choice:
            duration_seconds = 5 * 60
        else:
            duration_seconds = 10
        
        progress_bar = st.progress(0)
        countdown_text = st.empty()
        
        for remaining in range(duration_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            countdown_text.markdown(f"### ⏳ {m:02d}:{s:02d}")
            
            progress_pct = (duration_seconds - remaining) / duration_seconds
            progress_bar.progress(progress_pct)
            
            time.sleep(1) 
            
        st.balloons()
        st.success("Time's up!")

    st.write("---")
    st.metric("Tasks Left", len(st.session_state.task_list))
    st.metric("Tasks Done", st.session_state.done_count)
    
    if st.button("🗑️ Reset Everything"):
        st.session_state.task_list = []
        st.session_state.done_count = 0
        st.rerun()

# 5. Main Header & Roast Feature
st.header("📝 My School Task Manager")

roasts = [
    "Your to-do list looks like a 'maybe-someday' list. Get moving!",
    "Sloth mode detected. Initiating virtual coffee splash... ☕",
    "If you spent as much time working as you did changing colors, you'd be done!",
    "Is that a task list or a bedtime story? Wake up!",
    "Your ambition says 'Robot', but your pace says 'Sloth'."
]
if st.button("Roast My Productivity"):
    st.toast(random.choice(roasts), icon="🔥")

# 6. Input Section
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name of task", placeholder="e.g. Biology Quiz")
    start_time = st.time_input("Start time")
    end_time = st.time_input("Finish time")

with col2:
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    motivation = st.select_slider("Motivation Level", options=["Sloth", "Human", "Robot"])

# 7. Logic to Add, Sort, and Feedback
if st.button("Add Task"):
    if name:
        new_task = {
            "name": name,
            "priority": priority,
            "start": start_time,
            "end": end_time,
            "motivation": motivation
        }
        st.session_state.task_list.append(new_task)
        
        p_map = {"High": 1, "Medium": 2, "Low": 3}
        st.session_state.task_list.sort(key=lambda x: p_map[x["priority"]])
        
        if priority == "Low" and motivation == "Sloth":
            st.warning("Low priority and Sloth mode? This task is never happening, is it?")
        elif priority == "High":
            st.success("High priority! Let's get to work.")
        else:
            st.info("You've got this!")
    else:
        st.error("Please enter a task name!")

st.divider()

# 8. Task Display List
st.subheader("Your Priority List")
if not st.session_state.task_list:
    st.info("No tasks left! Time for a break?")
else:
    for i, task in enumerate(st.session_state.task_list):
        if task['priority'] == "High":
            b_col = "#D9534F" 
        elif task['priority'] == "Medium":
            b_col = "#F0AD4E" 
        else:
            b_col = title_color 
            
        st.markdown(
            f"""
            <div class="task-card" style="border-left-color: {b_col};">
                <h4 style="margin:0; color: {title_color};">{task['name']}</h4>
                <p style="margin:5px 0 0 0;">
                    ⏰ <b>{task['start'].strftime('%H:%M')} – {task['end'].strftime('%H:%M')}</b> | 
                    🚩 <b>{task['priority']}</b> | ⚡ <b>{task['motivation']}</b>
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button(f"Mark Done: {task['name']}", key=f"done_{i}"):
            st.session_state.task_list.pop(i)
            st.session_state.done_count += 1
            st.rerun()

st.divider()

# 9. FEATURE: Energy Level Graph (MOVED TO BOTTOM)
if st.session_state.task_list:
    st.subheader("📊 Your Effort Summary")
    m_map = {"Sloth": 1, "Human": 5, "Robot": 10}
    chart_data = {t['name']: m_map[t['motivation']] for t in st.session_state.task_list}
    st.bar_chart(chart_data, color="#4C3D19")
