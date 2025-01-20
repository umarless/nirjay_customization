// Copyright (c) 2025, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Invoice Item Report"] = {
	filters: [
		{
			"fieldname": "purchase_invoice",
			"label": __("Purchase Invoice"),
			"fieldtype": "Link",
			"options" : "Purchase Invoice",
			"reqd": 1,
			filters: {
				"docstatus": ["=", "1"]
			},
		},
	],
};
