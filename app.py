#!/usr/bin/env python3
"""
Convenience entry point for Time and Task Manager
This file simply imports and runs the main application from src/main.py
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function
from main import main

if __name__ == "__main__":
    main()
