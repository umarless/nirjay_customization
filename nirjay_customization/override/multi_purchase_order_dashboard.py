import frappe
from frappe import _
#connection Shipment in sales order
def get_dashboard_data(data):
    data["non_standard_fieldnames"]["Purchase Invoice"] = "multi_purchase_order"
    
   
    for transaction in data.get("transactions", []):
        if transaction.get("label") == _("Connection"):
            transaction["items"].append("Purchase Invoice")
            break
    else:
        data["transactions"].append({
            "label": _("Connection"),
            "items": ["Purchase Invoice"],
        })
    
    return data