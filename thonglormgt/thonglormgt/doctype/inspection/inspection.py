# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Inspection(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Data | None
		equipment: DF.Data | None
		inspection: DF.Data | None
		name: DF.Int | None
		value_end: DF.Data | None
		value_start: DF.Data | None
	# end: auto-generated types

	pass




@frappe.whitelist(allow_guest=True)
def inspection_data(category):
    try:
        # ดึงข้อมูล Equipment ที่อยู่ใน Category ที่เลือก
        equipments = frappe.get_all(
            "Equipment",
            filters={"category": category},
            fields=["name", "category", "equipment_name"]
        )

        # ดึง inspection ของแต่ละ equipment
        data = []
        for eq in equipments:
            inspections = frappe.get_all(
                "Inspection",
                filters={"equipment": eq.name},  # ใช้ link field
                fields=["inspection", "value_start", "value_end"]
            )

            data.append({
                "category": eq.category,
                "equipment_name": eq.equipment_name,
                "inspections": inspections
            })

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Inspection GET Error")
        return {
            "status": "error",
            "message": str(e)
        }


