# Todo List Application

A simple and functional todo list web application built with Python, Streamlit, and PostgreSQL for managing daily tasks.

## Features

- ✅ **Add Tasks** - Quickly add new todo items with priority levels
- ✅ **Mark Complete** - Check off tasks as you finish them (with strikethrough)
- ✅ **Edit Tasks** - Modify existing task text anytime
- ✅ **Delete Tasks** - Remove tasks you no longer need
- ✅ **Priority Levels** - Assign Low (🟢), Medium (🟡), or High (🔴) priority to tasks
- ✅ **Due Dates** - Set optional due dates for tasks with overdue warnings
- ✅ **Filter Tasks** - View All, Active (incomplete), or Completed tasks
- ✅ **Persistent Storage** - All tasks saved in PostgreSQL database

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with Streamlit
- **Database**: PostgreSQL via psycopg2
- **Language**: Python 3.11+

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── main.py             # Entry point for running the app
├── requirements.txt    # Python dependencies
├── README.md          # Project overview and technical details
├── ANALYSIS.md        # Vibe coding tools research and comparative analysis
├── EXPERIENCE.md      # Development experience and learning
└── .gitignore         # Git ignore file
```

## Installation

1. Install Python 3.11 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (DATABASE_URL will be provided by Replit)

## Running the Application

```bash
python main.py
```

Or run Streamlit directly:
```bash
streamlit run app.py --server.port 5000
```

The application will be available at `http://localhost:5000`

## Usage

1. **Add a Task**:
   - Enter task text in the input field
   - Select priority level (Low, Medium, High)
   - Optionally check "Add due date" and select a date
   - Click "Add Task"

2. **Manage Tasks**:
   - Check the checkbox to mark a task as complete
   - Click "✏️ Edit" to modify task text
   - Click "🗑️" to delete a task

3. **Filter Tasks**:
   - Use the radio buttons at the top to filter between All, Active, or Completed tasks
   - Progress counter shows total, completed, and remaining tasks

## Database Schema

The application uses a single `todos` table with the following structure:

```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(10) DEFAULT 'Medium',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Features Implemented

### MVP (Core Features)
- Add, view, and delete todo items
- Mark todos as complete/incomplete
- Session-based data persistence
- Clean, simple interface

### Enhanced Features
- PostgreSQL database persistence
- Edit existing todo text
- Priority levels for tasks
- Due date management with overdue warnings
- Filter options (All/Active/Completed)
- Task count summary
