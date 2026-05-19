# apps/vdeal_custom_app/vdeal_custom_app/api.py

import frappe
from frappe.utils.file_manager import save_file

@frappe.whitelist(allow_guest=True)
def create_service_request(**kwargs):

    doc = frappe.new_doc(
        "Service Request"
    )

    doc.request_type = kwargs.get(
        "request_type"
    )
    doc.existing_sr_id = kwargs.get(
        "existing_sr_id"
    )
    doc.customer_name = kwargs.get(
        "customer_name"
    )

    doc.address = kwargs.get(
        "location"
    )

    doc.contact_person = kwargs.get(
        "contact_person"
    )

    doc.email_id = kwargs.get(
        "email_id"
    )

    doc.mobile_number = kwargs.get(
        "mobile_number"
    )

    doc.nature_of_job = kwargs.get(
        "nature_of_job"
    )

    doc.service_required_for = kwargs.get(
        "service_required_for"
    )

    doc.payment_type = kwargs.get(
        "payment_type"
    )

    doc.estimated_cost = kwargs.get(
        "estimated_cost"
    )

    doc.po_number = kwargs.get(
        "po_number"
    )

    doc.po_date = kwargs.get(
        "po_date"
    )

    doc.expected_visit_date = kwargs.get(
        "expected_visit_date"
    )

    doc.priority_level = kwargs.get(
        "priority_level"
    )
    doc.priority_reason = kwargs.get("priority_reason")
    doc.scope_of_work = kwargs.get(
        "scope_of_work"
    )
    # Handle PO Copy Upload

    doc.insert(
        ignore_permissions=True
    )
    if "po_copy" in frappe.request.files:

        file = frappe.request.files["po_copy"]

        saved_file = save_file(
            file.filename,
            file.stream.read(),
            "Service Request",
            doc.name,
            is_private=0
        )

        doc.po_copy = saved_file.file_url
        doc.save(ignore_permissions=True)
    if doc.email_id:

        frappe.sendmail(

            recipients=[doc.email_id],

            subject=f"""
            Service Request Created:
            {doc.name}
            """,

            message=f"""

            Dear {doc.contact_person},

            Your Service Request has been submitted successfully.

            Service Request ID:
            {doc.name}

            Our team will contact you shortly.

            Regards,
            Service Team
            """

        )
    frappe.db.commit()

    return doc.name