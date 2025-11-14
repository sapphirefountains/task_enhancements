# File: task_enhancements/task_enhancements/task/task.py

import frappe
from frappe.utils.nestedset import NestedSet

class Task(NestedSet):
    """
    Overrides the standard Task DocType controller to add hierarchical capabilities.

    This class extends the NestedSet functionality to tasks, allowing them to be
    organized in a tree structure. It ensures that parent tasks are correctly

    designated as "groups" to contain sub-tasks.
    """
    def before_save(self):
        """
        Ensures that if a task is assigned a parent, the parent is marked as a group.

        This method is a Frappe hook that runs before the document is saved. It
        checks for a `parent_task` and, if found, verifies that the parent is
        flagged as a group task (`is_group` = 1). This is essential for the
        NestedSet model to function correctly.
        """
        if self.parent_task:
            if not frappe.db.get_value("Task", self.parent_task, "is_group"):
                parent_task_doc = frappe.get_doc("Task", self.parent_task)
                parent_task_doc.is_group = 1
                parent_task_doc.save(ignore_permissions=True)

    def on_update(self):
        """
        Updates the nested set tree structure after a task is saved.

        This method is a Frappe hook that is called automatically after a document
        is saved. It triggers the `on_update` method from the parent `NestedSet`
        class, which handles the complex recalculations of the left (`lft`) and
        right (`rgt`) values for the entire task tree.
        """
        super(Task, self).on_update()

@frappe.whitelist()
def get_child_tasks_html(task_name):
    """
    Gets all descendant tasks and builds a nested HTML structure for them.
    """
    task = frappe.get_doc("Task", task_name)
    # Using get_descendants() is the correct approach for a NestedSet model
    descendants = task.get_descendants()
    
    if not descendants:
        return ""

    # A dictionary to hold tasks by their name for easy lookup
    task_map = {d.name: d for d in descendants}
    # Initialize a children list for each task
    for d in descendants:
        d.children = []

    # This list will hold the top-level tasks in the hierarchy below the main task
    tree = []
    for d in descendants:
        # If the parent is the main task, it's a direct child
        if d.parent_task == task_name:
            tree.append(d)
        # If the parent is in our map, it's a nested child
        elif d.parent_task in task_map:
            task_map[d.parent_task].children.append(d)

    return _build_task_tree_html(tree)

def _build_task_tree_html(tasks):
    """
    Recursively builds an HTML unordered list for a list of tasks and their children.
    """
    if not tasks:
        return ""

    # Start the list
    html = "<ul>"
    for task in tasks:
        html += "<li>"
        # Add a toggle icon if the task has children
        if task.children:
            html += '<i class="fa fa-minus-square toggle-child-tasks" style="cursor: pointer;"></i> '
        else:
            # Use a different icon for tasks without children for visual clarity
            html += '<i class="fa fa-square-o"></i> '
        
        # Add the link to the task
        html += f'<a href="/app/task/{task.name}">{task.subject}</a>'
        
        # If there are children, recursively call this function to build the nested list
        if task.children:
            html += _build_task_tree_html(task.children)
            
        html += "</li>"
    html += "</ul>"
    return html
