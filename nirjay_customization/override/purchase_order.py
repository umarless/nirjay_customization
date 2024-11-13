import frappe

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
            total_amount = total_rate * item.custom_qty_in_pcs
            custom_duty = total_amount * item.custom_basic_duty_rate / 100
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
    # doc.reload()