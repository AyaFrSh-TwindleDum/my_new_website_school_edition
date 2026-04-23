import streamlit as st
import time
import random

# 1. PAGE CONFIG - Sets the browser tab name
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

# --- THE ORIGINAL COLORS ---
bg_color = "#c2c395"     # Original Mossy Green
title_color = "#4C3D19"  # Original Dark Brown
card_color = "#fdfae1"   # Original Cream Card

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

# 4. Sidebar (Image, REAL Timer, and Stats)
with st.sidebar:
    st.header("⚙️ Settings")
    st.image("https://cdn-icons-png.flaticon.com/512/4345/4345573.png", width=100)
    
    st.write("---")
    
    # CORRECTED REAL POMODORO TIMER
    st.subheader("Pomodoro in action")
    timer_choice = st.radio("Focus Mode:", ["Study (25m)", "Break (5m)"])
    
    if st.button("Start Timer"):
        # Calculate real seconds
        mins = 25 if "Study" in timer_choice else 5
        duration_seconds = mins * 60 
        
        progress_bar = st.progress(0)
        countdown_text = st.empty()
        
        # The loop that runs for the full duration
        for remaining in range(duration_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            countdown_text.markdown(f"### ⏳ {m:02d}:{s:02d}")
            
            # Update progress bar
            progress_pct = (duration_seconds - remaining) / duration_seconds
            progress_bar.progress(progress_pct)
            
            time.sleep(1) # This waits 1 actual second
            
        st.balloons()
        st.success("Time's up! Great session.")

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
    "A journey of a thousand miles begins with closing this tab and starting your essay.",
    "Is that a task list or a bedtime story? Wake up!"
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
        
        # Sort by Priority (High to Low)
        p_map = {"High": 1, "Medium": 2, "Low": 3}
        st.session_state.task_list.sort(key=lambda x: p_map[x["priority"]])
        
        # Feedback Logic
        if priority == "Low" and motivation == "Sloth":
            st.warning("Low priority and Sloth mode? This task is never happening, is it?")
        elif priority == "High":
            st.success("High priority! Let's get to work.")
        else:
            st.info("You've got this!")
    else:
        st.error("Please enter a task name!")

st.divider()

# 8. FEATURE: Energy Level Graph
if st.session_state.task_list:
    st.subheader("📊 Your Energy Schedule")
    m_map = {"Sloth": 1, "Human": 5, "Robot": 10}
    # Create the chart based on motivation scores
    chart_data = {t['name']: m_map[t['motivation']] for t in st.session_state.task_list}
    st.bar_chart(chart_data, color="#4C3D19")

# 9. Task Display List
st.subheader("Priority Queue")
if not st.session_state.task_list:
    st.info("No tasks left! Time for a nap?")
else:
    for i, task in enumerate(st.session_state.task_list):
        # Card border color logic
        if task['priority'] == "High":
            b_col = "#D9534F" # Red
        elif task['priority'] == "Medium":
            b_col = "#F0AD4E" # Orange
        else:
            b_col = title_color # Brown
            
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
        
        # The unique key=f"done_{i}" is very important here!
        if st.button(f"Mark Done: {task['name']}", key=f"done_{i}"):
            st.session_state.task_list.pop(i)
            st.session_state.done_count += 1
            st.rerun()
