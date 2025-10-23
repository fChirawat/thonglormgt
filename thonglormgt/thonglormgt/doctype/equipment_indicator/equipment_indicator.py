# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EquipmentIndicator(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		code: DF.Data | None
		description: DF.LongText | None
		equipment: DF.Link | None
		option: DF.LongText | None
		period_day: DF.Check
		period_month: DF.Check
		period_quarter: DF.Check
		period_year: DF.Check
		standard_grading: DF.Literal["<", "<=", ">=", ">=", "==", "Range In"]
		standard_value_end: DF.Data | None
		standard_value_start: DF.Data | None
		title: DF.Data | None
		type: DF.Literal["int", "float", "data", "select"]
	# end: auto-generated types

	pass
