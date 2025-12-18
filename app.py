import streamlit as st
import psycopg2
import os
from datetime import date, datetime

st.set_page_config(page_title="Todo List", page_icon="✅", layout="centered")

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                priority VARCHAR(10) DEFAULT 'Medium',
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
    except psycopg2.errors.DuplicateTable:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text, completed, priority, due_date FROM todos ORDER BY created_at DESC")
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": t[0], "text": t[1], "completed": t[2], "priority": t[3], "due_date": t[4]} for t in todos]

def add_todo(text, priority, due_date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (text, priority, due_date) VALUES (%s, %s, %s)", (text, priority, due_date))
    conn.commit()
    cur.close()
    conn.close()

def update_todo_completed(todo_id, completed):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET completed = %s WHERE id = %s", (completed, todo_id))
    conn.commit()
    cur.close()
    conn.close()

def update_todo_text(todo_id, text):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET text = %s WHERE id = %s", (text, todo_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()

init_db()

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

st.title("📝 Todo List")

with st.form("add_todo_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_todo = st.text_input("Add a new task", placeholder="Enter your task here...")
    with col2:
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
    
    add_due_date = st.checkbox("Add due date")
    due_date = None
    if add_due_date:
        due_date = st.date_input("Due date", value=date.today(), min_value=date.today())
    
    submitted = st.form_submit_button("Add Task")
    
    if submitted and new_todo.strip():
        add_todo(new_todo.strip(), priority, due_date if add_due_date else None)
        st.rerun()

filter_option = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True)

todos = get_todos()

if filter_option == "Active":
    todos = [t for t in todos if not t["completed"]]
elif filter_option == "Completed":
    todos = [t for t in todos if t["completed"]]

if not todos:
    if filter_option == "All":
        st.info("No tasks yet. Add your first task above!")
    else:
        st.info(f"No {filter_option.lower()} tasks.")
else:
    st.subheader(f"Your Tasks ({len(todos)})")
    
    for todo in todos:
        with st.container():
            col1, col2, col3, col4 = st.columns([0.08, 0.55, 0.22, 0.15])
            
            with col1:
                completed = st.checkbox(
                    "Complete",
                    value=todo["completed"],
                    key=f"check_{todo['id']}",
                    label_visibility="collapsed"
                )
                if completed != todo["completed"]:
                    update_todo_completed(todo["id"], completed)
                    st.rerun()
            
            with col2:
                if st.session_state.editing_id == todo["id"]:
                    new_text = st.text_input("Edit", value=todo["text"], key=f"edit_{todo['id']}", label_visibility="collapsed")
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("Save", key=f"save_{todo['id']}"):
                            if new_text.strip():
                                update_todo_text(todo["id"], new_text.strip())
                            st.session_state.editing_id = None
                            st.rerun()
                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{todo['id']}"):
                            st.session_state.editing_id = None
                            st.rerun()
                else:
                    priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    priority_icon = priority_colors.get(todo["priority"], "")
                    
                    if todo["completed"]:
                        st.markdown(f"{priority_icon} ~~{todo['text']}~~")
                    else:
                        st.write(f"{priority_icon} {todo['text']}")
                    
                    if todo["due_date"]:
                        due = todo["due_date"]
                        if isinstance(due, str):
                            due = datetime.strptime(due, "%Y-%m-%d").date()
                        if due < date.today() and not todo["completed"]:
                            st.caption(f"⚠️ Overdue: {due}")
                        else:
                            st.caption(f"📅 Due: {due}")
            
            with col3:
                if st.session_state.editing_id != todo["id"]:
                    if st.button("✏️ Edit", key=f"edit_btn_{todo['id']}"):
                        st.session_state.editing_id = todo["id"]
                        st.rerun()
            
            with col4:
                if st.button("🗑️", key=f"delete_{todo['id']}"):
                    delete_todo(todo["id"])
                    st.rerun()
            
            st.divider()

all_todos = get_todos()
completed_count = sum(1 for t in all_todos if t["completed"])
st.caption(f"Total: {len(all_todos)} | Completed: {completed_count} | Remaining: {len(all_todos) - completed_count}")
