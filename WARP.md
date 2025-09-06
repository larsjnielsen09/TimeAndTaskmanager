# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Time and Task Manager is a Python CLI application for tracking time spent on customer tasks and projects. It provides full CRUD functionality for task management and comprehensive time tracking capabilities with JSON-based persistent storage.

## Development Commands

### Running the Application
```bash
# Primary method (from root directory)
python app.py

# Alternative method (direct)
python src/main.py
```

### Development Setup
```bash
# No external dependencies required - uses Python standard library only
# Python 3.7+ required
python --version  # Verify Python version
```

### Testing
```bash
# No test framework currently configured
# Tests would typically be run with:
# python -m pytest tests/
# python -m unittest discover tests/
```

### Data Management
```bash
# View data files
ls data/
cat data/tasks.json      # View tasks data
cat data/time_entries.json  # View time tracking data

# Backup data
cp -r data/ data_backup_$(date +%Y%m%d)/

# Reset data (removes all tasks and time entries)
rm -f data/*.json
```

## Architecture Overview

### Core Components

**Main Application (`src/main.py`)**
- Entry point that initializes and coordinates all components
- Creates TaskManager, TimeTracker, and CLIInterface instances

**Task Management (`src/task_manager.py`)**
- `Task` dataclass: Core data model with id, title, description, customer, project, status, timestamps, estimated hours
- `TaskManager` class: Handles CRUD operations for tasks
- JSON persistence with automatic file creation and error handling
- Task status workflow: active → paused/completed

**Time Tracking (`src/time_tracker.py`)**
- `TimeEntry` dataclass: Tracks work sessions with start/end times, duration, description
- `TimeTracker` class: Manages timer operations and time calculations  
- Single active timer enforcement (auto-stops current when starting new)
- Real-time duration calculation for active timers

**CLI Interface (`src/cli_interface.py`)**
- `CLIInterface` class: Complete user interface with menu-driven navigation
- Real-time active timer display in main menu
- Comprehensive reporting (by task, customer, project, all entries)
- Input validation and confirmation prompts for destructive operations

### Data Flow

1. **Task Creation**: User input → TaskManager.create_task() → JSON persistence
2. **Time Tracking**: Select task → TimeTracker.start_timer() → Active timer state → TimeTracker.stop_timer() → Duration calculation → JSON persistence  
3. **Reporting**: Query tasks/entries → Calculate totals → Format output with percentages and comparisons

### Data Storage

- **Location**: `data/` directory (auto-created)
- **Format**: JSON files for human readability and portability
- **Files**:
  - `tasks.json`: All task data with metadata
  - `time_entries.json`: All time tracking sessions
- **Persistence**: Immediate save after each operation
- **Error Handling**: Graceful degradation with file corruption recovery

### Key Design Patterns

- **Separation of Concerns**: Each module has a single responsibility
- **Dataclass Models**: Type-safe data structures with built-in serialization
- **JSON Serialization**: Custom to_dict()/from_dict() methods for persistence
- **Active Record Pattern**: Manager classes handle both data and persistence
- **CLI State Management**: Active timer state maintained across menu navigation

### Development Notes

- Pure Python standard library - no external dependencies
- Type hints throughout for better code maintainability  
- UUID-based task/entry IDs for uniqueness
- ISO format timestamps for consistency
- Modular structure allows easy extension (web interface, API, etc.)
- Customer and project grouping enables hierarchical reporting
