import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Task Manager", layout="centered")

# -------------------------------------------------
# MONGODB CONNECTION
# -------------------------------------------------
MONGO_URI = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["task_manager"]

members_col = db["members"]
tasks_col = db["tasks"]
activity_col = db["task_activity"]

# -------------------------------------------------
# SECURITY (PUBLIC LOGIN)
# -------------------------------------------------
PUBLIC_USERNAME = "strategy.team2025"
PUBLIC_PASSWORD_HASH = "3137e6853c24fffa678e5ed165b10834dbfb3e8c97b79ad43d16d6cd9e9273ea"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# -------------------------------------------------
# INITIAL DATA (ONLY RUNS ONCE)
# -------------------------------------------------
if members_col.count_documents({}) == 0:
    members_col.insert_many([
        {"name": "Belal Merghany", "role": "Admin"},
        {"name": "Marwan Alahmar", "role": "Admin"},
        {"name": "Maya Allam", "role": "Member"},
        {"name": "Karim Anwar", "role": "Member"},
        {"name": "Ahmed Khodier", "role": "Member"},
        {"name": "Amr Gado", "role": "Member"},
    ])

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "member_name" not in st.session_state:
    st.session_state.member_name = None

# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.experimental_rerun()

def add_logout():
    _, col = st.columns([10, 1.8])
    with col:
        if st.button("Logout 🔒"):
            logout()

# -------------------------------------------------
# PUBLIC LOGIN
# -------------------------------------------------
def public_login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="max-width:560px;margin:auto;padding:40px;
    border-radius:20px;box-shadow:0 14px 35px rgba(11,61,145,.15);
    background:white;text-align:center">
    <h1 style="color:#0b3d91">Secure Access</h1>
    </div>
    """, unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if not user or not pwd:
            st.error("Both fields required")
        elif user == PUBLIC_USERNAME and hash_password(pwd) == PUBLIC_PASSWORD_HASH:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# -------------------------------------------------
# ROLE SELECTION
# -------------------------------------------------
def select_role():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    role = st.radio("Select role", ["Admin", "Member"], horizontal=True)

    if role == "Member":
        names = [m["name"] for m in members_col.find({"role": "Member"})]
        member = st.selectbox("Select your name", names)
    else:
        member = None

    if st.button("Continue"):
        st.session_state.role = role
        st.session_state.member_name = member
        st.experimental_rerun()

# -------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------
def admin_dashboard():
    add_logout()

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    tab1, tab2, tab3 = st.tabs(["Create & Assign Task", "Member Task Board", "All Tasks"])

    # CREATE TASK
    with tab1:
        with st.form("task_form"):
            title = st.text_input("Task Title")
            desc = st.text_area("Description")
            priority = st.selectbox("Priority", ["Low","Medium","High"])
            task_type = st.selectbox("Task Type", ["Digital Initiative","PMS","Manual","Dashboard"])
            deadline = st.date_input("Deadline")
            members = [m["name"] for m in members_col.find({"role":"Member"})]
            assigned = st.multiselect("Assign to Members", members)

            if st.form_submit_button("Create Task"):
                tasks_col.insert_one({
                    "title": title,
                    "description": desc,
                    "priority": priority,
                    "task_type": task_type,
                    "deadline": str(deadline),
                    "status": "Pending",
                    "assigned_members": assigned,
                    "created_at": datetime.now()
                })
                st.success("Task created")

    # MEMBER BOARDS
    with tab2:
        for m in members_col.find({"role":"Member"}):
            tasks = list(tasks_col.find({"assigned_members": m["name"]}))
            with st.expander(m["name"]):
                st.write(f"Tasks: {len(tasks)}")

    # ALL TASKS
    with tab3:
        df = pd.DataFrame(list(tasks_col.find()))
        if not df.empty:
            df["assigned_members"] = df["assigned_members"].apply(", ".join)
            st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# MEMBER DASHBOARD
# -------------------------------------------------
def member_dashboard():
    add_logout()

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    name = st.session_state.member_name
    tasks = list(tasks_col.find({"assigned_members": name}))

    if not tasks:
        st.info("No tasks assigned")
        return

    for t in tasks:
        with st.expander(t["title"]):
            new_status = st.selectbox(
                "Status",
                ["Pending","In Progress","Review","Completed"],
                index=["Pending","In Progress","Review","Completed"].index(t["status"]),
                key=str(t["_id"])
            )
            if st.button("Save", key="btn"+str(t["_id"])):
                tasks_col.update_one(
                    {"_id": t["_id"]},
                    {"$set":{"status": new_status}}
                )
                st.success("Updated")

# -------------------------------------------------
# ROUTING
# -------------------------------------------------
if not st.session_state.authenticated:
    public_login()
elif st.session_state.role is None:
    select_role()
elif st.session_state.role == "Admin":
    admin_dashboard()
else:
    member_dashboard()
