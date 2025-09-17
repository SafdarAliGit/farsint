frappe.ui.form.on("Item", {
    refresh(frm) {
        frm.set_query("item", "custom_item_recipe", function () {
            return {
                filters: {
                    "item_group": "Raw Material"
                }
            };
        });
    },
});

