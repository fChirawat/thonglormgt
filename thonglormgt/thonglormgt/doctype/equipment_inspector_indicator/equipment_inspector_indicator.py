# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EquipmentInspectorIndicator(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.LongText | None
		equipment_indicator: DF.Link | None
		option: DF.LongText | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		standard_grading: DF.Data | None
		standard_value_end: DF.Data | None
		standard_value_start: DF.Data | None
		title: DF.Data | None
		type: DF.Literal["int", "float", "data", "select"]
		value: DF.Data | None
	# end: auto-generated types

	pass
