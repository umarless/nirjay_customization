// Copyright (c) 2024, Hybrowlabs Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Multi Purchase Order', {
    // Trigger when the form is loaded or refreshed
    refresh: function (frm) {
        // Recalculate grand total on refresh
        calculate_grand_total(frm);

    
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Purchase Invoice'), function () {
                frappe.model.open_mapped_doc({
                    method: "nirjay_customization.override.purchase_invoice.make_purchase_invoice", 
                    frm: frm,
                });
            }, __("Create"));
        }

    },
    
    // Custom function for adding purchase orders
    add_po: function (frm) {
        let selectedOrders = frm.doc.purchase_order
            ? frm.doc.purchase_order.split(',').map(order => order.trim()).filter(Boolean)
            : [];

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Purchase Order',
                fields: ['name', 'grand_total'], // Fetch name and grand total of Purchase Orders
                filters: {
                    docstatus: ['!=', 2] // Exclude canceled Purchase Orders
                },
                limit_page_length: 0,
            },
            callback: function (response) {
                if (response.message) {
                    let options = response.message
                        .filter(po => !selectedOrders.includes(po.name)) // Exclude selected orders
                        .map(po => ({
                            value: po.name,
                            description: `Grand Total: ${po.grand_total}`
                        })); // Add grand total to description

                    const dialog = new frappe.ui.Dialog({
                        title: __('Select Purchase Order'),
                        fields: [
                            {
                                label: __("Select Purchase Order"),
                                fieldtype: "MultiSelectList",
                                fieldname: "purchase_order",
                                placeholder: "Select Purchase Orders",
                                options: options,
                                reqd: 1,
                                get_data: function () {
                                    return options;
                                }
                            }
                        ],
                        primary_action_label: __('Submit'),
                        primary_action: function (values) {
                            let newOrders = values['purchase_order'] || [];
                            let duplicates = newOrders.filter(order => selectedOrders.includes(order));

                            if (duplicates.length > 0) {
                                frappe.msgprint(
                                    __("The following Purchase Orders are already selected: {0}.", [duplicates.join(', ')])
                                );
                            } else {
                                selectedOrders = [...new Set([...selectedOrders, ...newOrders])];
                                frm.set_value("purchase_order", selectedOrders.join(', '));
                                frm.refresh_field('purchase_order');

                                // Add selected Purchase Orders to the child table
                                response.message.forEach(po => {
                                    if (newOrders.includes(po.name) && !frm.doc.items.some(row => row.purchase_order === po.name)) {
                                        let newRow = frm.add_child('items');
                                        newRow.purchase_order = po.name;
                                        newRow.purchase_order_grand_total = po.grand_total; // Set grand total
                                    }
                                });

                                frm.refresh_field('items'); // Refresh the 'items' child table
                                calculate_grand_total(frm); // Update the parent grand total
                            }

                            dialog.hide();
                            $('body').removeClass('modal-open');
                        }
                    });

                    dialog.show();
                    $('body').addClass('modal-open');

                    let userCount = options.length;
                    let dynamicHeight = userCount * 100;
                    if (userCount > 10) {
                        dynamicHeight = 300;
                    }

                    dialog.$wrapper.find('.modal-body').css({
                        "overflow-y": "auto",
                        "height": dynamicHeight + "px",
                        "max-height": "90vh"
                    });
                } else {
                    frappe.msgprint(__('No Purchase Orders found.'));
                }
            }
        });
    }
});

function calculate_grand_total(frm) {
    let total = 0;
    (frm.doc.items || []).forEach(row => {
        total += row.total || 0; 
    });

    frm.set_value('purchase_order_grand_total', total); 
    frm.refresh_field('purchase_order_grand_total');
    frm.save()
}

frappe.ui.form.on('Multi Purchase Order Item', {
    items_add: function (frm) {
        calculate_grand_total(frm);
    },
    items_remove: function (frm) {
        calculate_grand_total(frm);
    },
    purchase_order_grand_total: function (frm) {
        calculate_grand_total(frm);
    }
});
