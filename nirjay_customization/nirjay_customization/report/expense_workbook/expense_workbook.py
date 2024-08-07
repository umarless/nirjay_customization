# Copyright (c) 2024, Hybrowlabs Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import IfNull, Sum
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
			"width": 350,
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

# def get_data(filters):

	# po = frappe.qb.DocType("Purchase Order")
	# pi = frappe.qb.DocType("Purchase Invoice")
	# po_item = frappe.qb.DocType("Purchase Order Item")
	# pi_item = frappe.qb.DocType("Purchase Invoice Item")

# 	po = frappe.qb.DocType("Purchase Order")
# 	po_item = frappe.qb.DocType("Purchase Order Item")
# 	pi_item = frappe.qb.DocType("Purchase Invoice Item")

	# SELECT `tabPurchase Order`.`transaction_date`,
	# 	`date`,
	# 	`tabPurchase Order Item`.`schedule_date`,
	# 	`required_date`,
	# 	`tabPurchase Order Item`.`project`,
	# 	`tabPurchase Order`.`name`,
	# 	 `purchase_order`,
	# 	`tabPurchase Order`.`status`,
	# 	`tabPurchase Order`.`supplier`,
	# 	`tabPurchase Order Item`.`item_code`,
	# 	`tabPurchase Order Item`.`qty`,
	# 	`tabPurchase Order Item`.`received_qty`,
	# 	`tabPurchase Order Item`.`qty`-`tabPurchase Order Item`.`received_qty`,
	# 	`pending_qty`,
	# 	SUM(IFNULL(`tabPurchase Invoice Item`.`qty`,0)),
	# 	`billed_qty`,
	# 	`tabPurchase Order Item`.`base_amount`,
	# 	`amount`,
	# 	`tabPurchase Order Item`.`received_qty`*`tabPurchase Order Item`.`base_rate`,
	# 	`received_qty_amount`,
	# 	`tabPurchase Order Item`.`billed_amt`*IFNULL(`tabPurchase Order`.`conversion_rate`,1),
	# 	`billed_amount`,
	# 	`tabPurchase Order Item`.`base_amount`-`tabPurchase Order Item`.`billed_amt`*IFNULL(`tabPurchase Order`.`conversion_rate`,1),
	# 	`pending_amount`,`tabPurchase Order`.`set_warehouse` `warehouse`,
	# 	`tabPurchase Order`.`company`,`tabPurchase Order Item`.`name` FROM `tabPurchase Order`,
	# 	`tabPurchase Order Item` 
	# 	LEFT JOIN `tabPurchase Invoice Item`
	# 	ON `tabPurchase Invoice Item`.`po_detail`=`tabPurchase Order Item`.`name`
	# 	WHERE `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name`
	# 	AND `tabPurchase Order`.`status` NOT IN ('Stopped','Closed')
	# 	AND `tabPurchase Order`.`docstatus`= 1 
	# 	GROUP BY `tabPurchase Order Item`.`name` 
	# 	ORDER BY `tabPurchase Order`.`transaction_date`

	# query = (
	# 	frappe.qb.from_(po)
	# 	.from_(po_item)
	# 	.left_join(pi_item)
	# 	.on(pi_item.po_detail == po_item.name)
	# 	.left_join(pi)
	# 	.on(po.name == pi.payment_against_po)
	# 	.select(
	# 		po.transaction_date.as_("date"),
	# 		po_item.schedule_date.as_("required_date"),
	# 		po_item.project,
	# 		po.name.as_("purchase_order"),
	# 		po.status,
	# 		po.supplier,
	# 		pi_item.item_code,
	# 		pi_item.qty,
	# 		pi_item.base_amount,
	# 		pi_item.base_amount.as_("pi_amount"),
	# 		po_item.item_code,
	# 		po_item.qty,
	# 		po_item.received_qty,
	# 		(po_item.qty - po_item.received_qty).as_("pending_qty"),
	# 		Sum(IfNull(pi_item.qty, 0)).as_("billed_qty"),
	# 		po_item.base_amount.as_("amount"),
	# 		(po_item.received_qty * po_item.base_rate).as_("received_qty_amount"),
	# 		(po_item.billed_amt * IfNull(po.conversion_rate, 1)).as_("billed_amount"),
	# 		(po_item.base_amount - (po_item.billed_amt * IfNull(po.conversion_rate, 1))).as_(
	# 			"pending_amount"
	# 		),
	# 		po.set_warehouse.as_("warehouse"),
	# 		po.company,
	# 		po_item.name,
	# 	)
	# 	.where((pi_item.parent == po.payment_against_po) & (po_item.parent == po.name) & (po.status.notin(("Stopped", "Closed"))) & (po.docstatus == 1))
	# 	.groupby(po_item.name)
	# 	.orderby(po.transaction_date)
	# )

	# npo = filters.get(po)
	# frappe.errprint(npo)

	# for field in ("name"):
	# 	if filters.get(field):
	# 		query = query.where(po[field] == filters.get(field))

	# if filters.get("from_date") and filters.get("to_date"):
	# 	query = query.where(po.transaction_date.between(filters.get("from_date"), filters.get("to_date")))

	# if filters.get("status"):
	# 	query = query.where(po.status.isin(filters.get("status")))

	# if filters.get("project"):
	# 	query = query.where(po_item.project == filters.get("project"))

	# data2 = query.run(as_dict=True)
	# frappe.errprint(data2)
	
	# [{'date': datetime.date(2024, 7, 2),
	# 'required_date': datetime.date(2024, 7, 31),
	# 'project': None,
	# 'purchase_order': 'PUR-ORD-2024-00001',
	# 'status': 'To Receive and Bill',
	# 'supplier': 'First Supplier',
	# 'item_code': 'Charger',
	# 'qty': 1.0,
	# 'received_qty': 0.0,
	# 'pending_qty': 1.0,
	# 'billed_qty': 0.0,
	# 'amount': 60.0,
	# 'received_qty_amount': 0.0,
	# 'billed_amount': 0.0,
	# 'pending_amount': 60.0,
	# 'warehouse': None,
	# 'company': 'Hybrowlabs',
	# 'name': 'akuqd6o8bs'
	# }]
	# return data

