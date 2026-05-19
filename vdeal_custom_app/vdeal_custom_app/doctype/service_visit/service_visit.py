# Copyright (c) 2026, gauravpathak911311@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from vdeal_custom_app.utils.email import (
    send_fsm_email
)

class ServiceVisit(Document):

    def autoname(self):
        visit_count = frappe.db.count(
            "Service Visit",
            {"sr": self.sr}
        ) + 1

        self.visit_number = visit_count
        self.name = f"{self.sr}/V{str(visit_count).zfill(3)}"

    def after_insert(self):

        total_visits = frappe.db.count(
            "Service Visit",
            {"sr": self.sr}
        )

        frappe.db.set_value(
            "Service Request",
            self.sr,
            {
                "total_visits": total_visits,
                "current_visit_number": self.visit_number,
                "status":"In Progress"
            }
        )

    def validate(self):

        # Allow only one reschedule by Service Engineer
        if self.is_rescheduled:

            old_doc = self.get_doc_before_save()

            if old_doc and old_doc.visit_date != self.visit_date:

                self.reschedule_count = (
                    self.reschedule_count or 0
                ) + 1

                self.rescheduled_by = frappe.session.user

                if (
                    self.reschedule_count > 1
                    and not frappe.has_role("Service Manager")
                ):
                    frappe.throw(
                        "Only Service Manager can reschedule more than once."
                    )

        if (
            self.workflow_state == "Waiting MOM Approval"
            and not self.mom_upload
        ):
            frappe.throw(
                "Please upload MOM before approval."
            )
        if self.is_rescheduled:

            sr = frappe.get_doc(
                "Service Request",
                self.sr
            )

            recipients = []

            if sr.owner:
                recipients.append(sr.owner)

            manager_emails = frappe.get_all(
                "Has Role",
                filters={
                    "role": "Service Manager"
                },
                fields=["parent"]
            )

            for manager in manager_emails:

                email = frappe.db.get_value(
                    "User",
                    manager.parent,
                    "email"
                )

                if email:
                    recipients.append(email)

            subject = f"""
            Service Visit Rescheduled:
            {self.name}
            """

            message = f"""
            Service Visit has been rescheduled.

            Visit:
            {self.name}

            SR:
            {self.sr}

            New Visit Date:
            {self.visit_date}

            Reason:
            {self.reschedule_reason}

            Regards,
            FSM System
            """

            send_fsm_email(
                recipients=list(set(recipients)),
                subject=subject,
                message=message
            )

    def on_update(self):

        if (
            self.workflow_state == "Approved"
            and self.next_visit_required
        ):

            existing_visit = frappe.db.exists(
                "Service Visit",
                {
                    "sr": self.sr,
                    "visit_date": self.next_visit_date
                }
            )

            if not existing_visit:

                next_visit = frappe.new_doc(
                    "Service Visit"
                )

                next_visit.sr = self.sr
                next_visit.visit_date = self.next_visit_date
                next_visit.assigned_engineer = (
                    self.assigned_engineer
                )

                next_visit.insert(
                    ignore_permissions=True
                )

                frappe.msgprint(
                    f"Next Visit Created: {next_visit.name}"
                )
                frappe.db.set_value(
                "Service Request",
                self.sr,
                "status",
                "In Progress"
            )

            elif self.workflow_state == "Completed":

                frappe.db.set_value(
                    "Service Request",
                    self.sr,
                    "status",
                    "Completed"
                )
            
            if self.workflow_state == "Approved":

                sr = frappe.get_doc(
                    "Service Request",
                    self.sr
                )

                recipients = []

                if sr.email_id:
                    recipients.append(sr.email_id)

                if self.assigned_engineer:

                    engineer_email = frappe.db.get_value(
                        "User",
                        self.assigned_engineer,
                        "email"
                    )

                    if engineer_email:
                        recipients.append(engineer_email)

                subject = f"""
                Service Visit Approved:
                {self.name}
                """

                message = f"""
                Service Visit has been approved.

                Visit:
                {self.name}

                SR:
                {self.sr}

                Regards,
                Service Team
                """

                send_fsm_email(
                    recipients=list(set(recipients)),
                    subject=subject,
                    message=message
                )