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
        fields=["item", "qty", "rate", "amount"],
        order_by="idx"
    )
    
    if recipe:
        for i in recipe:
            item = frappe.get_doc("Item", i.item)
            i.update({
                "uom": item.stock_uom or "", 
            })
        

    return {
        "recipe": recipe,
    }
