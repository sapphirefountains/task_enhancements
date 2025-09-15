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
