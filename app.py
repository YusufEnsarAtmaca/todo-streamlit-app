import streamlit as st

st.set_page_config(page_title="Todo List", page_icon="✅", layout="centered")

if "todos" not in st.session_state:
    st.session_state.todos = []

st.title("📝 Todo List")

with st.form("add_todo_form", clear_on_submit=True):
    new_todo = st.text_input("Add a new task", placeholder="Enter your task here...")
    submitted = st.form_submit_button("Add Task")
    
    if submitted and new_todo.strip():
        st.session_state.todos.append({
            "text": new_todo.strip(),
            "completed": False
        })
        st.rerun()

if not st.session_state.todos:
    st.info("No tasks yet. Add your first task above!")
else:
    st.subheader(f"Your Tasks ({len(st.session_state.todos)})")
    
    for i, todo in enumerate(st.session_state.todos):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        
        with col1:
            completed = st.checkbox(
                "Complete",
                value=todo["completed"],
                key=f"check_{i}",
                label_visibility="collapsed"
            )
            if completed != todo["completed"]:
                st.session_state.todos[i]["completed"] = completed
                st.rerun()
        
        with col2:
            if todo["completed"]:
                st.markdown(f"~~{todo['text']}~~")
            else:
                st.write(todo["text"])
        
        with col3:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()

    completed_count = sum(1 for t in st.session_state.todos if t["completed"])
    st.caption(f"Completed: {completed_count}/{len(st.session_state.todos)}")
