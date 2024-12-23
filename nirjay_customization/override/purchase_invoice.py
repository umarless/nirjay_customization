import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
    def set_missing_values(source, target, source_parent=None):
            target.custom_multi_po = 1  
            target.custom_is_expense = 1  
            target.custom_multi_purchase_order = source.name

    doc = get_mapped_doc(
        "Multi Purchase Order", 
        source_name, 
        {
            "Multi Purchase Order": {  
                "doctype": "Purchase Invoice", 
                "field_map": { 
                    "amended_from": "amended_from",  
                    "purchase_order": "purchase_order",  
                    "items": "items",  
                    "purchase_order_grand_total": "grand_total",  
                    "currency": "currency", 
                    "exchange_rate": "conversion_rate",  
                    "price_list": "price_list", 
                },
                "postprocess": set_missing_values,  
            }
        },
        target_doc  
    )

    return doc