def get_data(filters):
	
	# frappe.errprint(filters.name)
	# fname = filters.get('name')
	# frappe.errprint(fname)

	po = frappe.qb.DocType("Purchase Order")
	pi = frappe.qb.DocType("Purchase Invoice")
	po_item = frappe.qb.DocType("Purchase Order Item")
	pi_item = frappe.qb.DocType("Purchase Invoice Item")
	per = frappe.qb.DocType("Payment Entry Reference")

	# SELECT
    # `tabPurchase Order`.name,
    # `tabPurchase Order`.supplier,
    # `tabPurchase Order`.grand_total,
    # SUM(`tabPayment Entry Reference`.allocated_amount)
	# FROM `tabPurchase Order`
	# LEFT JOIN `tabPayment Entry Reference`
	# ON `tabPurchase Order`.name = `tabPayment Entry Reference`.reference_name
	# WHERE `tabPurchase Order`.name = 'PUR-ORD-2024-00002'

	# query = (
	# 	frappe.qb.from_(po)
	# 	.left_join(pi_item)
	# 	.on(pi_item.po_detail == po_item.name)
	# 	.select(
	# 		po.transaction_date.as_("date"),
	# 		po.name.as_("purchase_order"),
	# 		po.status,
	# 		po.supplier,
	# 		po.total.as_("amount"),
	# 		po.currency,
	# 		po.conversion_rate,
	# 		po.custom_freight__insurance_,
	# 		po.base_total
	# 	)
	# 	.where(po.name == filters.name)
	# )


	# for field in ("name"):
	# 	if filters.get(field):
	# 		query = query.where(po[field] == filters.get(field))
	# 		frappe.errprint(query)

	query = (
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
			Sum(per.allocated_amount).as_("total_paid")
		)
		.where(po.name == filters.name)
	)

	data2 = query.run(as_dict=True)
	# custom_expense_against_purchase_order
	query2 = (
		frappe.qb.from_(pi)
		.left_join(pi_item)
		.on(pi.name == pi_item.parent)
		.select(
			pi.custom_is_expense,
			pi.custom_expense_against_purchase_order,
			pi.name,
			pi.docstatus,
			pi.supplier,
			pi.grand_total.as_("amount"),
			pi.currency,
			pi_item.item_name,
			pi_item.item_code,
		)
		.where((pi.custom_expense_against_purchase_order == filters.name) & (pi.custom_is_expense == 1) & (pi.docstatus == 1))
	)

	expenses = query2.run(as_dict=True)
	# frappe.errprint(expenses)
	
	# query2 = [{'is_expense': 1, 'payment_against_po': 'PUR-ORD-2024-00001', 'name': 'ACC-PINV-2024-00005', 'docstatus': 1, 'supplier': 'Department of Custom Duty', 'amount': 15000.0, 'currency': 'INR', 'item_name': 'Custom Duty', 'item_code': 'Custom Duty'}, {'is_expense': 1, 'payment_against_po': 'PUR-ORD-2024-00001', 'name': 'ACC-PINV-2024-00004-1', 'docstatus': 1, 'supplier': 'Freight Agent', 'amount': 5000.0, 'currency': 'INR', 'item_name': 'Sea Freight', 'item_code': 'Sea Freight'}]

	# data = frappe.db.get_all('Purchase Order',
	# 	filters={
	# 		'name': filters.name
	# 	},
	# 	fields=['supplier', 'transaction_date', 'currency', 'conversion_rate', 'grand_total', 'base_grand_total', 'advance_paid']
	# )

	# frappe.errprint(data2)
	# frappe.errprint(po)

	second_row = {'particulars': 'Advance Paid'}
	third_row = {'particulars': 'Party Total Balance'}
	fourth_row = {'particulars': ''}

	for p in data2:
		second_row['amount']  = p.advance_paid
		third_row['amount'] = get_balance_on(party_type='Supplier', party= p.supplier)
		p['particulars'] = p.supplier + ' ' + p.date.strftime('%d-%m-%Y')+' '+ p.currency +' '+str(p.grand_total) +'@' + str(p.conversion_rate)
 
	data2.append(second_row)
	data2.append(third_row)
	data2.append(fourth_row)

	if query2:
		for e in expenses:
			new_row = {'particulars': e.item_name, 'amount': e.amount}
			data2.append(new_row)

	return data2

def validate_filters(filters):
	p_o = filters.get('name')

	if not p_o:
		frappe.throw(_("Select Purchase Order"))
