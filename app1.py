# import streamlit as st
# import sqlite3
# import pandas as pd
# import plotly.express as px
# from datetime import datetime  # ✅ fixed import

# # -----------------------------
# # DATABASE CONNECTION
# # -----------------------------
# conn = sqlite3.connect("task_app.db", check_same_thread=False)
# c = conn.cursor()

# # -----------------------------
# # SESSION STATE INIT
# # -----------------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_id = None
#     st.session_state.role = None
#     st.session_state.first_login = None

# # -----------------------------
# # LOGOUT FUNCTION
# # -----------------------------
# def logout():
#     st.session_state.logged_in = False
#     st.session_state.user_id = None
#     st.session_state.role = None
#     st.session_state.first_login = None

# def add_logout_topright():
#     col1, col2 = st.columns([10, 1.85])
#     with col2:
#         if st.button("Logout 🔒"):
#             logout()

# # -----------------------------
# # LOGIN SCREEN
# # -----------------------------
# def show_login():
#     st.set_page_config(page_title="Task Manager Login", layout="centered")

#     st.markdown("""
#     <style>
#     .logo-container { text-align: center; margin-top: 30px; margin-bottom: 20px; }
#     .logo-container img { width: 150px; }
#     .login-card { background-color: #0b3d91; padding: 40px 30px; max-width: 420px; margin: 0 auto 20px auto; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); text-align: center; color: white; }
#     .login-card h1 { font-size: 32px; margin-bottom: 10px; }
#     .login-card p { color: #E63946; font-size: 18px; margin-bottom: 25px; }
#     .stTextInput>div>div>input { border-radius: 10px !important; border: 1px solid #0b3d91 !important; padding: 12px !important; font-size: 16px !important; }
#     div.stButton>button { width: 500%; padding: 12px; margin-top: 0px; background-color: #0b3d91; color: white; border-radius: 10px; font-size: 18px; border: none; cursor: pointer; transition: 0.3s; }
#     div.stButton>button:hover { background-color: #062a6c; }
#     </style>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     st.markdown("""
#     <div class="login-card">
#         <h1>Task Manager</h1>
#         <p>Securely access your tasks</p>
#     </div>
#     """, unsafe_allow_html=True)

#     username = st.text_input("Username", key="username")
#     password = st.text_input("Password", type="password", key="password")
#     st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

#     login_col1, login_col2, login_col3 = st.columns([1,2,1])
#     with login_col2:
#         login_disabled = not (username and password)
#         if st.button("Login", disabled=login_disabled):
#             c.execute("""
#                 SELECT id, role, first_login
#                 FROM users
#                 WHERE username=? AND password=?
#             """, (username, password))
#             user = c.fetchone()

#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user_id = user[0]
#                 st.session_state.role = user[1]
#                 st.session_state.first_login = user[2]
#             else:
#                 st.error("Invalid username or password")

# # -----------------------------
# # PASSWORD CHANGE SCREEN
# # -----------------------------
# def show_password_change():
#     st.title("Change Your Password")
#     new_password = st.text_input("New Password", type="password")
#     confirm = st.text_input("Confirm Password", type="password")

#     if st.button("Update Password"):
#         if not new_password:
#             st.error("Password cannot be empty")
#         elif new_password != confirm:
#             st.error("Passwords do not match")
#         else:
#             c.execute("""
#                 UPDATE users
#                 SET password=?, first_login=0
#                 WHERE id=?
#             """, (new_password, st.session_state.user_id))
#             conn.commit()
#             st.session_state.first_login = 0
#             st.success("Password updated successfully")

# # -----------------------------
# # ADMIN DASHBOARD
# # -----------------------------
# def admin_dashboard():
#     add_logout_topright()

