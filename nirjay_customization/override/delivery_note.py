# from frappe.model.document import Document
# import frappe

# def create_stock_entry(doc, method):
#     stock_entry = frappe.new_doc("Stock Entry")
#     stock_entry.stock_entry_type = "Material Issue"
#     stock_entry.purpose = "Material Issue"
#     stock_entry.company = doc.company
#     stock_entry.from_warehouse = doc.set_warehouse


#     for item in doc.custom_item:
#         item_uom = item.uom  
#         item_qty = item.ply or 0  
#         # item_rate = item.rate_per_box  
#         item_warehouse = item.source_warehouse or doc.set_warehouse  

#         stock_entry.append("items", {
#             "item_code": item.item_code,
#             "qty": item_qty,
#             "uom": item_uom,
#             "stock_uom": item_uom,
#             "conversion_factor": 1,
#             "basic_rate": item.rate_per_box,
#             "warehouse": item_warehouse,
#         })

#     stock_entry.insert()
#     stock_entry.submit()

#     frappe.msgprint(f"Stock Entry {stock_entry.name} has been created.")


from frappe.model.document import Document
import frappe

def create_stock_entry(doc, method):
    """
    Create a Stock Entry document for Material Issue when custom logic is triggered.
    """
    try:
        # Initialize a new Stock Entry document
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Material Issue"
        stock_entry.purpose = "Material Issue"
        stock_entry.company = doc.company
        stock_entry.from_warehouse = doc.set_warehouse

        # Iterate over custom items in the parent document
        for item in doc.custom_item:
            # Validate and fetch required fields
            item_uom = item.uom or frappe.throw(f"UOM is missing for item {item.item_code}")
            item_qty = item.ply or 0  # Default to 0 if not provided
            item_warehouse = item.source_warehouse or doc.set_warehouse
            basic_rate = item.rate_per_box or 0  # Default rate to 0

            # Validate essential fields
            if not item.item_code:
                frappe.throw("Item Code is missing for one of the items.")
            if item_qty <= 0:
                frappe.throw(f"Invalid quantity for item {item.item_code}. Quantity must be greater than 0.")

            # Append item details to the Stock Entry
            stock_entry.append("items", {
                "item_code": item.item_code,
                "qty": item_qty,
                "uom": item_uom,
                "stock_uom": item_uom,  # Assuming stock_uom is the same as item_uom
                "conversion_factor": 1,
                "basic_rate": basic_rate,
                "warehouse": item_warehouse,
            })

        # Insert and submit the Stock Entry
        stock_entry.insert()
        stock_entry.submit()

        # Notify the user
        frappe.msgprint(f"Stock Entry {stock_entry.name} has been created successfully.")

    except Exception as e:
        # Catch and log any unexpected errors
        frappe.log_error(f"Error creating Stock Entry: {str(e)}", "Stock Entry Creation")
        frappe.throw(f"An error occurred while creating the Stock Entry: {str(e)}")
