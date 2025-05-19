from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'
DATA_FILE = 'todos.json'

def load_tasks():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', 
                         tasks=tasks,
                         datetime=datetime)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_data = {
            'id': str(uuid.uuid4()),
            'title': request.form['title'],
            'description': request.form.get('description', ''),
            'category': request.form.get('category', 'general'),
            'due_date': request.form['due_date'],
            'created_at': datetime.now().isoformat()
        }
        
        tasks = load_tasks()
        tasks.append(task_data)
        save_tasks(tasks)
        return redirect('/')
    
    return render_template('add.html', datetime=datetime)  # Critical fix here

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = [t for t in load_tasks() if t['id'] != task_id]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    app.run(debug=True)