# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Time and Task Manager is a Python application for tracking time spent on customer tasks and projects. It provides full CRUD functionality for task management and comprehensive time tracking with reporting capabilities. The application comes in two versions:

1. **CLI Application** (src/main.py) - Original command-line interface, dependency-free
2. **Web Application** (app.py) - Modern Flask web interface with manual hour entry

## Common Commands

### Running the CLI Application
```bash
python src/main.py
```

### Running the Web Application
```bash
python app.py
```
Web app will be available at http://127.0.0.1:5000

### Development Testing
```bash
# Run individual modules for testing
python -m src.task_manager
python -m src.time_tracker
python -m src.cli_interface
```

### Data Management
```bash
# View current data files
ls data/
cat data/tasks.json      # View tasks (if exists)
cat data/time_entries.json  # View time entries (if exists)
```

## Architecture Overview

### Core Components

**main.py** - Application entry point that initializes and coordinates all components:
- Creates instances of TaskManager, TimeTracker, and CLIInterface
- Serves as the composition root

**task_manager.py** - Task CRUD operations and business logic:
- `Task` dataclass: id, title, description, customer, project, status, timestamps, estimated_hours
- `TaskManager` class: handles JSON persistence, CRUD operations, filtering by customer/project
- Status management: 'active', 'completed', 'paused'

**time_tracker.py** - Time tracking functionality:
- `TimeEntry` dataclass: id, task_id, start_time, end_time, description, duration_seconds
- `TimeTracker` class: start/stop timers, calculate durations, handle active sessions
- Automatic timer switching: starting new timer stops current one
- Real-time duration calculation for active timers

**cli_interface.py** - User interface and workflow orchestration:
- Menu-driven interface with 8 main options
- Real-time timer display in main menu
- Comprehensive reporting: by task, customer, project, all entries
- Input validation and error handling

**app.py** - Flask web application:
- Modern web interface with responsive design
- Manual hour entry instead of start/stop timers
- Dashboard with statistics and recent activity
- Professional UI with Bootstrap-inspired styling
- All CRUD operations accessible via web forms

### Data Architecture

**Storage Pattern**: JSON file persistence with in-memory objects
- `data/tasks.json` - Task storage
- `data/time_entries.json` - Time entry storage  
- Auto-creates data directory and files as needed
- Immediate persistence after every operation

**UUID-based IDs**: All entities use UUID4 for unique identification

**Dataclass Pattern**: Both Task and TimeEntry use dataclasses with to_dict/from_dict methods for JSON serialization

### Key Business Rules

**Timer Management**:
- Only one timer can be active at a time
- Starting a new timer automatically stops the current one
- Active timers persist across application restarts
- Duration calculated in real-time for active sessions

**Task Status Workflow**:
- New tasks default to 'active' status
- Only 'active' tasks can have timers started
- Status affects availability in timer selection

**Time Calculation**:
- Completed entries store duration_seconds
- Active entries calculate duration dynamically
- Total task time includes both completed and active entries

## Development Patterns

### Error Handling
- JSON parsing errors reset data stores with warning messages
- File operations use makedirs with exist_ok=True
- User input validation at CLI layer

### Data Integrity
- All updates immediately persist to JSON files
- UUID collision unlikely but not explicitly handled
- No cascading deletes (time entries remain if task deleted)

### Type Safety
- Type hints used throughout codebase
- dataclasses provide structured data models
- Optional types used appropriately for nullable fields

## Testing Considerations

When making changes, verify:
1. Timer start/stop functionality works correctly
2. Task CRUD operations persist properly
3. Reports calculate time correctly (especially with active timers)
4. JSON serialization/deserialization handles all data types
5. CLI navigation and error handling

## File Structure Context

- `src/` - All source code
- `data/` - JSON data storage (gitignored except .gitkeep)
- `requirements.txt` - Documents standard library usage (no external deps)

The modular architecture allows independent testing of components, but the CLI interface coordinates all user workflows and should be the primary testing entry point for end-to-end functionality.
