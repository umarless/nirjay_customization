import frappe

def before_save(doc, method=None):
    fi_percent = doc.custom_freight__insurance_
    custom_total_igst_assessable_value = 0
     
    for item in doc.items:
        if item.custom_pack and item.custom_basic_duty_rate:
            item.custom_qty_in_pcs = item.custom_pack * item.qty
            item.custom_rate_per_pcs = item.base_rate / item.custom_pack
            # calculation of assessable value
            fi = item.custom_rate_per_pcs * fi_percent / 100
            total_rate = item.custom_rate_per_pcs + fi
            total_amount = total_rate * item.custom_qty_in_pcs
            custom_duty = total_amount * item.custom_basic_duty_rate / 100
            sws = custom_duty * 10 / 100
            custom_igst_assessable_value = total_amount + custom_duty + sws
            item.custom_igst_assessable_value =  custom_igst_assessable_value
            custom_total_igst_assessable_value += custom_igst_assessable_value

    doc.custom_total_igst_assessable_value = custom_total_igst_assessable_value