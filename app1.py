import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os
import hashlib
import shutil
import time
import threading




def hash_password(password: str) -> str:
    return hashlib.sha256((password).encode()).hexdigest()



# -----------------------------
# DATA FILE
# -----------------------------
DATA_FILE = "data.json"
BACKUP_FILE = "data_backup.json"




# -----------------------------
# INITIALIZE DATA
# -----------------------------
if not os.path.exists(DATA_FILE):
    # Try backup first
    if os.path.exists(BACKUP_FILE):
        shutil.copy2(BACKUP_FILE, DATA_FILE)
        print("Restored data.json from backup.")
    else:
        # original initialization if no backup
        data = {
            "members": [
                {"id": 1, "username": "Maya Allam"},
                {"id": 2, "username": "Ahmed Khodier"},
                {"id": 3, "username": "Amr Gado"},
                {"id": 4, "username": "Karim Anwar"},
            ],
            "tasks": [],
            "task_activity": []
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
else:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)


# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -----------------------------
# Backup DATA
# -----------------------------

def backup_data():
    try:
        # Copy the current data file to a backup
        shutil.copy2(DATA_FILE, BACKUP_FILE)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Backup created.")
    except Exception as e:
        print(f"Backup failed: {e}")

def periodic_backup(interval=300):
    def run():
        while True:
            time.sleep(interval)
            backup_data()
    threading.Thread(target=run, daemon=True).start()

periodic_backup(interval=300)  

# -----------------------------
# SAVE DATA
# -----------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    backup_data()



# -----------------------------
# LOGOUT FUNCTION
# -----------------------------
def logout():
    st.session_state.role = None
    st.session_state.user_id = None

def add_logout_topright():
    col1, col2 = st.columns([10, 1.85])
    with col2:
        if st.button("Logout 🔒"):
            logout()

