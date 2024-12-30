import frappe
from frappe.utils import flt

def get_exchange_rate(currency):
    # Assuming Currency Exchange is used to fetch exchange rates
    exchange_rate = frappe.get_all('Currency Exchange', filters={'from_currency': currency}, fields=['rate'], limit=1)
    if exchange_rate:
        return flt(exchange_rate[0].rate)
    return 1  # Default to 1 if no exchange rate found

def execute(filters=None):
    if not filters:
        return [], []

    validate_filters(filters)

    # Fetch data for Multi Purchase Order with calculated GBP values
    data = get_data(filters)
    
    # Prepare the columns for the report
    columns = get_columns()

    return columns, data

def get_columns():
    # Define columns for the report
    return [
        {
            'label': 'Sr No',
            'fieldname': 'sr_no',
            'fieldtype': 'Int',
            'width': 80
        },
        {
            'label': 'Multi Purchase Order',
            'fieldname': 'name',
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'label': 'Purchase Order',
            'fieldname': 'purchase_order',
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'label': 'Expense',
            'fieldname': 'expense',
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'label': 'Expense %',
            'fieldname': 'expense_p',
            'fieldtype': 'Currency',
            'width': 150
        },
        {
            'label': 'Supplier',
            'fieldname': 'supplier',
            'fieldtype': 'Data',
            'width': 200
        },
        {
            'label': 'Total',
            'fieldname': 'total',
            'fieldtype': 'Currency',
            'width': 150
        },
        {
            'label': 'Purchase Order (%)',
            'fieldname': 'gbp',
            'fieldtype': 'Float',
            'width': 150
        },
        {
            'label': 'Status',
            'fieldname': 'status',
            'fieldtype': 'Data',
            'width': 150
        }
    ]

def validate_filters(filters):
    if not filters.get('name'):
        frappe.throw(_("Please select a Multi Purchase Order"))

def get_data(filters):
    data = []
    sr_no = 1

    # Fetch Multi Purchase Order data
    mpo_data = frappe.get_all(
        "Multi Purchase Order",
        filters=filters,
        fields=["name", "purchase_order", "purchase_order_grand_total"],
        order_by="creation desc"
    )

    # Fetch expenses for the selected Multi Purchase Order (submitted invoices)
    expenses = frappe.get_all(
        "Purchase Invoice",
        filters={
            "custom_expense_against_multi_purchase_order": filters.get("name"),
            "docstatus": 1  # Only submitted invoices
        },
        fields=["name as expense", "total as expense_amount"]
    )

    # Group the expenses into a dictionary for easy access
    expense_dict = {exp["expense"]: exp["expense_amount"] for exp in expenses}

    for mpo in mpo_data:
        # Parent row for the Multi Purchase Order
        data.append({
            "sr_no": sr_no,
            "name": mpo["name"],
            "purchase_invoice": ", ".join([expense for expense in expense_dict.keys()]),
            "purchase_order": None,
            "expense": None,
            "expense_amount": None,
            "supplier": None,
            "total": mpo["purchase_order_grand_total"],
            "gbp": None,
            "status": None,
        })

        if mpo["purchase_order"]:
            purchase_orders = [po.strip() for po in mpo["purchase_order"].split(",")]

            for po in purchase_orders:
                supplier = frappe.db.get_value("Purchase Order", po, "supplier")
                status = frappe.db.get_value("Purchase Order", po, "status")
                po_grand_total = frappe.db.get_value("Purchase Order", po, "base_total")

                # Add row for each Purchase Order
                data.append({
                    "sr_no": None,
                    "name": None,
                    "purchase_invoice": ", ".join([expense for expense in expense_dict.keys()]),
                    "purchase_order": po,
                    "expense": None,
                    "expense_amount": None,
                    "supplier": supplier,
                    "total": po_grand_total,
                    "gbp": "{:.10f}%".format((po_grand_total / mpo["purchase_order_grand_total"]) * 100) if mpo["purchase_order_grand_total"] else "0.000000000%",
                    "status": status,
                })

                # Fetch related items from the Purchase Invoice for this Purchase Order
                for expense in expenses:
                    expense_name = expense["expense"]
                    expense_amount = expense["expense_amount"]

                    # Fetch items related to the Purchase Invoice for this expense
                    items = frappe.get_all(
                        "Purchase Invoice Item",
                        filters={"parent": expense_name},
                        fields=["item_code", "item_name", "qty", "rate"]
                    )

                    total_expense_p = (flt(expense_amount) * (flt(po_grand_total) / mpo["purchase_order_grand_total"])) if mpo["purchase_order_grand_total"] else 0
                    
                    # Loop through each item in the Purchase Invoice Item child table
                    for item in items:
                        # Calculate the percentage of each expense based on the expense amount
                        item_expense_p = (flt(item["qty"]) * flt(item["rate"]) / expense_amount) * total_expense_p if expense_amount else 0

                        data.append({
                            "sr_no": None,
                            "name": None,
                            "purchase_invoice": expense_name,  # Purchase Invoice value is in the 'purchase_invoice' field
                            "purchase_order": po,
                            "expense": item["item_name"],  # Use item_name from the Purchase Invoice Item as the expense
                            "expense_amount": flt(item["qty"]) * flt(item["rate"]),  # Calculate the expense amount for the item
                            "supplier": None,
                            "total": None,
                            "gbp": None,
                            "status": None,
                            "expense_p": item_expense_p,  # Add the calculated expense percentage for each item
                        })

        sr_no += 1

    return data
