// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Expense Workbook For  Multi Purchase Order"] = {
	filters: [
				{
					fieldname: "name",
					label: __("Multi Purchase Order"),
					fieldtype: "Link",
					options: "Multi Purchase Order",
					filters: {
						"docstatus": ["=", "1"]
					},
				}
			]
	
};