#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .stTabs [role="tablist"] button { border-radius: 25px; background-color: #0b3d91; color: white; font-weight: 600; margin-right: 5px; padding: 8px 18px; transition: 0.3s; }
#     .stTabs [role="tablist"] button[aria-selected="true"] { background-color: #062a6c; }
#     .dashboard-card { background-color: #0b3d91; padding: 25px 20px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.12); color: white; margin-bottom: 20px; }
#     .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div { border-radius: 10px !important; border: 1px solid #0b3d91 !important; padding: 10px !important; font-size: 15px !important; background-color: white !important; color: black !important; }
#     div.stButton>button { background-color: #0b3d91; color: white; border-radius: 10px; padding: 12px 0px; width: 100%; font-size: 16px; transition: 0.3s; }
#     div.stButton>button:hover { background-color: #062a6c; }
#     </style>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div style="max-width:600px; margin: 0 auto 25px auto; padding:20px; background:#f8fbff; border-radius:14px; box-shadow:0 4px 12px rgba(11,61,145,0.08); text-align:center;">
#         <h1 style="margin:0; color:#0b3d91; font-weight:700; letter-spacing:1px;">Admin Dashboard</h1>
#         <p style="margin-top:8px; color:#6b7fa6; font-size:15px;">Task Management & Oversight</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; margin-bottom: 25px; }
#     .stTabs [data-baseweb="tab"] { background-color: #e9f0ff; color: #0b3d91; padding: 8px 18px; border-radius: 25px; font-weight: 600; font-size: 14px; border: 1px solid #cddcff; }
#     .stTabs [data-baseweb="tab"]:hover { background-color: #d6e4ff; }
#     .stTabs [aria-selected="true"] { background-color: #0b3d91 !important; color: white !important; border: none; box-shadow: 0 4px 10px rgba(11,61,145,0.25); }
#     </style>
#     """, unsafe_allow_html=True)

#     tab1, tab2, tab3 = st.tabs(["Create & Assign Task", "Member Task Board", "All Tasks"])

#     # -----------------------------
#     # Tab 1: Create & Assign Task
#     # -----------------------------
#     with tab1:
#         st.subheader("Create & Assign Task")
#         with st.form("create_task_form"):
#             title = st.text_input("Task Title")
#             description = st.text_area("Description")
#             priority = st.selectbox("Priority", ["Low", "Medium", "High"])
#             task_type = st.selectbox("Task Type", ["Digital Initiative", "Performance Management System", "Departmental Manual", "Dashboards"])
#             deadline = st.date_input("Deadline")

#             c.execute("SELECT id, username FROM users WHERE role='MEMBER'")
#             members = c.fetchall()
#             member_map = {m[1]: m[0] for m in members}

#             assigned_members = st.multiselect("Assign to Members", list(member_map.keys()))

#             if st.form_submit_button("Create Task"):
#                 if not title or not assigned_members:
#                     st.error("Task title and at least one member are required")
#                 else:
#                     created_at = datetime.now().strftime("%Y-%m-%d %H:%M")  # ✅ fixed
#                     c.execute("""
#                         INSERT INTO tasks (title, description, priority, status, deadline, created_by, created_at, task_type)
#                         VALUES (?, ?, ?, 'Pending', ?, ?, ?, ?)
#                     """, (title, description, priority, str(deadline), st.session_state.user_id, created_at, task_type))
#                     task_id = c.lastrowid
#                     for username in assigned_members:
#                         c.execute("INSERT INTO task_assignments (task_id, user_id) VALUES (?, ?)", (task_id, member_map[username]))
#                     conn.commit()
#                     st.success("Task created and assigned!")
#         st.markdown("</div>", unsafe_allow_html=True)

#     # -----------------------------
#     # Tab 2: Member Task Board
#     # -----------------------------
#     with tab2:
#         st.subheader("Member Board Dashboard")
#         c.execute("SELECT id, username FROM users WHERE role='MEMBER'")
#         members = c.fetchall()

#         if not members:
#             st.info("No members found.")
#         else:
#             for m in members:
#                 with st.expander(f"📊 {m[1]}'s Board", expanded=False):
#                     c.execute("""
#                         SELECT t.id, t.title, t.status, t.deadline, t.created_at, t.task_type
#                         FROM tasks t
#                         JOIN task_assignments ta ON t.id = ta.task_id
#                         WHERE ta.user_id = ?
#                         ORDER BY t.id DESC
#                     """, (m[0],))
#                     tasks = c.fetchall()
#                     if not tasks:
#                         st.info("No tasks assigned")
#                         continue

