# Copyright (c) 2026, gauravpathak911311@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceChallan(Document):

    def autoname(self):
        visit_count = frappe.db.count(
            "Service Visit",
            {"sr": self.sr}
        ) + 1

        self.name = f"{self.sr}/CH{str(visit_count).zfill(3)}"

    def before_insert(self):

        if self.service_visit:

            visit = frappe.get_doc(
                "Service Visit",
                self.service_visit
            )

            self.service_engineer = visit.assigned_engineer
