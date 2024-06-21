import frappe

def before_save(doc, method=None):
    frappe.errprint(doc.name)
