import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TaskManager.css';

function TaskManager({ pets, apiBase }) {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({
    pet: pets[0]?.name || '',
    title: '',
    time: '09:00',
    priority: 'medium'
  });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = () => {
    axios.get(`${apiBase}/api/tasks`)
      .then(res => setTasks(res.data.tasks))
      .catch(err => console.error('Error loading tasks:', err));
  };

  const handleAddTask = (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;

    axios.post(`${apiBase}/api/tasks`, newTask)
      .then(() => {
        setNewTask({
          pet: pets[0]?.name || '',
          title: '',
          time: '09:00',
          priority: 'medium'
        });
        loadTasks();
      })
      .catch(err => console.error('Error adding task:', err));
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: '#4CAF50',
      medium: '#FF9800',
      high: '#f44336'
    };
    return colors[priority] || '#666';
  };

  return (
    <div className="task-manager">
      <h2>Task Manager</h2>

      <form className="task-form" onSubmit={handleAddTask}>
        <div className="form-row">
          <select
            value={newTask.pet}
            onChange={(e) => setNewTask({ ...newTask, pet: e.target.value })}
          >
            {pets.map(pet => (
              <option key={pet.name} value={pet.name}>
                {pet.name} ({pet.species})
              </option>
            ))}
          </select>

          <input
            type="text"
            placeholder="Task title"
            value={newTask.title}
            onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
          />

          <input
            type="time"
            value={newTask.time}
            onChange={(e) => setNewTask({ ...newTask, time: e.target.value })}
          />

          <select
            value={newTask.priority}
            onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <button type="submit">Add Task</button>
        </div>
      </form>

      <div className="tasks-list">
        <h3>Today's Tasks ({tasks.length})</h3>
        {tasks.length === 0 ? (
          <p className="empty">No tasks yet. Add one to get started!</p>
        ) : (
          <div className="tasks">
            {tasks.map((task, idx) => (
              <div key={idx} className="task-card">
                <div className="task-header">
                  <span className="task-pet">{task.pet}</span>
                  <span
                    className="task-priority"
                    style={{ color: getPriorityColor(task.priority) }}
                  >
                    {task.priority.toUpperCase()}
                  </span>
                </div>
                <h4>{task.title}</h4>
                <p className="task-time">{task.time}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TaskManager;
