# Focused Tasks - Modern Todo Application

A sleek, dark-themed task management application built with PyQt6 that adapts to your workflow. It features a unique focus mode that transforms the app into a minimalist view when not actively being used.

## Screenshots

## Focused
![Screenshot 2025-04-27 235437](https://github.com/user-attachments/assets/8cd1f388-8f78-4f02-8e2e-af21fa44f458)

## Not Focused
![Screenshot 2025-04-27 235444](https://github.com/user-attachments/assets/6081352f-fe27-4653-add3-0844d6d9ebdd)



## Features

### Core Functionality
- Create, complete, and delete tasks
- Assign priority levels (Low, Medium, High)
- Sort tasks by priority, creation date, or alphabetically
- Clear completed tasks with one click
- Automatic saving of tasks between sessions

### Advanced Features
- Always-on-top mode keeps your tasks visible
- Focus/Unfocus transitions:
  - Transforms into a compact, minimalist view when unfocused
  - Shows only task names with larger text when not in focus
  - Automatically reduces window size when unfocused
  - Returns to full interface when clicked
- Modern dark theme designed for reduced eye strain
- Smooth animations and transitions
- Fully draggable interface
- Color-coded priority indicators

### User Interface
- Clean, distraction-free design
- Custom-styled checkboxes with proper checkmarks
- Consistent, modern visual language
- Compact, space-efficient layout

## Installation

### Prerequisites
- Python 3.6+
- PyQt6

### Step 1: Clone the repository
```bash
git clone https://github.com/sahilcmd3/focused-tasks.git
cd focused-tasks
```

### Step 2: Install dependencies
```bash
pip install PyQt6
```

### Step 3: Run the application
```bash
python focused_todo_app_enhanced.py
```

## Usage Guide

Convert to Executable file
## Install pyinstaller
```bash
pip install pyinstaller
```

## Run 
```bash
pyinstaller --onefile --noconsole To-Do.py
```


### Managing Tasks

#### Adding Tasks
1. Select priority level from the dropdown (Low, Medium, High)
2. Type your task in the input field
3. Click "Add" or press Enter

#### Completing Tasks
- Click the checkbox next to a task to mark it complete
- Completed tasks will be visually indicated with a strikethrough

#### Changing Priority
- Click the colored priority indicator to open the priority menu
- Select a new priority level:
  - 🔴 Red: High Priority
  - 🟡 Yellow: Medium Priority
  - 🟢 Green: Low Priority

#### Deleting Tasks
- Click the × button on the right side of a task to delete it
- Use "Clear Completed" to remove all completed tasks at once

### Sorting Options
Use the "Sort by:" dropdown to arrange tasks by:
- **Priority**: Groups by importance (High → Medium → Low)
- **Creation Date**: Orders by when tasks were added
- **Alphabetical**: Sorts A-Z by task name

### Window Management
- **Move**: Click and drag anywhere on the window
- **Minimize**: Click the – button
- **Close**: Click the × button
- **Focus/Unfocus**: 
  - Window automatically changes when focus changes
  - Click anywhere on the window when unfocused to restore full view

## Focus Mode

The unique feature of this app is its adaptive focus mode:

### When Focused (Active Window)
- Full interface with all controls visible
- Standard window size (320×480)
- Complete task management capabilities

### When Unfocused (Background Window)
- Compact window size (250×400)
- Shows only task names with larger font size
- Hides controls, title bar, and other UI elements
- Creates a clean, distraction-free list
- Remains visible but unobtrusive

This dual-mode functionality helps you keep your tasks visible while working on other applications without taking up excessive screen space.

## Technical Details

### Architecture
- Built with PyQt6 for modern UI components
- Implements custom-styled widgets throughout
- Uses JSON for data persistence
- Custom window management (frameless, movable window)

### Task Data Structure
```python
{
    "id": "20250427173314123456",  # Timestamp-based unique ID
    "text": "Example task",         # Task description
    "completed": False,             # Completion status
    "priority": "medium",           # Priority level
    "created_at": "2025-04-27 17:33:14"  # Creation timestamp
}
```

### Key Components
- **TaskCard**: Displays individual tasks with priority, checkbox, and delete button
- **PriorityButton**: Custom button for indicating and changing task priority
- **ModernTodoApp**: Main application window with focus detection and UI state management

## Customization

If you want to customize the application, here are some key areas you can modify:

### Colors
Look for these hex codes in the stylesheets:
- **Main Background**: `#1e1f21`
- **Task Card Background**: `#1e1f21`
- **Task Card Hover**: `#28292c`
- **Accent Color**: `#5865F2` (buttons, highlights)
- **Priority Colors**: 
  - High: `#ff5252`
  - Medium: `#ffc107`
  - Low: `#4caf50`

### Window Size
Modify these constants in the `ModernTodoApp` class:
```python
self.NORMAL_WIDTH = 320      # Width when focused
self.NORMAL_HEIGHT = 480     # Height when focused
self.COMPACT_WIDTH = 250     # Width when unfocused
self.COMPACT_HEIGHT = 400    # Height when unfocused
```

### Font Sizes
Look for `font-size` properties in the stylesheet definitions.

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- **Bug Reports**: Submit issues for any bugs you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with improvements
- **Documentation**: Help improve or translate the documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Created by [sahilcmd3](https://github.com/sahilcmd3)

---
