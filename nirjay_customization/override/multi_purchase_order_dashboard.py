import frappe
from frappe import _
#connection Shipment in sales order
def get_dashboard_data(data):
    data["non_standard_fieldnames"]["Sales Invoice"] = "multi_purchase_order"
    
   
    for transaction in data.get("transactions", []):
        if transaction.get("label") == _("Fulfillment"):
            transaction["items"].append("Sales Invoice")
            break
    else:
        data["transactions"].append({
            "label": _("Fulfillment"),
            "items": ["Sales Invoice"],
        })
    
    return data