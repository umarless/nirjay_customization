import frappe

def validate(doc,method=None):
    custom_set_freight_insurance(doc,method)
   

def before_save(doc, method=None):
    
    frappe.errprint(doc.custom_freight__insurance_)
    frappe.errprint(type(doc.custom_freight__insurance_))
    is_string = isinstance(doc.custom_freight__insurance_, str)
    frappe.errprint(is_string)
    if is_string:
        fi_percent = float(doc.custom_freight__insurance_)
    else:
        fi_percent = doc.custom_freight__insurance_

    custom_total_igst_assessable_value = 0
     
    for item in doc.items:
        if item.custom_pack and item.custom_basic_duty_rate:
            item.custom_qty_in_pcs = item.custom_pack * item.qty
            item.custom_rate_per_pcs = item.base_rate / item.custom_pack
            # calculation of assessable value
            frappe.errprint(item.custom_rate_per_pcs)
            frappe.errprint(type(item.custom_rate_per_pcs))
            frappe.errprint(item.base_rate / item.custom_pack)
            frappe.errprint(type(item.base_rate / item.custom_pack))
            fi = item.custom_rate_per_pcs * fi_percent / 100
            total_rate = item.custom_rate_per_pcs + fi
            item.custom_rate_per_pcs_withfreight__insurance = total_rate
            total_amount = total_rate * item.custom_qty_in_pcs
            item.custom_total_amount_freight__insurance = total_amount
            custom_duty = total_amount * item.custom_basic_duty_rate / 100
            item.custom_basic_duty_amount = custom_duty
            #  SOCIAL WELFARE SURCHARGE (%) = if 5 then take 5% of CUSTOM DUTY
            sws = 0
            if item.custom_social_welfare_surcharge_:
                sws = custom_duty * item.custom_social_welfare_surcharge_ / 100
                frappe.errprint(sws)
            else:
                sws = custom_duty * 10 / 100
                frappe.errprint("social_welfare_surcharge not set, 10%")
                frappe.errprint(sws)

            item.custom_social_welfare_surcharge = sws
            custom_igst_assessable_value = total_amount + custom_duty + sws
            item.custom_igst_assessable_value =  custom_igst_assessable_value
            custom_total_igst_assessable_value += custom_igst_assessable_value

    doc.custom_total_igst_assessable_value = custom_total_igst_assessable_value
    
    calculate_total(doc, method)
    
#calculation of custom_social_welfare_surcharge and custom duty
@frappe.whitelist()
def calculate_total(doc, method):                                                                                                                                                                                                                                                                                                                                                                                                                 
    total_c = 0
    total_s = 0
    for item in doc.items:
        total_s += item.custom_social_welfare_surcharge or 0
        total_c += item.custom_basic_duty_amount or 0
    doc.custom_custom_duty = total_c
    doc.custom_total_social_welfare_surcharge = total_s
    

# Freight + Insurance % value  fetched from the last PO
@frappe.whitelist()
def custom_set_freight_insurance(doc,method):
    if not doc.custom_freight__insurance_:
        last_po = frappe.db.get_value(
            "Purchase Order",
            {
                "supplier":doc.supplier,"docstatus":1
            },
            ["name","custom_freight__insurance_"],
            order_by="creation desc"
        )
        if last_po:
            last_po_name, last_freight_insurance = last_po
            doc.custom_freight__insurance_ = last_freight_insurance
        else:
            frappe.msgprint(f"Add Freight & Insurance (%) Value")
        

