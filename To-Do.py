import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLineEdit, QPushButton, QScrollArea, QLabel,
                             QCheckBox, QFrame, QSizePolicy, QComboBox, QMenu)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize, pyqtProperty
from PyQt6.QtGui import QColor, QPalette, QIcon, QFont, QFontDatabase, QAction


class PriorityButton(QPushButton):
    def __init__(self, priority, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(22, 22)
        self.setProperty("priority", priority)
        self.updateStyle()

    def updateStyle(self):
        priority = self.property("priority")

        # Set color based on priority
        if priority == "high":
            color = "#ff5252"
            hover_color = "#ff7070"
            tooltip = "High Priority"
            text = "!"
        elif priority == "medium":
            color = "#ffc107"
            hover_color = "#ffcd38"
            tooltip = "Medium Priority"
            text = "!"
        else:  # low
            color = "#4caf50"
            hover_color = "#6abe6d"
            tooltip = "Low Priority"
            text = "!"

        self.setText(text)
        self.setToolTip(tooltip)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 11px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)


class TaskCard(QFrame):
    def __init__(self, task_text, task_id, completed=False, priority="low", parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.completed = completed
        self.priority = priority
        self.parent_widget = parent

        # Set up the card appearance - MATCHING MAIN BACKGROUND COLOR
        self.setObjectName("taskCard")
        self.setStyleSheet("""
            #taskCard {
                background-color: #1e1f21;
                border-radius: 8px;
                padding: 2px;
                margin: 2px 1px;
            }
            #taskCard:hover {
                background-color: #28292c;
            }
        """)

        # Set up layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)

        # Priority indicator
        self.priority_btn = PriorityButton(priority)
        self.priority_btn.clicked.connect(self.show_priority_menu)
        self.layout.addWidget(self.priority_btn)

        # Checkbox - using image for checkmark
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(completed)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #6a6a6a;
            }
            QCheckBox::indicator:unchecked {
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                background-color: #5865F2;
                border: 2px solid #5865F2;
                image: url('checkmark.png');
            }
            QCheckBox::indicator:hover {
                border: 2px solid #5865F2;
            }
        """)
        self.checkbox.stateChanged.connect(self.on_status_change)
        self.layout.addWidget(self.checkbox)

        # Task text
        self.task_label = QLabel(task_text)
        self.task_label.setWordWrap(True)
        self.update_text_style()
        self.layout.addWidget(self.task_label, 1)  # 1 is stretch factor

        # Delete button
        self.delete_btn = QPushButton("×")
        self.delete_btn.setObjectName("deleteTaskBtn")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            #deleteTaskBtn {
                background-color: transparent;
                border: none;
                color: #6c757d;
                font-size: 18px;
                font-weight: bold;
                padding: 0px 3px;
            }
            #deleteTaskBtn:hover {
                color: #ff5252;
            }
        """)
        self.delete_btn.clicked.connect(self.on_delete)
        self.layout.addWidget(self.delete_btn)

        # Animation properties
        self.setGraphicsEffect(None)  # Initialize without effect

        # Animation for task completion
        self.animation = QPropertyAnimation(self, b"background_color")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def switch_to_minimalist_view(self):
        # Only show task text when out of focus
        self.priority_btn.hide()
        self.checkbox.hide()
        self.delete_btn.hide()

        # Update margins for cleaner look
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Make task label use available space with LARGER FONT (+2)
        if self.completed:
            self.task_label.setStyleSheet("""
                color: #6e7175;
                font-family: 'Segoe UI';
                font-size: 14px; /* Increased by 2 from 12px */
                text-decoration: line-through;
            """)
        else:
            self.task_label.setStyleSheet("""
                color: #e0e1e2;
                font-family: 'Segoe UI';
                font-size: 14px; /* Increased by 2 from 12px */
            """)

    def switch_to_full_view(self):
        # Show all controls when in focus
        self.priority_btn.show()
        self.checkbox.show()
        self.delete_btn.show()

        # Restore original margins
        self.layout.setContentsMargins(8, 8, 8, 8)

        # Restore original text style
        self.update_text_style()

    def show_priority_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1f21;
                color: #e0e1e2;
                border: 1px solid #3e3e42;
                padding: 5px;
                border-radius: 6px;
            }
            QMenu::item {
                padding: 5px 15px;
            }
            QMenu::item:selected {
                background-color: #28292c;
            }
        """)

        high_action = QAction("High Priority", self)
        high_action.triggered.connect(lambda: self.set_priority("high"))

        medium_action = QAction("Medium Priority", self)
        medium_action.triggered.connect(lambda: self.set_priority("medium"))

        low_action = QAction("Low Priority", self)
        low_action.triggered.connect(lambda: self.set_priority("low"))

        menu.addAction(high_action)
        menu.addAction(medium_action)
        menu.addAction(low_action)

        menu.exec(self.priority_btn.mapToGlobal(self.priority_btn.rect().bottomLeft()))

    def set_priority(self, priority):
        self.priority = priority
        self.priority_btn.setProperty("priority", priority)
        self.priority_btn.updateStyle()
        if self.parent_widget:
            self.parent_widget.update_task_priority(self.task_id, priority)

    def on_status_change(self):
        self.completed = self.checkbox.isChecked()
        if self.parent_widget:
            self.parent_widget.update_task(self.task_id, self.completed)
        self.update_text_style()

        # Animate background color change
        if self.completed:
            self.animation.setStartValue(QColor("#1e1f21"))
            self.animation.setEndValue(QColor("#1e1f21"))  # Keep same background
        else:
            self.animation.setStartValue(QColor("#1e1f21"))
            self.animation.setEndValue(QColor("#1e1f21"))  # Keep same background
        self.animation.start()

    def on_delete(self):
        if self.parent_widget:
            self.parent_widget.delete_task(self.task_id)

    def update_text_style(self):
        if self.completed:
            self.task_label.setStyleSheet("""
                color: #6e7175;
                font-family: 'Segoe UI';
                font-size: 13px;
                text-decoration: line-through;
            """)
        else:
            self.task_label.setStyleSheet("""
                color: #f8f9fa;
                font-family: 'Segoe UI';
                font-size: 13px;
            """)

    # Property for animation
    def _get_background_color(self):
        return self.palette().color(QPalette.ColorRole.Window)

    def _set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

    background_color = pyqtProperty(QColor, _get_background_color, _set_background_color)


class ModernTodoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # App state
        self.is_focused = True

        # Window size constants
        self.NORMAL_WIDTH = 320
        self.NORMAL_HEIGHT = 480
        self.COMPACT_WIDTH = 250  # Smaller width when unfocused
        self.COMPACT_HEIGHT = 400  # Smaller height when unfocused

        # Generate checkmark image
        self.create_checkmark_image()

        # App data
        self.tasks = []
        self.normal_opacity = 1.0
        self.faded_opacity = 0.85

        # Window setup
        self.setWindowTitle("Todo")
        self.setFixedSize(self.NORMAL_WIDTH, self.NORMAL_HEIGHT)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # Pin to screen
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Frameless window

        # Apply rounded corners style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1f21;
                border-radius: 10px;
                border: 1px solid #3d3d3d;
            }
        """)

        # Load saved tasks
        self.load_tasks()

        # Setup UI
        self.setup_ui()

        # Connect focus events
        self.installEventFilter(self)

        # Store references to task cards
        self.task_cards = []

    def create_checkmark_image(self):
        # Create a simple checkmark image
        try:
            from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush

            # Create a transparent pixmap
            pixmap = QPixmap(12, 12)
            pixmap.fill(Qt.GlobalColor.transparent)

            # Create painter
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Set pen to white
            pen = QPen(QColor("white"))
            pen.setWidth(2)
            painter.setPen(pen)

            # Draw checkmark
            painter.drawLine(2, 6, 5, 9)
            painter.drawLine(5, 9, 10, 3)

            # End painting
            painter.end()

            # Save image
            pixmap.save("checkmark.png")
        except Exception as e:
            print(f"Could not create checkmark image: {e}")

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == event.Type.WindowActivate:
                self.on_focus_gained()
            elif event.type() == event.Type.WindowDeactivate:
                self.on_focus_lost()
        return super().eventFilter(obj, event)

    def on_focus_gained(self):
        self.is_focused = True
        self.setWindowOpacity(self.normal_opacity)

        # Restore original window size
        self.setFixedSize(self.NORMAL_WIDTH, self.NORMAL_HEIGHT)

        # Show full UI
        self.show_full_view()

    def on_focus_lost(self):
        self.is_focused = False
        self.setWindowOpacity(self.faded_opacity)

        # Reduce window size
        self.setFixedSize(self.COMPACT_WIDTH, self.COMPACT_HEIGHT)

        # Show minimalist UI (just task names)
        self.show_minimalist_view()

    def show_full_view(self):
        # Show all UI controls
        self.title_bar.show()
        self.input_widget.show()
        self.sort_widget.show()
        self.status_widget.show()

        # Show all task card controls
        for task_card in self.task_cards:
            task_card.switch_to_full_view()

    def show_minimalist_view(self):
        # Hide non-essential UI elements
        self.title_bar.hide()
        self.input_widget.hide()
        self.sort_widget.hide()
        self.status_widget.hide()

        # Show only task names in task cards with larger font
        for task_card in self.task_cards:
            task_card.switch_to_minimalist_view()

    def setup_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Smaller margins
        main_layout.setSpacing(10)  # Reduced spacing

        # Set the dark theme
        main_widget.setStyleSheet("""
            background-color: #1e1f21;
            color: #e0e1e2;
            border-radius: 10px;
        """)
        self.setCentralWidget(main_widget)

        # Custom title bar with move functionality
        self.title_bar = QWidget()
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 0, 5)  # Reduced bottom margin

        # App title
        app_title = QLabel("Focused Tasks")
        app_title.setStyleSheet("""
            color: #e0e1e2;
            font-family: 'Segoe UI';
            font-size: 18px;  /* Smaller font */
            font-weight: bold;
        """)
        title_layout.addWidget(app_title)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)  # Smaller button
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ff5252;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

        # Minimize button
        min_btn = QPushButton("–")
        min_btn.setFixedSize(26, 26)  # Smaller button
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #5865F2;
            }
        """)
        min_btn.clicked.connect(self.showMinimized)
        title_layout.insertWidget(1, min_btn, 0, Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.title_bar)

        # Make title bar draggable
        app_title.mouseMoveEvent = self.move_window
        app_title.mousePressEvent = self.get_pos

        # Input area with priority selection
        self.input_widget = QWidget()
        input_layout = QHBoxLayout(self.input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)  # Reduced spacing

        # Priority selector for new tasks - with matched height
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentIndex(0)
        self.priority_combo.setFixedHeight(36)  # Match heights
        self.priority_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1f21;
                color: #e0e1e2;
                border: 1px solid #3e3e42;
                border-radius: 6px;
                padding: 2px 10px;
                font-family: 'Segoe UI';
                font-size: 12px;
                min-width: 80px;
                max-width: 80px;
            }
            QComboBox:hover {
                border: 1px solid #5865F2;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1f21;
                color: #e0e1e2;
                border: 1px solid #3e3e42;
                selection-background-color: #5865F2;
                border-radius: 6px;
            }
        """)
        input_layout.addWidget(self.priority_combo)

        # Task input field - with matched height
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task...")
        self.task_input.setFixedHeight(36)  # Match heights
        self.task_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1f21;
                border: 1px solid #3e3e42;
                border-radius: 6px;
                color: #e0e1e2;
                padding: 2px 10px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #5865F2;
            }
        """)
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input)

        # Add button - with matched height
        add_btn = QPushButton("Add")
        add_btn.setFixedHeight(36)  # Match heights
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 2px 12px;
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4752c4;
            }
            QPushButton:pressed {
                background-color: #3c45a5;
            }
        """)
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(add_btn)

        main_layout.addWidget(self.input_widget)

        # Sort options - more compact
        self.sort_widget = QWidget()
        sort_layout = QHBoxLayout(self.sort_widget)
        sort_layout.setContentsMargins(0, 0, 0, 0)

        # Sort label
        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("""
            color: #6c757d;
            font-family: 'Segoe UI';
            font-size: 11px;
        """)
        sort_layout.addWidget(sort_label)

        # Sort options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Priority", "Creation Date", "Alphabetical"])
        self.sort_combo.setCurrentIndex(0)  # Default to Priority
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                color: #e0e1e2;
                border: none;
                padding: 0px 5px;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
            QComboBox:hover {
                color: #5865F2;
            }
            QComboBox::drop-down {
                border: none;
                width: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1f21;
                color: #e0e1e2;
                border: 1px solid #3e3e42;
                selection-background-color: #5865F2;
                border-radius: 4px;
            }
        """)
        self.sort_combo.currentIndexChanged.connect(lambda: self.render_tasks())
        sort_layout.addWidget(self.sort_combo)

        sort_layout.addStretch(1)  # Push everything to the left

        main_layout.addWidget(self.sort_widget)

        # Tasks area
        tasks_container = QWidget()
        tasks_layout = QVBoxLayout(tasks_container)
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(0)

        # Scrollable area for tasks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1f21;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #1e1f21;
                width: 8px;  /* Thinner scrollbar */
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #3e3e42;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5865F2;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setContentsMargins(2, 2, 2, 2)  # Smaller margins
        self.tasks_layout.setSpacing(6)  # Smaller spacing
        self.tasks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.tasks_widget)
        tasks_layout.addWidget(self.scroll_area)

        main_layout.addWidget(tasks_container, 1)  # 1 is stretch factor

        # Status bar - more compact
        self.status_widget = QWidget()
        status_layout = QHBoxLayout(self.status_widget)
        status_layout.setContentsMargins(0, 3, 0, 0)  # Smaller margins

        # Date display
        date_label = QLabel(f"Today: {datetime.now().strftime('%Y-%m-%d')}")
        date_label.setStyleSheet("""
            color: #6c757d;
            font-family: 'Segoe UI';
            font-size: 10px;  /* Smaller text */
        """)
        status_layout.addWidget(date_label)

        # Clear completed button
        clear_btn = QPushButton("Clear Completed")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: none;
                font-family: 'Segoe UI';
                font-size: 10px;  /* Smaller text */
                padding: 3px 8px;  /* Smaller padding */
            }
            QPushButton:hover {
                color: #5865F2;
                text-decoration: underline;
            }
        """)
        clear_btn.clicked.connect(self.clear_completed)
        status_layout.addWidget(clear_btn, 0, Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(self.status_widget)

        # Make the tasks widget area draggable too
        self.tasks_widget.mouseMoveEvent = self.move_window
        self.tasks_widget.mousePressEvent = self.get_pos
        self.scroll_area.mouseMoveEvent = self.move_window
        self.scroll_area.mousePressEvent = self.get_pos

        # Render existing tasks
        self.render_tasks()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Store the initial position for dragging
            self.dragPos = event.globalPosition().toPoint()

            # If clicked while in minimalist view, switch back to full view
            if not self.is_focused:
                self.activateWindow()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Move window
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def get_pos(self, event):
        self.dragPos = event.globalPosition().toPoint()

        # If clicked while in minimalist view, switch back to full view
        if not self.is_focused:
            self.activateWindow()

    def move_window(self, event):
        # If left mouse button is pressed
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Move window
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def add_task(self):
        task_text = self.task_input.text().strip()
        priority = self.priority_combo.currentText().lower()

        if task_text:
            task_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            self.tasks.append({
                "id": task_id,
                "text": task_text,
                "completed": False,
                "priority": priority,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.task_input.clear()
            self.save_tasks()
            self.render_tasks()

    def update_task(self, task_id, completed):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = completed
                break
        self.save_tasks()

    def update_task_priority(self, task_id, priority):
        for task in self.tasks:
            if task["id"] == task_id:
                task["priority"] = priority
                break
        self.save_tasks()
        self.render_tasks()  # Re-render tasks to apply sorting

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        self.render_tasks()

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        self.render_tasks()

    def render_tasks(self):
        # Clear existing tasks and references
        self.task_cards = []
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.tasks:
            empty_label = QLabel("Add a new task above")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("""
                color: #6c757d;
                font-family: 'Segoe UI';
                font-size: 13px;
                font-style: italic;
                padding: 20px 0px;
            """)
            self.tasks_layout.addWidget(empty_label)
            return

        # Sort tasks based on the selected sort method
        sort_method = self.sort_combo.currentText()

        if sort_method == "Priority":
            # Sort by priority (high > medium > low) and then by completion status
            priority_order = {"high": 0, "medium": 1, "low": 2}
            sorted_tasks = sorted(
                self.tasks,
                key=lambda x: (
                    x["completed"],  # Incomplete first
                    priority_order.get(x["priority"], 3),  # Then by priority
                    x["created_at"]  # Then by date
                )
            )
        elif sort_method == "Creation Date":
            # Sort by creation date (newest first) and then by completion status
            sorted_tasks = sorted(
                self.tasks,
                key=lambda x: (
                    x["completed"],  # Incomplete first
                    x["created_at"]  # Then by date
                )
            )
        else:  # Alphabetical
            # Sort alphabetically by text and then by completion status
            sorted_tasks = sorted(
                self.tasks,
                key=lambda x: (
                    x["completed"],  # Incomplete first
                    x["text"].lower()  # Then alphabetically
                )
            )

        for task in sorted_tasks:
            priority = task.get("priority", "low")  # Default to low if not specified
            task_card = TaskCard(
                task["text"],
                task["id"],
                task["completed"],
                priority,
                self
            )
            self.tasks_layout.addWidget(task_card)
            self.task_cards.append(task_card)

        # Apply current view state if not focused
        if not self.is_focused:
            self.show_minimalist_view()

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            if os.path.exists("tasks.json"):
                with open("tasks.json", "r") as file:
                    self.tasks = json.load(file)

                    # Ensure all tasks have a priority field
                    for task in self.tasks:
                        if "priority" not in task:
                            task["priority"] = "low"
        except Exception as e:
            print(f"Error loading tasks: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show the application
    window = ModernTodoApp()
    window.show()

    sys.exit(app.exec())