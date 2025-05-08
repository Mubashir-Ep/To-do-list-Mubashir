from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime

app = Flask(__name__)

# Custom filter to format datetime in Jinja2 templates
def strftime(value, format_string):
    if value is None:
        return "Not set"
    return value.strftime(format_string)

# Register the filter
app.jinja_env.filters['strftime'] = strftime

# In-memory task list (id, task, completed, start_date, end_date)
todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')

    # Validate inputs
    if not task or not start_date_str or not end_date_str:
        return "All fields are required.", 400

    try:
        # Parse dates in YYYY-MM-DD format (matches <input type="date">)
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    except ValueError as e:
        return f"Invalid date format: {str(e)}. Expected YYYY-MM-DD.", 400

    # Add task with a unique ID
    new_id = todos[-1][0] + 1 if todos else 0
    todos.append((new_id, task, False, start_date, end_date))

    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    for i, todo in enumerate(todos):
        if todo[0] == id:
            todos[i] = (todo[0], todo[1], True, todo[3], todo[4])
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    global todos
    todos = [todo for todo in todos if todo[0] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)