# Copyright (c) 2024, Hybrowlabs Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import IfNull, Sum
from frappe.utils import today
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.utils import (
    cancel_exchange_gain_loss_journal,
    get_account_currency,
    get_balance_on,
    get_outstanding_invoices,
    get_party_types_from_account_type,
)

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

def execute(filters=None):
    if not filters:
        return [], []

    validate_filters(filters)

    columns = get_columns(filters)
    data = get_data(filters)

    if not data:
        return [], [], None, []

    # data, chart_data = prepare_data(data, filters)

    return columns, data, None

def get_columns(filters):
    return [
        {
            "label": _("Particulars"),
            "fieldname": "particulars",
            "fieldtype": "Data",
            "width": 450,
        },
        {
            "label": _("Mode of Payment"),
            "fieldname": "mode",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": _("Net Amount"),
            "fieldname": "net_amount",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": _("IGST 18%"),
            "fieldname": "igst",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": _("CGST 9%"),
            "fieldname": "cgst",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": _("SGST 9%"),
            "fieldname": "sgst",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": _("Overall Expense %"),
            "fieldname": "overall_expense",
            "fieldtype": "Float",
            "width": 180,	
        },
    ]

def get_data(filters):
    po = frappe.qb.DocType("Purchase Order")
    pi = frappe.qb.DocType("Purchase Invoice")
    # po_item = frappe.qb.DocType("Purchase Order Item")
    pi_item = frappe.qb.DocType("Purchase Invoice Item")
    per = frappe.qb.DocType("Payment Entry Reference")
    tnc = frappe.qb.DocType("Purchase Taxes and Charges")

    payment_entry_exists = frappe.db.exists("Payment Entry Reference", {"reference_name": filters.name, "docstatus": 1})

    if payment_entry_exists:
        po_per_query = (
            frappe.qb.from_(po)
            .left_join(per)
            .on(po.name == per.reference_name)
            .select(
                po.transaction_date.as_("date"),
                po.name,
                po.status,
                po.supplier,
                po.base_grand_total.as_("amount"),
                po.currency,
                po.conversion_rate,
                po.custom_freight__insurance_,
                po.base_total,
                po.advance_paid,
                po.grand_total,
                po.base_grand_total,
                per.exchange_rate,
                per.outstanding_amount,
                per.total_amount,
                per.allocated_amount,
                # Sum(per.allocated_amount).as_("total_paid")
            )
            .where((po.name == filters.name) & (po.docstatus == 1) & (per.docstatus == 1))
        )
        
        data = po_per_query.run(as_dict=True)

    else:
        po_query = (
            frappe.qb.from_(po)
            .select(
                po.transaction_date.as_("date"),
                po.name,
                po.status,
                po.supplier,
                po.base_grand_total.as_("amount"),
                po.currency,
                po.conversion_rate,
                po.custom_freight__insurance_,
                po.base_total,
                po.advance_paid,
                po.grand_total,
                po.base_grand_total,
            )
            .where((po.name == filters.name) & (po.docstatus == 1))
        )
        
        data = po_query.run(as_dict=True)

    expense_query = (
        frappe.qb.from_(pi)
        .left_join(pi_item)
        .on(pi.name == pi_item.parent)
        .select(
            pi.custom_is_expense,
            pi.custom_expense_against_purchase_order,
            pi.name,
            pi.docstatus,
            pi.supplier,
            pi.grand_total,
            pi.total,
            pi.taxes_and_charges,
            pi.total_taxes_and_charges,
            pi.base_grand_total.as_("amount"),
            pi.currency,
            pi_item.item_name,
            pi_item.item_code,
            pi_item.base_net_amount,
            pi_item.net_amount,
            pi_item.base_amount,
            pi_item.igst_amount,
            pi_item.sgst_amount,
            pi_item.cgst_amount,
            pi_item.amount
        )
        .where((pi.custom_expense_against_purchase_order == filters.name) & (pi.custom_is_expense == 1) & (pi.docstatus == 1))
    )

    expenses = expense_query.run(as_dict=True)

    pi_query = (
        frappe.qb.from_(pi)
        .left_join(pi_item)
        .on(pi.name == pi_item.parent)
        .select(
            pi.custom_is_expense,
            pi.name,
            pi.docstatus,
            pi.supplier,
            pi.currency,
            pi.conversion_rate,
            pi.grand_total,
            pi.total_advance,
            pi.base_grand_total,
            pi.outstanding_amount,
            pi.currency,
            pi_item.item_name,
            pi_item.item_code,
            pi_item.base_amount,
            pi_item.amount,
            pi_item.purchase_order
        )
        .where((pi_item.purchase_order == filters.name) & (pi.custom_is_expense == 0) & (pi.docstatus == 1))
    )

    pi_data = pi_query.run(as_dict=True)

    newdata = []
    
    todays_rate = get_exchange_rate(data[0].currency, 'INR', today())
    total_unpaid = get_balance_on(party_type='Supplier', party= data[0].supplier)
    po_balance = 0
    total_allocated_amount = 0
    po_grand_total = 0
    # if total_unpaid:
    #     total_unpaid *= -1

    # incase of only one advance payment against selected PO
    if data and len(data) == 1:
        for p in data:
            po_grand_total = p.grand_total
            first_row = {
                            'particulars': p.supplier + ' ' + p.date.strftime('%d-%m-%Y')+' '+ p.currency +' '+ str(po_grand_total) +'@' + str(p.conversion_rate),
                            'amount': p.amount
                        }

            if p.allocated_amount:
                total_allocated_amount += p.allocated_amount
                second_row = {
                                'particulars': 'Advance Paid - ' + p.currency +' '+ str(p.allocated_amount) +'@' + str(p.exchange_rate),
                                'amount' : p.allocated_amount * p.exchange_rate
                            }
                
                po_balance = p.grand_total - p.allocated_amount
                
                third_row = {
                            'particulars': 'Balance - ' + p.currency + ' ' + str(po_balance) + '@' + str(todays_rate),
                            'amount': po_balance * todays_rate
                        }
            else:
                total_allocated_amount = p.advance_paid
                second_row = {
                                'particulars': 'Advance Paid - '+ p.currency +' '+ str(p.advance_paid) +'@' + str(p.conversion_rate),
                                'amount' : p.advance_paid * p.conversion_rate
                            }
                
                po_balance = p.grand_total
                
                third_row = {
                            'particulars': 'Balance - ' + p.currency + ' ' + str(po_balance) + '@' + str(todays_rate),
                            'amount': p.grand_total * todays_rate
                        }
            
            # fourth_row = {
            #     'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' +str(total_unpaid) + '@' + str(todays_rate),
            #     'amount': total_unpaid * todays_rate
            # }
       
        newdata.append(first_row)
        newdata.append(second_row)
        newdata.append(third_row)
        # newdata.append(fourth_row)
        
            #if pi is not created then total unpaid amount row will go ====> po_balance + total_unpaid = total_party_balance
            # if pi is already created against this po then row for total payable or balance will go ====> po_balance ===> pi is created against this po ===> total_unpaid

        # incase of more than one advance payments against selected PO
    elif data and len(data) > 1:
        po_grand_total = data[0].grand_total
        first_row = {
                        'particulars': data[0].supplier + ' ' + data[0].date.strftime('%d-%m-%Y')+' '+ data[0].currency +' '+ str(po_grand_total) +'@' + str(data[0].conversion_rate),
                        'amount': data[0].amount
                    }
        
        newdata.append(first_row)
        
        for p in data:
            second_row = {
                            'particulars': 'Advance Paid - ' + p.currency +' '+ str(p.allocated_amount) +'@' + str(p.exchange_rate),
                            'amount' : p.allocated_amount * p.exchange_rate
                        }
            total_allocated_amount += p.allocated_amount
            newdata.append(second_row)
        
        po_balance = po_grand_total - total_allocated_amount

        third_row = {
                        'particulars': 'Balance - ' + data[0].currency + ' ' + str(po_balance) + '@' + str(todays_rate),
                        'amount': po_balance * todays_rate
                    }
        
        # fourth_row = {
        #     'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' +str(total_unpaid) + '@' + str(todays_rate),
        #     'amount': total_unpaid * todays_rate
        # }
        
        newdata.append(third_row)
        # newdata.append(fourth_row)
    
    # if pi created with po
    # if only one pi created for one po

    # total_unpaid can be 0 +ve and -ve
    # if pi created then total_allocated_amount is zero
    sixth_row = {}
    if pi_data:
        pi_name = pi_data[0].name
        fourth_row = {
            'particulars': 'Purchase Invioce - ' + pi_name,
            'amount': pi_data[0].base_grand_total
        }
        fifth_row = {
            'particulars': 'Advance Paid- ' + pi_data[0].currency + ' ' + str(pi_data[0].total_advance) + '@' + str(pi_data[0].conversion_rate),
            'amount': pi_data[0].total_advance * pi_data[0].conversion_rate
        }

        if total_unpaid > 0 and pi_data[0].outstanding_amount == 0:
            sixth_row = {
                'particulars': 'Total Party Balance - Already Paid',
                'amount': ''
            }
        elif total_unpaid < 0:
            sixth_row = {
                'particulars': 'Total Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                'amount': total_unpaid * todays_rate * -1
            }
        else:
            sixth_row = {
                'particulars': 'Total Party Balance - ' + data[0].currency + ' ' + str(total_unpaid) +'@'+ str(todays_rate),
                'amount': total_unpaid * todays_rate
            }
    else:
        if total_unpaid > 0 and po_balance > total_unpaid:
            if total_allocated_amount == total_unpaid:
                fourth_row = {
                    'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                    'amount': total_unpaid * todays_rate * -1
                }
                fifth_row = {
                    'particulars': 'Total Party Balance - '  + data[0].currency + ' ' + str(po_balance) +'@'+ str(todays_rate),
                    'amount': (po_balance) * todays_rate
                }
            else:
                fourth_row = {
                    'particulars': 'Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                    'amount': total_unpaid * todays_rate * -1
                }
                
                fifth_row = {
                    'particulars': 'Total Party Balance - '  + data[0].currency + ' ' + str(po_balance - total_unpaid) +'@'+ str(todays_rate),
                    'amount': (po_balance - total_unpaid) * todays_rate
                }
        elif total_unpaid > 0 and po_balance < total_unpaid:
            if total_allocated_amount == total_unpaid:
                fourth_row = {
                    'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                    'amount': total_unpaid * todays_rate * -1
                }
                
                fifth_row = {
                    'particulars': 'Total Party Balance - '  + data[0].currency + ' ' + str(po_balance) +'@'+ str(todays_rate),
                    'amount': po_balance * todays_rate
                }
            else:
                fourth_row = {
                    'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                    'amount': total_unpaid * todays_rate * -1
                }
                
                fifth_row = {
                    'particulars': 'Total Party Balance - '  + data[0].currency + ' ' + str(po_balance) +'@'+ str(todays_rate),
                    'amount': po_balance * todays_rate
                }
        elif total_unpaid == 0:
            fourth_row = {
                'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' + str(total_unpaid) +'@'+ str(todays_rate),
                'amount': total_unpaid * todays_rate
            }
            fifth_row = {
                'particulars': 'Total Party Balance - ' + data[0].currency + ' ' + str(po_balance) +'@'+ str(todays_rate),
                'amount': po_balance * todays_rate
            }
        else:
            fourth_row = {
                'particulars': 'Previous Party Balance - ' + data[0].currency + ' ' + str(total_unpaid * -1) +'@'+ str(todays_rate),
                'amount': total_unpaid * todays_rate * -1
            }
            fifth_row = {
                'particulars': 'Total Party Balance - ' + data[0].currency + ' ' + str(-1 * total_unpaid + po_balance) +'@'+ str(todays_rate),
                'amount': (-1 * total_unpaid + po_balance) * todays_rate
            }

    newdata.append(fourth_row)
    newdata.append(fifth_row)
    if sixth_row:
        newdata.append(sixth_row)

    # all expense invoices currency is INR
    # only one expense in one pi

    if expenses:
        blank_row = {
            'particulars': '***Expenses***',
            'amount': ''
        }
        newdata.append(blank_row)

        for e in expenses:
            frappe.errprint(e)
            # for igst, cgst and sgst
            # if e.taxes_and_charges:
            #     tnc_query = (
            #         frappe.qb.from_(pi)
            #         .left_join(tnc)
            #         .on(pi.name == tnc.parent)
            #         .select(
            #             pi.total_taxes_and_charges,
            #             pi.name,
            #             tnc.description,
            #             tnc.tax_amount,
            #             tnc.rate,
            #             pi.grand_total,
            #             pi.total
            #         )
            #         .where((tnc.parent == filters.name) & (pi.custom_is_expense == 1) & (pi.docstatus == 1))
            #     )

            # taxes = tnc_query.run(as_dict=True)
            
            if e.sgst_amount and e.cgst_amount:
                new_row = {
                        'particulars': e.item_name,
                        'amount': e.base_amount,
                        'net_amount': e.base_net_amount + e.sgst_amount + e.cgst_amount,
                        'sgst': e.sgst_amount,
                        'cgst':  e.cgst_amount
                    }
            elif e.igst_amount:
                new_row = {
                        'particulars': e.item_name,
                        'amount': e.base_amount,
                        'net_amount': e.base_net_amount + e.igst_amount,
                        'igst': e.igst_amount
                    }
            else:
                new_row = {
                        'particulars': e.item_name,
                        'amount': e.base_amount
                    }
            
            newdata.append(new_row)

    return newdata

def validate_filters(filters):
    p_o = filters.get('name')

    if not p_o:
        frappe.throw(_("Select Purchase Order"))
