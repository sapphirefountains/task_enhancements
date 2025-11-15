# File: task_enhancements/task_enhancements/task/task.py

import frappe
from frappe.utils.nestedset import NestedSet

class Task(NestedSet):
    def before_save(self):
        if self.parent_task:
            if not frappe.db.get_value("Task", self.parent_task, "is_group"):
                parent_task_doc = frappe.get_doc("Task", self.parent_task)
                parent_task_doc.is_group = 1
                parent_task_doc.save(ignore_permissions=True)

    def on_update(self):
        super(Task, self).on_update()

@frappe.whitelist()
def get_child_tasks_html(task_name):
    # Use a dedicated logger for debugging
    logger = frappe.logger("task_enhancements")
    logger.debug(f"Executing get_child_tasks_html for task: {task_name}")

    try:
        task = frappe.get_doc("Task", task_name)
        descendants = _get_all_descendants("Task", task.name)
        
        logger.debug(f"Found {len(descendants)} descendants.")
        if not descendants:
            logger.debug("No descendants found. Returning empty string.")
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
        
        logger.debug(f"Constructed a tree with {len(tree)} top-level children.")

        html_output = _build_task_tree_html(tree)
        logger.debug(f"Generated HTML (first 200 chars): {html_output[:200]}")
        
        return html_output

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Enhancements Error")
        return f"<div>An error occurred: {e}</div>"


def _get_all_descendants(doctype, parent):
    descendants = []
    children = frappe.get_all(doctype, filters={'parent_task': parent}, fields=['name'])
    for child in children:
        descendants.append(frappe.get_doc(doctype, child.name))
        descendants.extend(_get_all_descendants(doctype, child.name))
    return descendants


def _build_task_tree_html(tasks):
    if not tasks:
        return ""

    html = "<ul>"
    for task in tasks:
        html += "<li>"
        if task.children:
            html += '<i class="fa fa-minus-square toggle-child-tasks" style="cursor: pointer;"></i> '
        else:
            html += '<i class="fa fa-square-o"></i> '
        
        html += f'<a href="/app/task/{task.name}">{task.subject}</a>'
        
        if task.children:
            html += _build_task_tree_html(task.children)
            
        html += "</li>"
    html += "</ul>"
    return html
