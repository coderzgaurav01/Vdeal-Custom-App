// Copyright (c) 2026, gauravpathak911311@gmail.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Service Visit", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Service Visit', {

    refresh(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button('Create Challan', () => {

                frappe.new_doc('Service Challan', {

                    sr: frm.doc.sr,
                    visit: frm.doc.name,
                    service_engineer:
                            frm.doc.engineer
                });

            });

        }

    }

});