// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Expense Workbook"] = {
	"filters": [
		{
			fieldname: "name",
			label: __("Purchase Order"),
			fieldtype: "Link",
			options: "Purchase Order"
		}
	]
};
