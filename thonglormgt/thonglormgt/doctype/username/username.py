# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class username(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		full_name: DF.Data | None
		name: DF.Int | None
	# end: auto-generated types

	pass


@frappe.whitelist(allow_guest=True)
def get_all_users():
    """
    คืนค่า list ของผู้ใช้ทั้งหมดในรูปแบบ [{name, full_name}]
    """
    try:
        users = frappe.get_all("username", fields=["name", "full_name"])
        return users
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_all_users Error")
        return {"status": "error", "message": str(e)}