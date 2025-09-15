# Task Enhancements for Frappe

## Purpose

This Frappe app enhances the default Task management system by providing a hierarchical, tree-like view of tasks within a project. It allows users to create parent-child relationships between tasks, making it easier to visualize project structure, track dependencies, and manage complex projects with many nested sub-tasks.

The core functionality is built on Frappe's `NestedSet` model, which is applied to the standard `Task` DocType.

## Features

- **Hierarchical Task View**: See all tasks for a project organized in a clear, nested tree structure.
- **Parent-Child Relationships**: Easily create sub-tasks by assigning a `parent_task` to any task.
- **Automatic Parent Grouping**: When a task is assigned a parent for the first time, the parent is automatically converted to a "group" task, enabling it to contain other tasks.
- **Dedicated Page**: A new page, "Hierarchical Task View," is added to the Desk for easy access.

## Usage

1.  Navigate to the **Hierarchical Task View** page from the Desk search bar.
2.  In the "Project" field on the page, select the project you wish to view.
3.  The tasks for that project will be displayed in a tree below the project field.
4.  To create a sub-task, simply open a standard `Task` document and set another task as its `parent_task`. The hierarchy will be automatically updated.

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/your-username/task_enhancements --branch main
bench install-app task_enhancements
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/task_enhancements
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## License

This project is licensed under the MIT License. See the `license.txt` file for details.
