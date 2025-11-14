frappe.ui.form.on("Task", {
    refresh: function(frm) {
        if (frm.doc.is_group && !frm.is_new()) {
            frappe.call({
                method: "task_enhancements.task.task.get_child_tasks_html",
                args: {
                    task_name: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frm.fields_dict.custom_child_tasks_table.html(r.message);
                        frm.refresh_field("custom_child_tasks_table");
                        add_toggle_functionality();
                    }
                }
            });
        } else {
            frm.fields_dict.custom_child_tasks_table.html("");
            frm.refresh_field("custom_child_tasks_table");
        }
    }
});

function add_toggle_functionality() {
    // This event handler is delegated and will work for nested elements
    $("#custom_child_tasks_table").on("click", ".toggle-child-tasks", function(e) {
        e.preventDefault();
        // Toggle the UL that is a direct child of the same LI as the icon
        $(this).closest("li").children("ul").toggle();
        // Switch the icon class
        $(this).toggleClass("fa-plus-square fa-minus-square");
    });
}
