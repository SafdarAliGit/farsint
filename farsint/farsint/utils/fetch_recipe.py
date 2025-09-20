import frappe

@frappe.whitelist()
def fetch_recipe(finish_item):
    if not finish_item:
        return {"recipe": []}

    recipe = frappe.get_all(
        "Item Recipe",
        filters={
            "parent": finish_item
        },
        fields=["item", "qty","uom", "rate", "amount"],
        order_by="idx"
    )
       
    return {
        "recipe": recipe,
    }
