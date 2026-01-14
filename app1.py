import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from pymongo import MongoClient

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Task Manager", layout="centered", page_icon="✅")

# -------------------------------------------------
# MONGODB CONNECTION
# -------------------------------------------------
MONGO_URI = st.secrets[MONGO_URI] 

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tls=True)
    client.admin.command("ping")
except Exception as e:
    st.error("❌ Cannot connect to MongoDB Atlas")
    st.error(str(e))
    st.stop()

db = client["task_management"]
members_col = db["members"]
tasks_col = db["tasks"]

# -------------------------------------------------
# SECURITY
# -------------------------------------------------
PUBLIC_USERNAME = st.secrets["PUBLIC_USERNAME"]
PUBLIC_PASSWORD_HASH = st.secrets["PUBLIC_PASSWORD_HASH"]

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# -------------------------------------------------
# INITIAL DATA (RUN ONCE)
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
for key in ["authenticated", "role", "member_name"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "authenticated" else False

# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def add_logout():
    _, col = st.columns([10, 1.8])
    with col:
        if st.button("Logout 🔒"):
            logout()

# -------------------------------------------------
# PUBLIC LOGIN
# -------------------------------------------------
def public_login():
    with st.container():
        st.image("Unknown.png", use_column_width=True)
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="max-width:500px;margin:auto;padding:40px;
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
                st.rerun()
            else:
                st.error("Invalid credentials")

# -------------------------------------------------
# ROLE SELECTION
# -------------------------------------------------
def select_role():
    with st.container():
        st.image("Unknown.png", use_column_width=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        role = st.radio("Select role", ["Admin", "Member"], horizontal=True)

        member = None
        if role == "Member":
            names = [m["name"] for m in members_col.find({"role": "Member"})]
            member = st.selectbox("Select your name", names)

        if st.button("Continue"):
            st.session_state.role = role
            st.session_state.member_name = member
            st.rerun()

# -------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------
def admin_dashboard():
    add_logout()
    st.markdown("<h2 style='text-align:center;color:#0b3d91'>Admin Dashboard</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Create Task", "Member Tasks", "All Tasks"])

    # CREATE TASK
    with tab1:
        with st.form("task_form"):
            st.markdown("### Create New Task")
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
                st.success("✅ Task created successfully")

    # MEMBER TASKS
    with tab2:
        for m in members_col.find({"role":"Member"}):
            tasks = list(tasks_col.find({"assigned_members": m["name"]}))
            with st.expander(f"{m['name']} ({len(tasks)} tasks)"):
                for t in tasks:
                    st.markdown(f"**{t['title']}** - {t['status']}")

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
    st.markdown(f"<h2 style='text-align:center;color:#0b3d91'>Tasks for {st.session_state.member_name}</h2>", unsafe_allow_html=True)
    
    name = st.session_state.member_name
    tasks = list(tasks_col.find({"assigned_members": name}))

    if not tasks:
        st.info("No tasks assigned")
        return

    for t in tasks:
        with st.container():
            with st.expander(f"{t['title']}"):
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
                    st.success("✅ Status updated")

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
