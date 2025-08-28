frappe.views.TreeView.prototype.get_tree_nodes = function(doctype, parent, callback) {
    if (parent === this.doctype) {
        parent = null;
    }

    frappe.call({
        method: 'task_enhancements.task_enhancements.page.hierarchical_task_view.hierarchical_task_view.get_project_tasks_hierarchy',
        args: {
            project: this.page.fields_dict.project.get_value()
        },
        callback: function(r) {
            callback(r.message);
        }
    });
};
