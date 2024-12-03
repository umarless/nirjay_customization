from frappe.model.document import Document
import frappe

def create_stock_entry(doc, method):
    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.stock_entry_type = "Material Issue"
    stock_entry.purpose = "Material Issue"
    stock_entry.company = doc.company
    stock_entry.from_warehouse = doc.set_warehouse


    for item in doc.custom_item:
        item_uom = item.uom  
        item_qty = item.qty or 0  
        # item_rate = item.rate_per_box  
        item_warehouse = item.source_warehouse or doc.set_warehouse  

        stock_entry.append("items", {
            "item_code": item.item_code,
            "qty": item_qty,
            "transfer_qty" : item_qty,
            "uom": item_uom,
            "stock_uom": item_uom,
            "conversion_factor": 1,
            "basic_rate": item.basic_rate,
            "warehouse": item_warehouse,
        })

    stock_entry.insert()
    stock_entry.submit()

    frappe.msgprint(f"Stock Entry {stock_entry.name} has been created.")