#                     total_tasks = len(tasks)
#                     completed_tasks = sum(1 for t in tasks if t[2] == "Completed")
#                     pending_tasks = sum(1 for t in tasks if t[2] != "Completed")
#                     deadline_met = sum(1 for t in tasks if t[2] == "Completed" and pd.to_datetime(t[4]) <= pd.to_datetime(t[3]))

#                     c.execute("""
#                       SELECT task_id, timestamp
#                       FROM task_activity
#                       WHERE task_id IN (
#                         SELECT t.id FROM tasks t
#                         JOIN task_assignments ta ON t.id = ta.task_id
#                         WHERE ta.user_id = ?
#                       )
#                       ORDER BY task_id, timestamp
#                     """, (m[0],))
#                     activities = c.fetchall()

#                     task_times = {}
#                     for task_id, ts in activities:
#                         ts_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
#                         if task_id not in task_times:
#                             task_times[task_id] = [ts_dt, ts_dt]
#                         else:
#                             if ts_dt < task_times[task_id][0]:
#                                 task_times[task_id][0] = ts_dt
#                             if ts_dt > task_times[task_id][1]:
#                                 task_times[task_id][1] = ts_dt

#                     total_hours = sum((end - start).total_seconds() / 3600 for start, end in task_times.values())
#                     hours_worked = round(total_hours, 1)

#                     col1, col2, col3, col4, col5 = st.columns(5)
#                     col1.metric("Total Tasks", total_tasks)
#                     col2.metric("Completed", completed_tasks)
#                     col3.metric("Pending", pending_tasks)
#                     col4.metric("Deadline Met", deadline_met)
#                     col5.metric("Hours Worked", hours_worked)

#                     status_counts = pd.DataFrame([(t[2], 1) for t in tasks], columns=["Status", "Count"]).groupby("Status").sum().reset_index()
#                     if not status_counts.empty:
#                         fig = px.pie(status_counts, names="Status", values="Count", title=f"{m[1]}'s Task Status Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
#                         st.plotly_chart(fig, use_container_width=True)

#     # -----------------------------
#     # Tab 3: All Tasks
#     # -----------------------------
#     with tab3:
#         st.subheader("All Tasks Overview")
#         def color_status_row(row):
#             if row["Status"] == "Pending": return ["background-color: #ffcccc"]*len(row)
#             elif row["Status"] == "Completed": return ["background-color: #ccffcc"]*len(row)
#             elif row["Status"] in ["In Progress", "Review"]: return ["background-color: #fff3b3"]*len(row)
#             else: return [""]*len(row)

#         c.execute("SELECT t.id, t.title, t.status, t.task_type, t.priority, t.deadline, t.created_at FROM tasks t ORDER BY t.id DESC")
#         all_tasks = c.fetchall()

#         if not all_tasks:
#             st.info("No tasks found.")
#         else:
#             table_data = []
#             for t in all_tasks:
#                 task_id, task_title, task_status, task_type, task_priority, task_deadline, task_created = t
#                 c.execute("SELECT u.username FROM users u JOIN task_assignments ta ON u.id = ta.user_id WHERE ta.task_id = ?", (task_id,))
#                 members = [m[0] for m in c.fetchall()]
#                 members_str = ", ".join(members)
#                 table_data.append({
#                     "Task ID": task_id,
#                     "Task Name": task_title,
#                     "Task Type": task_type,
#                     "Priority": task_priority,
#                     "Status": task_status,
#                     "Deadline": task_deadline,
#                     "Created At": task_created,
#                     "Assigned Members": members_str
#                 })

#             df = pd.DataFrame(table_data)

#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 filter_type = st.selectbox("Filter by Task Type", ["All"] + df["Task Type"].unique().tolist())
#             with col2:
#                 filter_status = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
#             with col3:
#                 filter_member = st.selectbox("Filter by Assigned Member", ["All"] + sorted({m for members in df["Assigned Members"] for m in members.split(", ")}))

