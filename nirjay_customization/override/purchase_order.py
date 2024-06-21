import frappe

def before_save(doc, method=None):
    frappe.errprinnt(doc.name)
