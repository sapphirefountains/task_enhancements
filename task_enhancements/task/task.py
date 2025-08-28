# File: task_enhancements/task_enhancements/task/task.py

import frappe
from frappe.utils.nestedset import NestedSet

# This class overrides the standard Task DocType controller
class Task(NestedSet):
    def before_save(self):
        # This method runs before the document is saved.
        # It ensures that any task designated as a parent is marked as a group.
        if self.parent_task:
            # Check if the parent task is not already marked as a group
            if not frappe.db.get_value("Task", self.parent_task, "is_group"):
                # If it's not a group, update it to be one.
                parent_task_doc = frappe.get_doc("Task", self.parent_task)
                parent_task_doc.is_group = 1
                parent_task_doc.save(ignore_permissions=True) # Save the parent task

    def on_update(self):
        # This method is automatically called by Frappe when a document is saved.
        # It calls the standard NestedSet logic which handles all the
        # complex lft/rgt recalculations automatically.
        super(Task, self).on_update()
