import frappe

def before_save(doc, method=None):
    if doc.name:
        frappe.errprinnt(doc.name)
