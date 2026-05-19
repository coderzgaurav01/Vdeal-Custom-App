import frappe
from frappe.model.naming import make_autoname


def autoname_hd_ticket(self, method=None):
    naming_series = "VSL/.YYYY./SR.###"
    self.name = make_autoname(naming_series)

