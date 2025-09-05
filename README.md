# Time and Task Manager

A simple yet powerful command-line application to track time spent on customer tasks and projects. Built with Python, this tool provides full CRUD (Create, Read, Update, Delete) functionality for managing tasks and comprehensive time tracking capabilities.

## Features

### Task Management
- ✅ **Create tasks** with customer, project, and description details
- 📋 **List and view** all tasks with status and time information
- ✏️ **Update tasks** - modify any task details including status
- 🗑️ **Delete tasks** with confirmation prompts
- 📊 **Organize by customer and project** for better tracking

### Time Tracking  
- ⏱️ **Start/stop timers** for any active task
- 📈 **Automatic time calculation** with precise duration tracking
- 📝 **Work session descriptions** for detailed time entries
- 🔄 **Handle timer switching** - automatically stops current timer when starting a new one
- 💾 **Persistent storage** - all time data is saved automatically

### Reporting & Analytics
- 📋 **Task-based reports** - see time spent per task with estimates comparison
- 👤 **Customer reports** - total time and percentage breakdown by customer
- 📁 **Project reports** - analyze time distribution across projects  
- 📊 **Detailed time entries** - complete chronological view of all work sessions
- 🎯 **Progress tracking** - compare actual vs estimated hours

### User Experience
- 🖥️ **Intuitive CLI interface** with clear menus and prompts
- ⚡ **Real-time timer display** showing active work and elapsed time
- 🎨 **Visual indicators** with emojis and status symbols
- ✅ **Data validation** and error handling
- 💾 **Auto-save** functionality - never lose your data

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Quick Start

1. **Clone or download this project:**
   ```bash
   git clone <repository-url>
   cd time-task-manager
   ```

2. **Run the application:**
   ```bash
   python src/main.py
   ```

3. **Start using the application:**
   - Create your first task (option 1)
   - Start tracking time (option 5)
   - Generate reports when ready (option 7)

## Usage Guide

### Creating Tasks

When you create a new task, you'll be prompted for:
- **Title**: A descriptive name for the task
- **Description**: Additional details about the work
- **Customer**: The client or customer name
- **Project**: The project this task belongs to  
- **Estimated Hours**: (Optional) Expected time to complete

Example:
```
Task title: Implement user authentication
Task description: Add login/logout functionality with session management
Customer: Acme Corp
Project: Website Redesign
Estimated hours: 8
```

### Time Tracking Workflow

1. **Start Timer**: Select an active task and optionally add a work description
2. **Work**: The timer runs in the background, showing elapsed time in the main menu
3. **Stop Timer**: End the session - duration is automatically calculated and saved
4. **Switch Tasks**: Starting a new timer automatically stops the current one

### Understanding Task Status
- **Active** 🔄: Available for time tracking
- **Paused** ⏸️: Temporarily suspended, not available for timing
- **Completed** ✅: Finished tasks, not available for timing

### Report Types

1. **By Task**: See individual task performance vs estimates
2. **By Customer**: Understand which clients consume most time  
3. **By Project**: Analyze project time distribution
4. **All Entries**: Chronological view of every work session

## File Structure

```
time-task-manager/
├── src/
│   ├── main.py           # Application entry point
│   ├── task_manager.py   # Task CRUD operations
│   ├── time_tracker.py   # Time tracking functionality
│   └── cli_interface.py  # User interface and menus
├── data/
│   ├── tasks.json        # Task data storage (auto-created)
│   └── time_entries.json # Time entries storage (auto-created)
├── tests/                # Test files (for future expansion)
└── README.md            # This documentation
```

## Data Storage

- **JSON Format**: All data stored in human-readable JSON files
- **Auto-backup**: Files are automatically saved after each operation
- **Portable**: Simply copy the `data/` folder to backup or transfer your data
- **Location**: Data files are created in the `data/` directory

### Data Safety
- All operations are immediately persisted to disk
- JSON format allows manual data recovery if needed
- No external database dependencies

## Example Workflow

Here's a typical daily workflow:

1. **Start your day:**
   ```
   python src/main.py
   ```

2. **Check your tasks:**
   - Select option 2 to see all tasks
   - Review active tasks and priorities

3. **Begin work:**
   - Select option 5 (Start timer)
   - Choose the task you're working on
   - Add a brief description of what you'll be doing

4. **Track your time:**
   - The main menu shows your active timer
   - Take breaks as needed - timer continues running
   - Switch between tasks as priorities change

5. **End work sessions:**
   - Select option 6 (Stop timer) when finished
   - See the exact duration of your work

6. **Generate reports:**
   - Select option 7 for various reports
   - Review time spent by customer, project, or task
   - Use data for invoicing or productivity analysis

## Tips & Best Practices

### Task Organization
- Use consistent customer and project naming
- Create specific task titles for better tracking
- Set realistic time estimates to improve planning
- Update task status as work progresses

### Time Tracking
- Start timers at the beginning of focused work
- Add descriptive work session notes
- Stop timers during breaks for accurate tracking
- Review daily time entries to ensure completeness

### Reporting
- Generate customer reports for invoicing
- Use project reports for scope analysis  
- Compare estimated vs actual hours to improve future estimates
- Export or screenshot reports for client communications

## Troubleshooting

### Common Issues

**"No tasks available"**: Create a task first (option 1) before starting timers

**"Task not found"**: Ensure you're using the full task ID, which is displayed when listing tasks

**Data not saving**: Check that the application has write permissions in the data/ directory

**JSON errors**: If data files become corrupted, they will be reset automatically with a warning message

### Data Recovery
If you encounter data issues:
1. Check the `data/` directory for `.json` files
2. JSON files can be manually edited if needed
3. Delete corrupted files to reset (data will be lost)

## Technical Details

### Architecture
- **Modular design** with separate concerns
- **Object-oriented** approach for maintainability  
- **JSON persistence** for simplicity and portability
- **Type hints** throughout for better code quality

### Performance
- Lightweight and fast - handles hundreds of tasks and time entries
- Minimal memory usage
- No external dependencies or database overhead

## Contributing

This project is designed for simplicity and ease of use. Potential improvements:

- Web interface option
- CSV export functionality
- More detailed reporting options
- Team/multi-user support
- Integration with other tools

## License

This project is open source. Feel free to modify and adapt for your needs.

---

**Happy time tracking!** 📊⏱️

For questions or issues, please refer to the troubleshooting section or review the code in the `src/` directory.