#             filtered_df = df.copy()
#             if filter_type != "All": filtered_df = filtered_df[filtered_df["Task Type"] == filter_type]
#             if filter_status != "All": filtered_df = filtered_df[filtered_df["Status"] == filter_status]
#             if filter_member != "All": filtered_df = filtered_df[filtered_df["Assigned Members"].str.contains(filter_member)]

#             search_term = st.text_input("Search Task Name")
#             if search_term: filtered_df = filtered_df[filtered_df["Task Name"].str.contains(search_term, case=False)]

#             sort_col = st.selectbox("Sort by Column", filtered_df.columns.tolist(), index=0)
#             sort_order = st.radio("Order", ["Ascending", "Descending"], index=1)
#             filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order=="Ascending"))

#             st.dataframe(filtered_df.style.apply(color_status_row, axis=1), use_container_width=True)
#             csv = filtered_df.to_csv(index=False).encode("utf-8")
#             st.download_button(label="Download as CSV", data=csv, file_name="tasks_report.csv", mime="text/csv")

# # -----------------------------
# # MEMBER DASHBOARD
# # -----------------------------
# def member_dashboard():
#     add_logout_topright()

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     c.execute("SELECT t.id, t.title, t.description, t.status FROM tasks t JOIN task_assignments ta ON t.id = ta.task_id WHERE ta.user_id = ? ORDER BY t.id DESC", (st.session_state.user_id,))
#     tasks = c.fetchall()
#     if not tasks: st.info("No tasks assigned to you"); return

#     status_percent = {"Pending": 0, "In Progress": 25, "Review": 50, "Completed": 100}
#     overall_progress = sum([status_percent[t[3]] for t in tasks]) / len(tasks)
#     st.progress(int(overall_progress))
#     st.markdown(f"<p style='text-align:center; color:#0b3d91;'>Overall Progress: {overall_progress:.1f}%</p>", unsafe_allow_html=True)

#     statuses = ["Pending", "In Progress", "Review", "Completed"]
#     selected_status = st.radio("Task Status", statuses, index=0, horizontal=True)

#     for t in tasks:
#         task_id, task_title, task_desc, task_status = t
#         if task_status != selected_status: continue
#         expanded_by_default = task_status == "Pending"

#         with st.expander(f"{task_title} (Status: {task_status})", expanded=expanded_by_default):
#             st.write(task_desc)

#             new_status = st.selectbox(
#                 "Update Status",
#                 ["Pending", "In Progress", "Review", "Completed"],
#                 index=["Pending", "In Progress", "Review", "Completed"].index(task_status),
#                 key=f"status_{task_id}"
#             )

#             comment = st.text_area("Comment", key=f"comment_{task_id}")

#             if st.button("Save", key=f"btn_{task_id}"):
#                 c.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))

#                 created_at = datetime.now().strftime("%Y-%m-%d %H:%M")  # ✅ fixed
#                 c.execute("""
#                     INSERT INTO task_activity
#                     (task_id, user_id, old_status, new_status, comment, timestamp)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                 """, (task_id, st.session_state.user_id, task_status, new_status, comment, created_at))

#                 conn.commit()
#                 for idx, task in enumerate(tasks):
#                     if task[0] == task_id:
#                         tasks[idx] = (task_id, task_title, task_desc, new_status)

# # -----------------------------
# # ROUTING
# # -----------------------------
# if not st.session_state.get("logged_in", False):
#     show_login()
# elif st.session_state.first_login == 1:
#     show_password_change()
# else:
#     if st.session_state.role == "ADMIN":
#         admin_dashboard()
#     else:
#         member_dashboard()


# import streamlit as st
# import json
# from datetime import datetime
# import pandas as pd
# import plotly.express as px
# import os

# # -----------------------------
# # JSON FILE PATHS
# # -----------------------------
# USERS_FILE = "users.json"
# TASKS_FILE = "tasks.json"
# ASSIGNMENTS_FILE = "task_assignments.json"
# ACTIVITY_FILE = "task_activity.json"

