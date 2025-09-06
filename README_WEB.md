# Time and Task Manager - Web Application

This is the Flask web version of the Time and Task Manager, providing a modern web interface for managing tasks and tracking time.

## Features

- **Dashboard**: Overview of tasks, active timers, and daily statistics
- **Task Management**: Create, view, edit, and delete tasks with full CRUD operations
- **Time Tracking**: Start/stop timers for tasks with real-time updates
- **Filtering**: Filter tasks by customer, project, or status
- **Reports**: Generate reports by task, customer, project, and time entries
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Timer displays update automatically

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web Application**:
   ```bash
   python web_app.py
   ```

3. **Access the Application**:
   Open your web browser and go to: `http://127.0.0.1:5000`

## File Structure

```
├── web_app.py              # Main Flask application
├── templates/              # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── dashboard.html      # Main dashboard
│   ├── tasks.html          # Task list with filtering
│   ├── create_task.html    # Create new task form
│   ├── view_task.html      # Task details and time entries
│   ├── edit_task.html      # Edit task form
│   ├── timer.html          # Timer management page
│   └── reports.html        # Reports overview
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── app.js          # JavaScript functionality
├── src/                    # Backend modules (shared with CLI version)
│   ├── task_manager.py     # Task CRUD operations
│   ├── time_tracker.py     # Time tracking functionality
│   └── cli_interface.py    # CLI interface (not used by web app)
└── data/                   # Data storage (JSON files)
```

## Usage

### Dashboard
- View overview of your tasks and time tracking statistics
- See active timers with real-time countdown
- Quick access to create tasks and start timers

### Task Management
- **Create Tasks**: Add new tasks with customer, project, and estimated time
- **View Tasks**: See detailed task information and time entries
- **Edit Tasks**: Update task details and status
- **Filter Tasks**: Filter by customer, project, or status
- **Delete Tasks**: Remove tasks (with confirmation)

### Time Tracking
- **Start Timer**: Select a task and start tracking time
- **Stop Timer**: End current time tracking session
- **View History**: See all time entries for each task
- **Real-time Updates**: Timer displays update every second

### Reports
- **Task Report**: Time spent per task with progress tracking
- **Customer Report**: Time breakdown by customer
- **Project Report**: Time allocation across projects
- **Time Entries**: Detailed log of all time tracking sessions

## API Endpoints

- `GET /api/timer/status` - Get current timer status (for real-time updates)

## Keyboard Shortcuts

- `Ctrl+N` (or `Cmd+N` on Mac) - Create new task
- `Ctrl+T` (or `Cmd+T` on Mac) - Go to timer page
- `Escape` - Close modal dialogs

## Configuration

### Flask Configuration
Edit the following variables in `web_app.py`:

```python
app.secret_key = 'your-secret-key-change-this'  # Change for production
app.run(debug=True, host='127.0.0.1', port=5000)  # Adjust as needed
```

### Data Storage
- Tasks are stored in `data/tasks.json`
- Time entries are stored in `data/time_entries.json`
- Files are created automatically when you first run the application

## Production Deployment

For production deployment:

1. **Change the Secret Key**:
   ```python
   app.secret_key = 'your-secure-random-secret-key'
   ```

2. **Disable Debug Mode**:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. **Use a Production Server**:
   Consider using Gunicorn, uWSGI, or similar WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
   ```

4. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers supported
- JavaScript required for timer functionality

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   Change the port in `web_app.py`:
   ```python
   app.run(debug=True, host='127.0.0.1', port=5001)
   ```

2. **Template Not Found**:
   Ensure the `templates/` directory is in the same location as `web_app.py`

3. **Static Files Not Loading**:
   Ensure the `static/` directory is in the same location as `web_app.py`

4. **Timer Not Updating**:
   Check browser console for JavaScript errors and ensure you have an internet connection (for Bootstrap CDN)

### Data Backup

Your data is stored in JSON files in the `data/` directory. To backup:

```bash
# Backup your data
cp -r data/ backup-$(date +%Y%m%d)/

# Restore from backup
cp -r backup-20231106/ data/
```

## Comparison with CLI Version

| Feature | Web App | CLI App |
|---------|---------|---------|
| Interface | Modern web UI | Command line |
| Real-time Updates | ✅ Yes | ❌ No |
| Multi-user | Possible | Single user |
| Mobile Friendly | ✅ Yes | ❌ No |
| Filtering | Advanced | Basic |
| Reports | Visual | Text-based |
| Timer Display | Real-time | Manual refresh |

## License

This project shares the same license as the main Time and Task Manager project.
