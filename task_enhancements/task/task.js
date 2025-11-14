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
    $(".toggle-child-tasks").on("click", function(e) {
        e.preventDefault();
        $(this).closest("li").children("ul").toggle();
        $(this).toggleClass("fa-plus-square fa-minus-square");
    });
}
