# Copyright (c) 2026, gauravpathak911311@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from vdeal_custom_app.utils.email import (
    send_fsm_email
)
class ServiceRequest(Document):
	def autoname(self):
		if self.request_type == "Existing SR" and self.existing_sr_id:
			count= frappe.db.count("Service Request",{"existing_sr_id":self.existing_sr_id})+1
			self.name = f"{self.existing_sr_id}/R{str(count).zfill(2)}"
		else:
			self.name = make_autoname("VSL/.YYYY./SR.###")
	
	def validate(self):
		if self.request_type == "Existing SR" and not self.existing_sr_id :
			frappe.throw("Please Enter Existing SR ID")
		old_doc = self.get_doc_before_save()
		if old_doc:
			old_date = old_doc.expected_visit_date
			new_date = self.expected_visit_date
			if old_date != new_date and self.is_rescheduled == 1:
				self.reschedule_count = ((self.reschedule_count or 0)+1)
				self.last_rescheduled_by = frappe.session.user
				if not self.reschedule_reason:
					frappe.throw("Please Enter Reschedule Reason")
				if self.reschedule_count == 1:
					frappe.msgprint("First reschedule Allowed")
				elif "Service Manager" not in frappe.get_roles():
					frappe.throw("Request Service Manager for Reschedule . Only Service Manager can Reschedule More than Once")




	def before_insert(self):
		self.sr_date = frappe.utils.today()
		if self.expected_visit_date:
			self.original_visit_date = self.expected_visit_date
	def on_update(self):

		old_doc = self.get_doc_before_save()

		if (
			old_doc
			and old_doc.assigned_engineer
				!= self.assigned_engineer
			and self.assigned_engineer
		):

			engineer_email = frappe.db.get_value(
				"User",
				self.assigned_engineer,
				"email"
			)

			subject = f"""
			New Service Request Assigned:
			{self.name}
			"""

			message = f"""
			Dear Engineer,

			A new Service Request has been assigned.

			SR ID: {self.name}

			Customer:
			{self.customer_name}

			Priority:
			{self.priority_level}

			Expected Visit Date:
			{self.expected_visit_date}

			Regards,
			Service Team
			"""

			send_fsm_email(
				recipients=[engineer_email],
				subject=subject,
				message=message
			)