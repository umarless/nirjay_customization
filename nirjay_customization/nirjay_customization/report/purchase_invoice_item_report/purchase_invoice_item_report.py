# Copyright (c) 2025, Hybrowlabs Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, cint

def execute(filters=None):
    # Columns
    columns = get_columns()

    # Data
    data = get_data(filters)

    # Update data with currency symbol
    data = add_currency_symbol(data, filters)

    return columns, data

def get_columns():
    # Define columns for the report
    return [
        {"fieldname": "purchase_invoice", "label": "Purchase Invoice", "fieldtype": "Link", "options": "Purchase Invoice", "width": 150},
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "qty", "label": "Quantity", "fieldtype": "Float", "width": 100},
        {"fieldname": "rate", "label": "Rate", "fieldtype": "Data", "width": 120},  # Changed fieldtype to Data to include currency sign
        {"fieldname": "amount", "label": "Amount", "fieldtype": "Data", "width": 120},  # Changed fieldtype to Data to include currency sign
        {"fieldname": "custom_rate_per_pcs", "label": "Rate per Pcs", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_basic_duty_rate", "label": "Basic Duty Rate(%)", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_social_welfare_surcharge_", "label": "Social Welfare Surcharge (%)", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_rate_per_pcs_withfreight__insurance", "label": "Rate Per Pcs (with Freight + Insurance%)", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_total_amount_freight__insurance", "label": "Total Amount (Freight + Insurance)", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_custom_duty_amount", "label": "Custom Duty Amount", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_social_welfare_surcharge_amount", "label": "Social Welfare Surcharge (Amount)", "fieldtype": "Data", "width": 100},
        {"fieldname": "custom_igst_assessable_value", "label": "IGST Assessable Value", "fieldtype": "Data", "width": 100},
    ]

def get_data(filters):
    # Base query
    query = """
        SELECT
            pi.name AS purchase_invoice,
            pi.currency,
            pii.item_code,
            pii.item_name,
            pii.qty,
            pii.rate,
            pii.amount,
            pii.custom_rate_per_pcs,
            pii.custom_basic_duty_rate,
            pii.custom_social_welfare_surcharge_,
            pii.custom_total_amount_freight__insurance,
            pii.custom_rate_per_pcs_withfreight__insurance,
            pii.custom_custom_duty_amount,
            pii.custom_social_welfare_surcharge_amount,
            pii.custom_igst_assessable_value
        FROM
            `tabPurchase Invoice` pi
        JOIN
            `tabPurchase Invoice Item` pii ON pii.parent = pi.name
        WHERE
            pi.docstatus = 1
    """

    # Apply filters for selected Purchase Invoices
    if filters and filters.get("purchase_invoice"):
        query += " AND pi.name = %(purchase_invoice)s"

    # Execute query and return data
    return frappe.db.sql(query, filters, as_dict=True)

def add_currency_symbol(data, filters):
    """Add currency sign to rate and amount fields."""
    if not data:
        return data

    # Fetch currency for the first record (assuming all rows share the same currency for a report)
    currency = data[0].get("currency", frappe.defaults.get_global_default("currency"))

    # Add currency sign to rate and amount
    for row in data:
        row["rate"] = f"{currency} {row['rate']}"
        row["amount"] = f"{currency} {row['amount']}"

    return data
