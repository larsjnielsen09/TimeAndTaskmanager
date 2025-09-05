#!/usr/bin/env python3
"""
Time and Task Manager - Main Application
A simple CRUD application to track time spent on customer tasks and projects.
"""

import sys
import os
from datetime import datetime
from task_manager import TaskManager
from time_tracker import TimeTracker
from cli_interface import CLIInterface

def main():
    """Main application entry point."""
    print("=== Time and Task Manager ===")
    print("Track your time on customer projects and tasks")
    print()
    
    # Initialize components
    task_manager = TaskManager()
    time_tracker = TimeTracker()
    cli = CLIInterface(task_manager, time_tracker)
    
    # Start the CLI interface
    cli.run()

if __name__ == "__main__":
    main()
