# your_app/api.py
import frappe

@frappe.whitelist()
def fetch_recipe(finish_item, warehouse=None):
    """
    Fetch recipe lines and attach valuation_rate (from Stock Ledger Entry) per item.
    """

    if not finish_item:
        return {"recipe": []}

    # Get recipe lines
    recipe = frappe.get_all(
        "Item Recipe",
        filters={"parent": finish_item},
        fields=["item", "qty", "uom", "rate", "amount"],
        order_by="idx"
    )

    # For efficiency, get a list of distinct items in recipe
    items = list({row.get("item") for row in recipe if row.get("item")})

    # Prepare valuation rates mapping
    val_rates = {}
    for item_code in items:
        # get latest SLE for this item (and optional warehouse)
        sle_filters = {
            "item_code": item_code,
            "is_cancelled": 0
        }
        if warehouse:
            sle_filters["warehouse"] = warehouse

        sle = frappe.get_list(
            "Stock Ledger Entry",
            filters=sle_filters,
            fields=["valuation_rate"],
            order_by="posting_date DESC, posting_time DESC",
            limit=1
        )
        if sle and sle[0].valuation_rate is not None:
            val_rates[item_code] = sle[0].valuation_rate
        else:
            val_rates[item_code] = 0.0

    # Now build recipe list with valuation_rate added
    recipe_with_valuation = []
    for row in recipe:
        item_code = row.get("item")
        row_rate = val_rates.get(item_code, 0.0)
        # Add a key "valuation_rate" to each row
        new_row = row.copy()
        new_row["valuation_rate"] = row_rate
        recipe_with_valuation.append(new_row)

    return {
        "recipe": recipe_with_valuation
    }
