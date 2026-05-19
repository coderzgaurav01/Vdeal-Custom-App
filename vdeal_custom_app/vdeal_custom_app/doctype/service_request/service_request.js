// Copyright (c) 2026, gauravpathak911311@gmail.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Service Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Service Request', {

    refresh(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button('Create Service Visit', () => {

                frappe.new_doc('Service Visit', {

                    sr: frm.doc.name,
                    customer_name: frm.doc.customer_name,
                    engineer: frm.doc.assigned_engineer

                });

            });

        }

    }

});