# # -----------------------------
# # HELPER FUNCTIONS FOR JSON
# # -----------------------------
# def load_json(file_path):
#     if not os.path.exists(file_path):
#         with open(file_path, "w") as f:
#             json.dump([], f)
#     with open(file_path, "r") as f:
#         return json.load(f)

# def save_json(file_path, data):
#     with open(file_path, "w") as f:
#         json.dump(data, f, indent=4)

# # -----------------------------
# # SESSION STATE INIT
# # -----------------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user_id = None
#     st.session_state.role = None
#     st.session_state.first_login = None

# # -----------------------------
# # LOGOUT FUNCTION
# # -----------------------------
# def logout():
#     st.session_state.logged_in = False
#     st.session_state.user_id = None
#     st.session_state.role = None
#     st.session_state.first_login = None

# def add_logout_topright():
#     col1, col2 = st.columns([10, 1.85])
#     with col2:
#         if st.button("Logout 🔒"):
#             logout()

# # -----------------------------
# # LOGIN SCREEN
# # -----------------------------
# def show_login():
#     st.set_page_config(page_title="Task Manager Login", layout="centered")

#     st.markdown("""
#     <style>
#     .logo-container {text-align:center;margin-top:30px;margin-bottom:20px;}
#     .login-card {background-color:#0b3d91;padding:40px 30px;max-width:420px;margin:0 auto 20px auto;border-radius:15px;box-shadow:0 10px 25px rgba(0,0,0,0.15);text-align:center;color:white;}
#     .login-card h1 {font-size:32px;margin-bottom:10px;}
#     .login-card p {color:#E63946;font-size:18px;margin-bottom:25px;}
#     .stTextInput>div>div>input {border-radius:10px !important;border:1px solid #0b3d91 !important;padding:12px !important;font-size:16px !important;}
#     div.stButton>button {width:500%;padding:12px;margin-top:0px;background-color:#0b3d91;color:white;border-radius:10px;font-size:18px;border:none;cursor:pointer;transition:0.3s;}
#     div.stButton>button:hover {background-color:#062a6c;}
#     </style>
#     """, unsafe_allow_html=True)

#     # Logo
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     # Card
#     st.markdown("""
#     <div class="login-card">
#         <h1>Task Manager</h1>
#         <p>Securely access your tasks</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # Inputs
#     username = st.text_input("Username", key="username")
#     password = st.text_input("Password", type="password", key="password")
#     st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

#     # Login button
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         login_disabled = not (username and password)
#         if st.button("Login", disabled=login_disabled):
#             users = load_json(USERS_FILE)
#             user = next((u for u in users if u["username"]==username and u["password"]==password), None)
#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user_id = user["id"]
#                 st.session_state.role = user["role"]
#                 st.session_state.first_login = user.get("first_login", 1)
#             else:
#                 st.error("Invalid username or password")

# # -----------------------------
# # PASSWORD CHANGE SCREEN
# # -----------------------------
# def show_password_change():
#     st.title("Change Your Password")
#     new_password = st.text_input("New Password", type="password")
#     confirm = st.text_input("Confirm Password", type="password")

#     if st.button("Update Password"):
#         if not new_password:
#             st.error("Password cannot be empty")
#         elif new_password != confirm:
#             st.error("Passwords do not match")
#         else:
#             users = load_json(USERS_FILE)
#             for u in users:
#                 if u["id"] == st.session_state.user_id:
#                     u["password"] = new_password
#                     u["first_login"] = 0
#             save_json(USERS_FILE, users)
#             st.session_state.first_login = 0
#             st.success("Password updated successfully")

# # -----------------------------
# # ADMIN DASHBOARD
# # -----------------------------
# def admin_dashboard():
#     add_logout_topright()
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#     /* Add your original dashboard CSS here */
#     </style>
#     """, unsafe_allow_html=True)

#     st.markdown("<h1 style='text-align:center;color:#0b3d91;'>Admin Dashboard</h1>", unsafe_allow_html=True)

#     # Tabs
#     tab1, tab2, tab3 = st.tabs(["Create & Assign Task","Member Task Board","All Tasks"])

