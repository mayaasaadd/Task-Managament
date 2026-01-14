import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# -----------------------------
# MONGODB CONNECTION
# -----------------------------
MONGO_URI = "mongodb+srv://AlahlyiaTaskManagment:<alahlyiastrategy@2025>@cluster0.oo0pkwy.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["task_manager"]

admins_col = db["admins"]
members_col = db["members"]
tasks_col = db["tasks"]
task_activity_col = db["task_activity"]

# -----------------------------
# PASSWORD HASH
# -----------------------------
PUBLIC_USERNAME = st.secrets["passwords"]["public_username"]
PUBLIC_PASSWORD = st.secrets["passwords"]["public_password"]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

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
# LOGOUT FUNCTION
# -----------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.user_id = None

def add_logout_topright():
    col1, col2 = st.columns([10, 1.85])
    with col2:
        if st.button("Logout 🔒"):
            logout()

# -----------------------------
# PUBLIC LOGIN
# -----------------------------
def public_login():
    st.set_page_config(page_title="Task Manager", layout="centered")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

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

    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if st.button("Login"):
        if not username or not password:
            st.error("Both fields are required")
            return

        if username == PUBLIC_USERNAME and hash_password(password) == PUBLIC_PASSWORD_HASH:
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials")

# -----------------------------
# ROLE SELECTION
# -----------------------------
def select_role():
    st.set_page_config(page_title="Task Manager", layout="centered")

    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    # Role card
    st.markdown("""
<div style="
    background-color: #ffffff;
    max-width: 560px;
    margin: 0 auto;
    padding: 40px 35px 35px 35px;
    border-radius: 20px;
    box-shadow: 0 14px 35px rgba(11,61,145,0.15);
    text-align: center;">
    <h1 style="color:#0b3d91;">Task Manager</h1>
    <p style="color:#6b7fa6; font-size:15px;">Select your role to continue</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1, 1.5, 1])
    with r2:
        role = st.radio("", ["Admin", "Member"], horizontal=True)

    member_id = None
    if role == "Member":
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        scol1, scol2, scol3 = st.columns([1, 1.5, 1])
        with scol2:
            member_docs = list(members_col.find())
            member_name = st.selectbox(
                "Select your name",
                [m["username"] for m in member_docs],
                key="member_name"
            )
            member_id = str(next((m["_id"] for m in member_docs if m["username"] == member_name), None))

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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        max-width: 600px;
        margin: 0 auto;
        padding: 25px;
        background: #f8fbff;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(11,61,145,0.1);
        text-align: center;">
        <h1 style="color:#0b3d91; font-weight:800; margin-bottom:6px;">Admin Dashboard</h1>
        <p style="color:#6b7fa6; font-size:15px; margin-bottom:25px;">Task Management & Oversight</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Create & Assign Task", "Member Task Board", "All Tasks"])

    # Tab 1: Create Task
    with tab1:
        st.subheader("Create & Assign Task")
        with st.form("create_task_form"):
            title = st.text_input("Task Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            task_type = st.selectbox("Task Type", ["Digital Initiative", "Performance Management System", "Departmental Manual", "Dashboards"])
            deadline = st.date_input("Deadline")
            
            member_docs = list(members_col.find())
            assigned_members = st.multiselect("Assign to Members", [m["username"] for m in member_docs])

            if st.form_submit_button("Create Task"):
                if not title or not assigned_members:
                    st.error("Task title and at least one member required")
                else:
                    task = {
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "status": "Pending",
                        "deadline": str(deadline),
                        "created_by": "Admin",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "task_type": task_type,
                        "assigned_members": assigned_members
                    }
                    tasks_col.insert_one(task)
                    st.success("Task created and assigned!")

    # Tab 2: Member Task Board
    with tab2:
        st.subheader("Member Task Boards")
        members = list(members_col.find())
        if not members:
            st.info("No members found.")
        else:
            for m in members:
                member_tasks = list(tasks_col.find({"assigned_members": m["username"]}))
                with st.expander(f"📊 {m['username']}'s Board", expanded=False):
                    if not member_tasks:
                        st.info("No tasks assigned")
                        continue

                    total_tasks = len(member_tasks)
                    completed_tasks = sum(1 for t in member_tasks if t["status"] == "Completed")
                    pending_tasks = total_tasks - completed_tasks
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Tasks", total_tasks)
                    col2.metric("Completed", completed_tasks)
                    col3.metric("Pending", pending_tasks)
                    col4.metric("Deadline Met", "-")  # Can calculate if needed

                    status_counts = pd.DataFrame([(t["status"], 1) for t in member_tasks], columns=["Status", "Count"]).groupby("Status").sum().reset_index()
                    if not status_counts.empty:
                        fig = px.pie(status_counts, names="Status", values="Count", title=f"{m['username']}'s Task Status Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
                        st.plotly_chart(fig, use_container_width=True)

    # Tab 3: All Tasks
    with tab3:
        st.subheader("All Tasks Overview")
        tasks = list(tasks_col.find())
        if not tasks:
            st.info("No tasks found.")
        else:
            df = pd.DataFrame(tasks)
            df["Assigned Members"] = df["assigned_members"].apply(lambda x: ", ".join(x))
            st.dataframe(df, use_container_width=True)

# -----------------------------
# MEMBER DASHBOARD
# -----------------------------
def member_dashboard():
    add_logout_topright()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True)

    member_id = st.session_state.user_id
    member_doc = members_col.find_one({"_id": ObjectId(member_id)})
    member_name = member_doc["username"] if member_doc else "Unknown Member"
    
    tasks = list(tasks_col.find({"assigned_members": member_name}))
    
    if not tasks:
        st.info("No tasks assigned to you")
        return

    for t in tasks:
        with st.expander(f"{t['title']} (Status: {t['status']})", expanded=True):
            st.write(t["description"])
            new_status = st.selectbox(
                "Update Status",
                ["Pending", "In Progress", "Review", "Completed"],
                index=["Pending", "In Progress", "Review", "Completed"].index(t["status"]),
                key=f"status_{t['_id']}"
            )
            comment = st.text_area("Comment", key=f"comment_{t['_id']}")
            if st.button("Save", key=f"btn_{t['_id']}"):
                old_status = t["status"]
                tasks_col.update_one({"_id": t["_id"]}, {"$set": {"status": new_status}})
                task_activity_col.insert_one({
                    "task_id": t["_id"],
                    "user_id": member_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "comment": comment,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Updated successfully!")

# -----------------------------
# MAIN
# -----------------------------
if not st.session_state.authenticated:
    public_login()
elif st.session_state.role is None:
    select_role()
else:
    if st.session_state.role == "Admin":
        admin_dashboard()
    else:
        member_dashboard()
