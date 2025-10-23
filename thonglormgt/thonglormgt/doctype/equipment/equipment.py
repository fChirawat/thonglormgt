# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class Equipment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		code: DF.Data | None
		description: DF.LongText | None
		title: DF.Data | None
	# end: auto-generated types

	pass