def public_login():
    st.set_page_config(page_title="Task Manager", layout="centered")

    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # Container
    st.markdown("""
    <div style="
        max-width: 560px;
        margin: 0 auto;
        padding: 40px 35px;
        border-radius: 20px;
        box-shadow: 0 14px 35px rgba(11,61,145,0.15);
        background: white;
        text-align: center;
    ">
        <h1 style="color:#0b3d91;">Secure Access</h1>
        <p style="color:#6b7fa6;">Enter credentials to continue</p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if st.button("Login"):
        if not username or not password:
            st.error("Both fields are required")
            return

        if (
            username == PUBLIC_USERNAME
            and hash_password(password) == PUBLIC_PASSWORD_HASH
        ):
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials")

# -----------------------------
# ROLE SELECTION (REPLACES LOGIN)
# -----------------------------
def select_role():
    st.set_page_config(page_title="Task Manager", layout="centered")

    # -----------------------------
    # Custom CSS
    # -----------------------------
    st.markdown("""
<style>
.role-card {
    background-color: #ffffff;
    max-width: 560px;
    margin: 0 auto;
    padding: 40px 35px 35px 35px;
    border-radius: 20px;
    box-shadow: 0 14px 35px rgba(11,61,145,0.15);
    text-align: center;
}

.role-card h1 {
    color: #0b3d91;
    font-weight: 800;
    margin-bottom: 6px;
}

.role-card p {
    color: #6b7fa6;
    font-size: 15px;
    margin-bottom: 30px;
}

/* --- RADIO CLEAN STYLE --- */
.stRadio > div {
    justify-content: center;
    gap: 40px;
}

.stRadio label {
    background: transparent !important;
    padding: 0 !important;
    font-weight: 600;
    color: #0b3d91;
}

/* remove blue pill */
.stRadio input + div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* selected dot only */
.stRadio input:checked + div {
    color: #0b3d91 !important;
    font-weight: 700;
}

/* Selectbox spacing */
div[data-baseweb="select"] {
    margin-top: 10px;
}

/* Button */
div.stButton > button {
    background-color: #0b3d91;
    color: white;
    border-radius: 14px;
    padding: 14px 50px;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #062a6c;
}
</style>
""", unsafe_allow_html=True)


    # -----------------------------
    # Logo
    # -----------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      st.image("Unknown.png", use_container_width=True)
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    # -----------------------------
    # Role Card
    # -----------------------------
    st.markdown("""
<div class="role-card">
    <h1>Task Manager</h1>
    <p>Select your role to continue</p>
</div>
""", unsafe_allow_html=True)


    # Center radio inside card area
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1, 1.5, 1])
    with r2:
      role = st.radio("", ["Admin", "Member"], horizontal=True)

    member_id = None

    if role == "Member":
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        scol1, scol2, scol3 = st.columns([1, 1.5, 1])
        with scol2:
            member_name = st.selectbox(
                "Select your name",
                [m["username"] for m in data["members"]],
                key="member_name"
            )

        member_id = next(
            (m["id"] for m in data["members"] if m["username"] == member_name),
            None
        )

    # -----------------------------
    # Continue Button (Centered)
    # -----------------------------
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    bcol1, bcol2, bcol3 = st.columns([1, 0.87, 1])
    with bcol2:
        if st.button("Continue"):
            st.session_state.role = role
            st.session_state.user_id = member_id
            st.session_state.logged_in = True


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
def admin_dashboard():
    add_logout_topright()
    
    # -----------------------------
    # Logo - centered like main page
    # -----------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
     st.image("Unknown.png", use_container_width=True)
    
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    # -----------------------------
    # Dashboard Card
    # -----------------------------
    st.markdown("""
    <div style="
        max-width: 600px;
        margin: 0 auto;
        padding: 25px;
        background: #f8fbff;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(11,61,145,0.1);
        text-align: center;
    ">
        <h1 style="color:#0b3d91; font-weight:800; margin-bottom:6px;">Admin Dashboard</h1>
        <p style="color:#6b7fa6; font-size:15px; margin-bottom:25px;">Task Management & Oversight</p>
    </div>
    """, unsafe_allow_html=True)



    st.markdown("""
    <style>
    .stTabs [role="tablist"] button { border-radius: 25px; background-color: #0b3d91; color: white; font-weight: 600; margin-right: 5px; padding: 8px 18px; transition: 0.3s; }
    .stTabs [role="tablist"] button[aria-selected="true"] { background-color: #062a6c; }
    .dashboard-card { background-color: #0b3d91; padding: 25px 20px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.12); color: white; margin-bottom: 20px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div { border-radius: 10px !important; border: 1px solid #0b3d91 !important; padding: 10px !important; font-size: 15px !important; background-color: white !important; color: black !important; }
    div.stButton>button { background-color: #0b3d91; color: white; border-radius: 10px; padding: 8px 15px; width: 100%; font-size: 16px; transition: 0.3s; }
    div.stButton>button:hover { background-color: #062a6c; }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Create & Assign Task", "Member Task Board", "All Tasks"])

    # -----------------------------
    # Tab 1: Create & Assign Task
    # -----------------------------
    with tab1:
        st.subheader("Create & Assign Task")
        with st.form("create_task_form"):
            title = st.text_input("Task Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            task_type = st.selectbox("Task Type", ["Digital Initiative", "Performance Management System", "Departmental Manual", "Dashboards"])
            deadline = st.date_input("Deadline")

            assigned_members = st.multiselect("Assign to Members", [m["username"] for m in data["members"]])

            if st.form_submit_button("Create Task"):
                if not title or not assigned_members:
                    st.error("Task title and at least one member required")
                else:
                    task_id = len(data["tasks"]) + 1
                    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
                    task = {
                        "id": task_id,
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "status": "Pending",
                        "deadline": str(deadline),
                        "created_by": "Admin",
                        "created_at": created_at,
                        "task_type": task_type,
                        "assigned_members": assigned_members
                    }
                    data["tasks"].append(task)
                    save_data()
                    st.success("Task created and assigned!")

    # -----------------------------
    # Tab 2: Member Task Board
    # -----------------------------
    with tab2:
        st.subheader("Member Task Boards")
        if not data["members"]:
            st.info("No members found.")
        else:
            for m in data["members"]:
                member_tasks = [t for t in data["tasks"] if m["username"] in t["assigned_members"]]
                with st.expander(f"📊 {m['username']}'s Board", expanded=False):
                    if not member_tasks:
                        st.info("No tasks assigned")
                        continue

                    total_tasks = len(member_tasks)
                    completed_tasks = sum(1 for t in member_tasks if t["status"] == "Completed")
                    pending_tasks = sum(1 for t in member_tasks if t["status"] != "Completed")
                    deadline_met = sum(1 for t in member_tasks if t["status"] == "Completed" and datetime.strptime(t["created_at"], "%Y-%m-%d %H:%M") <= datetime.strptime(t["deadline"], "%Y-%m-%d"))

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Tasks", total_tasks)
                    col2.metric("Completed", completed_tasks)
                    col3.metric("Pending", pending_tasks)
                    col4.metric("Deadline Met", deadline_met)

                    status_counts = pd.DataFrame([(t["status"], 1) for t in member_tasks], columns=["Status", "Count"]).groupby("Status").sum().reset_index()
                    if not status_counts.empty:
                        fig = px.pie(status_counts, names="Status", values="Count", title=f"{m['username']}'s Task Status Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
                        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Tab 3: All Tasks
    # -----------------------------
    with tab3:
        st.subheader("All Tasks Overview")
        if not data["tasks"]:
            st.info("No tasks found.")
        else:
            df = pd.DataFrame(data["tasks"])
            df["Assigned Members"] = df["assigned_members"].apply(lambda x: ", ".join(x))

            col1, col2, col3 = st.columns(3)
            with col1:
                filter_type = st.selectbox("Filter by Task Type", ["All"] + df["task_type"].unique().tolist())
            with col2:
                filter_status = st.selectbox("Filter by Status", ["All"] + df["status"].unique().tolist())
            with col3:
                filter_member = st.selectbox("Filter by Assigned Member", ["All"] + sorted({m for members in df["assigned_members"] for m in members}))

            filtered_df = df.copy()
            if filter_type != "All": filtered_df = filtered_df[filtered_df["task_type"] == filter_type]
            if filter_status != "All": filtered_df = filtered_df[filtered_df["status"] == filter_status]
            if filter_member != "All": filtered_df = filtered_df[filtered_df["Assigned Members"].str.contains(filter_member)]

            search_term = st.text_input("Search Task Name")
            if search_term:
               filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False)]

            sort_col = st.selectbox("Sort by Column", filtered_df.columns.tolist(), index=0)
            sort_order = st.radio("Order", ["Ascending", "Descending"], index=1)
            filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order=="Ascending"))

            def color_status_row(row):
                if row["status"] == "Pending": return ["background-color: #ffcccc"]*len(row)
                elif row["status"] == "Completed": return ["background-color: #ccffcc"]*len(row)
                elif row["status"] in ["In Progress", "Review"]: return ["background-color: #fff3b3"]*len(row)
                else: return [""]*len(row)

            st.dataframe(filtered_df.style.apply(color_status_row, axis=1), use_container_width=True)
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(label="Download as CSV", data=csv, file_name="tasks_report.csv", mime="text/csv")

# -----------------------------
# MEMBER DASHBOARD
# -----------------------------
def member_dashboard():
    add_logout_topright()
    # -----------------------------
    # Logo - centered like main page
    # -----------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
     st.image("Unknown.png", use_container_width=True)
    
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    # -----------------------------
    # Dashboard Card
    # -----------------------------
    st.markdown("""
    <div style="
        max-width: 600px;
        margin: 0 auto;
        padding: 25px;
        background: #f8fbff;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(11,61,145,0.1);
        text-align: center;
    ">
        <h1 style="color:#0b3d91; font-weight:800; margin-bottom:6px;">Member Dashboard</h1>
        <p style="color:#6b7fa6; font-size:15px; margin-bottom:25px;">Check Your Tasks and Progress</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    st.markdown("""
<style>
.stTabs [role="tablist"] button { 
    border-radius: 50px; 
    background-color: #0b3d91; 
    color: white; 
    font-weight: 600; 
    margin-right: 5px; 
    padding: 10px 25px;  /* smaller padding */
    font-size: 14px;     /* slightly smaller text */
    transition: 0.3s; 
}
.stTabs [role="tablist"] button[aria-selected="true"] { 
    background-color: #062a6c; 
}
.dashboard-card { 
    background-color: #0b3d91; 
    padding: 20px 15px; 
    border-radius: 15px; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.12); 
    color: white; 
    margin-bottom: 20px; 
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div { 
    border-radius: 10px !important; 
    border: 1px solid #0b3d91 !important; 
    padding: 8px !important;  /* smaller padding */
    font-size: 14px !important; /* slightly smaller text */
    background-color: white !important; 
    color: black !important; 
}
div.stButton>button { 
    background-color: #0b3d91; 
    color: white; 
    border-radius: 10px; 
    padding: 8px 15px;   /* smaller vertical padding */
    width: 100%; 
    font-size: 14px;    /* smaller font */
    transition: 0.3s; 
}
div.stButton>button:hover { 
    background-color: #062a6c; 
}
</style>
""", unsafe_allow_html=True)


    member_id = st.session_state.user_id
    member_name = next((m["username"] for m in data["members"] if m["id"] == member_id),"Unknown Member")
    tasks = [t for t in data["tasks"] if member_name in t["assigned_members"]]

    if not tasks:
        st.info("No tasks assigned to you")
        return

    status_percent = {"Pending": 0, "In Progress": 25, "Review": 50, "Completed": 100}
    overall_progress = sum([status_percent[t["status"]] for t in tasks]) / len(tasks)
    st.progress(int(overall_progress))
    st.markdown(f"<p style='text-align:center; color:#0b3d91;'>Overall Progress: {overall_progress:.1f}%</p>", unsafe_allow_html=True)

    selected_status = st.radio("Task Status", ["Pending", "In Progress", "Review", "Completed"], index=0, horizontal=True)

    for t in tasks:
        if t["status"] != selected_status: continue
        with st.expander(f"{t['title']} (Status: {t['status']})", expanded=t["status"]=="Pending"):
            st.write(t["description"])
            new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Review", "Completed"], index=["Pending", "In Progress", "Review", "Completed"].index(t["status"]), key=f"status_{t['id']}")
            comment = st.text_area("Comment", key=f"comment_{t['id']}")

            if st.button("Save", key=f"btn_{t['id']}"):
                old_status = t["status"]
                t["status"] = new_status
                data["task_activity"].append({
                    "task_id": t["id"],
                    "user_id": member_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "comment": comment,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_data()
                st.success("Updated successfully!")

if not st.session_state.authenticated:
    public_login()
elif st.session_state.role is None:
    select_role()
else:
    if st.session_state.role == "Admin":
        admin_dashboard()
    else:
        member_dashboard()