#     # Tab 1: Create & Assign Task
#     with tab1:
#         st.subheader("Create & Assign Task")
#         with st.form("create_task_form"):
#             title = st.text_input("Task Title")
#             description = st.text_area("Description")
#             priority = st.selectbox("Priority", ["Low","Medium","High"])
#             task_type = st.selectbox("Task Type", ["Digital Initiative","Performance Management System","Departmental Manual","Dashboards"])
#             deadline = st.date_input("Deadline")
#             users = load_json(USERS_FILE)
#             members = [u for u in users if u["role"]=="MEMBER"]
#             member_map = {m["username"]: m["id"] for m in members}
#             assigned_members = st.multiselect("Assign to Members", list(member_map.keys()))

#             if st.form_submit_button("Create Task"):
#                 if not title or not assigned_members:
#                     st.error("Task title and at least one member are required")
#                 else:
#                     tasks = load_json(TASKS_FILE)
#                     task_assignments = load_json(ASSIGNMENTS_FILE)
#                     task_id = max([t["id"] for t in tasks], default=0) + 1
#                     created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
#                     tasks.append({
#                         "id": task_id,
#                         "title": title,
#                         "description": description,
#                         "priority": priority,
#                         "status": "Pending",
#                         "deadline": str(deadline),
#                         "task_type": task_type,
#                         "created_by": st.session_state.user_id,
#                         "created_at": created_at
#                     })
#                     for username in assigned_members:
#                         task_assignments.append({"task_id": task_id,"user_id": member_map[username]})
#                     save_json(TASKS_FILE, tasks)
#                     save_json(ASSIGNMENTS_FILE, task_assignments)
#                     st.success("Task created and assigned!")

#     # Tab 2: Member Task Board
#     with tab2:
#         st.subheader("Member Board Dashboard")
#         assignments = load_json(ASSIGNMENTS_FILE)
#         tasks = load_json(TASKS_FILE)
#         for m in members:
#             user_tasks_ids = [a["task_id"] for a in assignments if a["user_id"]==m["id"]]
#             user_tasks = [t for t in tasks if t["id"] in user_tasks_ids]
#             if not user_tasks:
#                 continue
#             with st.expander(f"📊 {m['username']}'s Board"):
#                 total_tasks = len(user_tasks)
#                 completed_tasks = sum(1 for t in user_tasks if t["status"]=="Completed")
#                 pending_tasks = sum(1 for t in user_tasks if t["status"]!="Completed")
#                 st.write(f"Total: {total_tasks}, Completed: {completed_tasks}, Pending: {pending_tasks}")

#     # Tab 3: All Tasks
#     with tab3:
#         st.subheader("All Tasks Overview")
#         tasks = load_json(TASKS_FILE)
#         assignments = load_json(ASSIGNMENTS_FILE)
#         users = load_json(USERS_FILE)
#         data = []
#         for t in tasks:
#             assigned_usernames = [u["username"] for u in users if any(a["user_id"]==u["id"] and a["task_id"]==t["id"] for a in assignments)]
#             data.append({
#                 "Task ID": t["id"],
#                 "Title": t["title"],
#                 "Type": t["task_type"],
#                 "Priority": t["priority"],
#                 "Status": t["status"],
#                 "Deadline": t["deadline"],
#                 "Created At": t["created_at"],
#                 "Assigned Members": ", ".join(assigned_usernames)
#             })
#         df = pd.DataFrame(data)
#         st.dataframe(df, use_container_width=True)
#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button(label="Download CSV", data=csv, file_name="tasks_report.csv", mime="text/csv")

# # -----------------------------
# # MEMBER DASHBOARD
# # -----------------------------
# def member_dashboard():
#     add_logout_topright()
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.image("Unknown.png", width=500)
#         st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#     tasks = load_json(TASKS_FILE)
#     assignments = load_json(ASSIGNMENTS_FILE)
#     my_tasks_ids = [a["task_id"] for a in assignments if a["user_id"]==st.session_state.user_id]
#     my_tasks = [t for t in tasks if t["id"] in my_tasks_ids]
#     if not my_tasks:
#         st.info("No tasks assigned to you")
#         return

