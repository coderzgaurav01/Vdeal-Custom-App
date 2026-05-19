import frappe


def send_fsm_email(
    recipients,
    subject,
    message
):

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message,
        now=True
    )