#     status_percent = {"Pending":0,"In Progress":25,"Review":50,"Completed":100}
#     overall_progress = sum([status_percent[t["status"]] for t in my_tasks])/len(my_tasks)
#     st.progress(int(overall_progress))
#     st.markdown(f"<p style='text-align:center; color:#0b3d91;'>Overall Progress: {overall_progress:.1f}%</p>", unsafe_allow_html=True)

# # -----------------------------
# # ROUTING
# # -----------------------------
# if not st.session_state.logged_in:
#     show_login()
# elif st.session_state.first_login == 1:
#     show_password_change()
# else:
#     if st.session_state.role=="ADMIN":
#         admin_dashboard()
#     else:
#         member_dashboard()


import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# -----------------------------
# DATA FILE
# -----------------------------
DATA_FILE = "data.json"

# -----------------------------
# INITIALIZE DATA
# -----------------------------
if not os.path.exists(DATA_FILE):
    # Preloaded members and tasks
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
if "role" not in st.session_state:
    st.session_state.role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -----------------------------
# SAVE DATA
# -----------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

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
    .logo-container {
        text-align: center;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .role-card {
        max-width: 520px;
        margin: 0 auto 25px auto;
        padding: 25px;
        background: #f8fbff;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(11,61,145,0.10);
        text-align: center;
    }

    .role-card h1 {
        margin: 0;
        color: #0b3d91;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .role-card p {
        margin-top: 8px;
        color: #6b7fa6;
        font-size: 15px;
    }

    /* Radio buttons inline & centered */
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 35px;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px;
    }

    /* Continue button */
    div.stButton > button {
        background-color:#0b3d91;
        color:white;
        border-radius:14px;
        padding:12px 40px;
        font-size:17px;
        font-weight:600;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color:#062a6c;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Logo
    # -----------------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Unknown.png", use_container_width=True)

    # -----------------------------
    # Role Container
    # -----------------------------
    st.markdown("""
    <div class="role-card">
        <h1>Task Manager</h1>
        <p>Select your role to continue</p>
    </div>
    """, unsafe_allow_html=True)

    role = st.radio("I am a:", ["Admin", "Member"], horizontal=True)

    member_id = None

    if role == "Member":
        member_name = st.selectbox(
            "Select your name",
            [m["username"] for m in data["members"]]
        )

        member_id = next(
            (m["id"] for m in data["members"] if m["username"] == member_name),
            None
        )

    # -----------------------------
    # Centered Continue Button (outside container)
    # -----------------------------
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Continue"):
            st.session_state.role = role
            st.session_state.user_id = member_id
            st.session_state.logged_in = True


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
def admin_dashboard():
    add_logout_topright()
    st.image("Unknown.png", width=500)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width:600px; margin: 0 auto 25px auto; padding:20px; background:#f8fbff; border-radius:14px; box-shadow:0 4px 12px rgba(11,61,145,0.08); text-align:center;">
        <h1 style="margin:0; color:#0b3d91; font-weight:700; letter-spacing:1px;">Admin Dashboard</h1>
        <p style="margin-top:8px; color:#6b7fa6; font-size:15px;">Task Management & Oversight</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .stTabs [role="tablist"] button { border-radius: 25px; background-color: #0b3d91; color: white; font-weight: 600; margin-right: 5px; padding: 8px 18px; transition: 0.3s; }
    .stTabs [role="tablist"] button[aria-selected="true"] { background-color: #062a6c; }
    .dashboard-card { background-color: #0b3d91; padding: 25px 20px; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.12); color: white; margin-bottom: 20px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div { border-radius: 10px !important; border: 1px solid #0b3d91 !important; padding: 10px !important; font-size: 15px !important; background-color: white !important; color: black !important; }
    div.stButton>button { background-color: #0b3d91; color: white; border-radius: 10px; padding: 12px 0px; width: 100%; font-size: 16px; transition: 0.3s; }
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
    st.image("Unknown.png", width=500)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

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

# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.role is None:
    select_role()
else:
    if st.session_state.role == "Admin":
        admin_dashboard()
    else:
        member_dashboard()
