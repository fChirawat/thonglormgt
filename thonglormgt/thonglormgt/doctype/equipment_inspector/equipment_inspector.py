# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import getdate, formatdate
from calendar import monthrange
from frappe.utils import get_first_day, get_last_day
from datetime import datetime, timedelta
import calendar
from frappe.utils import get_datetime
from datetime import datetime as dt  # เพิ่ม import
from frappe.utils import now_datetime
import json
from frappe.utils.data import getdate





class EquipmentInspector(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from thonglormgt.thonglormgt.doctype.equipment_inspector_indicator.equipment_inspector_indicator import EquipmentInspectorIndicator

		date: DF.Datetime | None
		equipment: DF.Link | None
		equipment_inspector_indicator: DF.Table[EquipmentInspectorIndicator]
		period: DF.Literal["\u0e27\u0e31\u0e19", "\u0e40\u0e14\u0e37\u0e2d\u0e19", "\u0e44\u0e15\u0e23\u0e21\u0e32\u0e2a", "\u0e1b\u0e35"]
	# end: auto-generated types

	pass


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ดึง Equipment Indicator ตรงกรอกแบบฟรอม
@frappe.whitelist(allow_guest=True)
def get_equipment_indicators(equipment=None, period=None):
    period_dict = {
        'วัน': 'period_day',
        'เดือน': 'period_month',
        'ไตรมาส': 'period_quarter',
        'ปี': 'period_year',
    }

    filters = {"equipment": equipment} if equipment else {}
    if period in period_dict:
        filters[period_dict[period]] = 1

    indicators = frappe.get_all(
        "Equipment Indicator",
        fields=["*"],
        filters=filters,
        order_by="idx asc"
    )

    # แปลง equipment code → title
    for d in indicators:
        if d.get("equipment"):
            title = frappe.get_value("Equipment", d["equipment"], "title")
            if title:
                d["equipment"] = title

    return {"message": indicators}

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# แปลงชื่อ equipment เป็น title
@frappe.whitelist(allow_guest=True)
def get_equipment_list():
    """
    Return list of all equipment with name and title
    """
    try:
        equipment = frappe.get_all(
            "Equipment",
            fields=["name", "title"],
            order_by="title asc"
        )
        return equipment
    except Exception as e:
        frappe.log_error(str(e), "get_equipment_list_error")
        return []
    

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# post equipment inspector จากฟรอม
@frappe.whitelist(allow_guest=True)
def submit_equipment_inspector(date=None, equipment=None, period=None, equipment_inspector_indicator=None):
    if isinstance(equipment_inspector_indicator, str):
        equipment_inspector_indicator = json.loads(equipment_inspector_indicator)

    # ตรวจสอบ Equipment
    if not frappe.db.exists("Equipment", equipment):
        frappe.throw(f"ไม่พบ Equipment: {equipment}")

    equipment_title = frappe.get_value("Equipment", equipment, "title") or equipment

    # สร้าง doc
    doc = frappe.get_doc({
        "doctype": "Equipment Inspector",
        "date": date or now_datetime(),
        "equipment": equipment,
        "period": period,
        "equipment_inspector_indicator": []
    })

    alert_list = []

    for ind in equipment_inspector_indicator:
        value = ind.get("value")
        start = ind.get("standard_value_start")
        end = ind.get("standard_value_end")
        ind_type = ind.get("type")
        grading = ind.get("standard_grading")

        # แปลง type
        try:
            if ind_type == "float":
                value = float(value) if value is not None else None
                start = float(start) if start is not None else None
                end = float(end) if end is not None else None
            elif ind_type == "int":
                value = int(value) if value is not None else None
                start = int(start) if start is not None else None
                end = int(end) if end is not None else None
            elif ind_type in ["string", "select"]:
                value = str(value) if value is not None else None
                start = str(start) if start is not None else None
                end = str(end) if end is not None else None
        except Exception as e:
            frappe.throw(f"แปลงค่า type ผิดพลาด: {ind.get('title')} -> {e}")

        # ตรวจสอบมาตรฐาน
        passed = True

        if ind_type == "select" and grading == "==":
            # แปลง start เป็น list
            options = []
            if start:
                if "\n" in start:
                    options = [x.strip() for x in start.split("\n")]
                elif "," in start:
                    options = [x.strip() for x in start.split(",")]
                else:
                    options = [start.strip()]
            passed = value in options
        else:
            # logic เดิม
            if grading == "<":
                passed = value < start
            elif grading == "<=":
                passed = value <= start
            elif grading == ">":
                passed = value > start
            elif grading == ">=":
                passed = value >= start
            elif grading == "==":
                passed = value == start
            elif grading.lower() in ["range", "range in"]:
                if start is not None and end is not None:
                    passed = start <= value <= end

        # append child table
        doc.append("equipment_inspector_indicator", {
            "title": ind.get("title"),
            "type": ind_type,
            "option": ind.get("option"),
            "value": value,
            "standard_grading": grading,
            "standard_value_start": start,
            "standard_value_end": end,
            "status": "✅ ผ่านมาตรฐาน" if passed else "❌ เกินมาตรฐาน"
        })

        if not passed:
            alert_list.append(f"{ind.get('title')}: {value} เกินมาตรฐาน")

    # บันทึก doc
    doc.insert()
    frappe.db.commit()

    email_sent = False

    # ส่ง email ถ้ามีค่าเกินมาตรฐาน
    if alert_list:
        message = f"{doc.name} อุปกรณ์ {equipment_title} ({period} {date}) มีค่าเกินมาตรฐาน:\n" + "\n".join(alert_list)
        try:
            frappe.sendmail(
                recipients=["kang2499k11@gmail.com"],  # ใส่อีเมลผู้รับ
                subject=f"แจ้งเตือน Equipment {equipment_title} เกินมาตรฐาน",
                message=message
            )
            email_sent = True
            doc.email_sent = 1
            doc.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(message=f"ส่งอีเมลล้มเหลว: {e}", title="Equipment Inspector Email Error")

    return {
        "message": "บันทึกสำเร็จ",
        "docname": doc.name,
        "alerts": alert_list,
        "email_sent": email_sent
    }


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# เช็ต equipment ที่กรอกได้ตาม period
@frappe.whitelist(allow_guest=True)
def get_equipment_by_period(period=None):
    from datetime import date, datetime
    import calendar

    if not period:
        return []

    today = date.today()

    # ดึง equipment ที่มีอยู่แล้วใน Equipment Inspector ตาม period
    if period == "วัน":
        # กรองแบบ range จากวันนี้ 00:00 ถึง 23:59
        first_day = datetime.combine(today, datetime.min.time())
        last_day = datetime.combine(today, datetime.max.time())
        filters = [["period", "=", "วัน"], ["date", ">=", first_day], ["date", "<=", last_day]]

    elif period == "เดือน":
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        filters = [["period", "=", "เดือน"], ["date", ">=", first_day], ["date", "<=", last_day]]
    elif period == "ไตรมาส":
        q = (today.month - 1) // 3 + 1
        first_month = 3 * (q - 1) + 1
        last_month = first_month + 2
        first_day = date(today.year, first_month, 1)
        last_day = date(today.year, last_month, calendar.monthrange(today.year, last_month)[1])
        filters = [["period", "=", "ไตรมาส"], ["date", ">=", first_day], ["date", "<=", last_day]]
    elif period == "ปี":
        first_day = date(today.year, 1, 1)
        last_day = date(today.year, 12, 31)
        filters = [["period", "=", "ปี"], ["date", ">=", first_day], ["date", "<=", last_day]]
    else:
        return []

    existing = frappe.get_all(
        "Equipment Inspector",
        fields=["equipment"],
        filters=filters,
        distinct=True
    )
    existing_equipment = [d["equipment"] for d in existing]

    # ดึง equipment จาก Equipment Indicator สำหรับ period ที่เลือก
    period_field = {
        "วัน": "period_day",
        "เดือน": "period_month",
        "ไตรมาส": "period_quarter",
        "ปี": "period_year"
    }.get(period)

    if not period_field:
        return []

    indicators = frappe.get_all(
        "Equipment Indicator",
        filters={period_field: 1},
        fields=["equipment"],
        distinct=True
    )
    equipment_codes = [d["equipment"] for d in indicators]

    # ตัด equipment ที่กรอกแล้ว
    remaining_equipment = list(set(equipment_codes) - set(existing_equipment))

    # แปลงเป็น code + title
    equipment_list = []
    for eq in remaining_equipment:
        title = frappe.get_value("Equipment", eq, "title")
        if title:
            equipment_list.append({"code": eq, "title": title})

    if not equipment_list:
        equipment_list = [{"code": "", "title": "ทุกข้อมูลกรอกหมดแล้ว"}]

    return equipment_list


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# เช็ต period ที่กรอกได้
@frappe.whitelist(allow_guest=True)
def check_period(period=None, year=None, month=None):
    """
    คืนค่า calendar_data = {date_or_month: [{"title": "...", "status": "✅/❌"}]}
    ต่อท้าย key ตามกฎ:
        - ✅ ทั้งหมด → ต่อท้าย ✅
        - ❌ ปน → ไม่ต่อท้าย
        - ❌ ทั้งหมด → ไม่ต่อท้าย
    """
    from calendar import monthrange
    from datetime import date as dt_date
    from frappe.utils.data import getdate

    try:
        today = getdate()
        year = int(year) if year else today.year
        month = int(month) if month else today.month

        calendar_data = {}

        # ดึง Equipment Indicator ทั้งหมด
        indicators = frappe.get_all(
            "Equipment Indicator",
            fields=["equipment", "title", "period_day", "period_month", "period_quarter", "period_year"]
        )

        # Mapping period field
        period_field_map = {
            "วัน": "period_day",
            "เดือน": "period_month",
            "ไตรมาส": "period_quarter",
            "ปี": "period_year"
        }
        period_field = period_field_map.get(period)
        if not period_field:
            return {"status": False, "message": f"period {period} ไม่ถูกต้อง", "data": {}}

        # กรอง indicators ตาม period
        indicators = [ind for ind in indicators if ind.get(period_field)]

        # ดึง Equipment Inspector
        filters = {"period": period}
        if period in ["วัน", "เดือน", "ไตรมาส"]:
            filters["date"] = ["between", [dt_date(year, 1, 1), dt_date(year, 12, 31)]]
        elif period == "ปี":
            filters["date"] = ["between", [dt_date(year, 1, 1), dt_date(year, 12, 31)]]

        inspector_records = frappe.get_all(
            "Equipment Inspector",
            fields=["name", "equipment", "date", "period"],
            filters=filters,
            order_by="date asc"
        )

        # Mapping: {key -> {equipment -> [titles]}}
        existing_map = {}
        for rec in inspector_records:
            doc = frappe.get_doc("Equipment Inspector", rec.name)
            rec_date = getdate(doc.date)
            if period == "วัน":
                key = str(rec_date)
            elif period == "เดือน":
                key = f"{rec_date.year}-{rec_date.month:02d}"
            elif period == "ไตรมาส":
                q = (rec_date.month - 1) // 3 + 1
                key = f"{rec_date.year}-{q}"
            elif period == "ปี":
                key = f"{rec_date.year}"
            existing_map.setdefault(key, {})
            existing_map[key].setdefault(rec.equipment, [])
            existing_map[key][rec.equipment] = [ind.title for ind in getattr(doc, "equipment_inspector_indicator", [])]

        # ฟังก์ชันสร้าง status และ key suffix
        def generate_data(key_base):
            data = []
            all_check = True
            any_check = False
            for ind in indicators:
                eq = ind.equipment
                title = ind.title
                existing_titles = existing_map.get(key_base, {}).get(eq, [])
                status = "✅" if title in existing_titles else "❌"
                if status == "❌":
                    all_check = False
                if status == "✅":
                    any_check = True
                data.append({"title": f"{eq} - {title}", "status": status})

            # กำหนด suffix: ถ้า ✅ ทั้งหมด → ต่อท้าย ✅
            suffix = "✅" if all_check and any_check else ""
            return key_base + suffix, data

        # สร้าง calendar_data ตาม period
        if period == "วัน":
            num_days = monthrange(year, month)[1]
            for day in range(1, num_days + 1):
                day_date = dt_date(year, month, day)
                key_base = str(day_date)
                key, data = generate_data(key_base)
                calendar_data[key] = data

        elif period == "เดือน":
            key_base = f"{year}-{month:02d}"
            key, data = generate_data(key_base)
            calendar_data[key] = data

        elif period == "ไตรมาส":
            quarter = (month - 1) // 3 + 1
            key_base = f"{year}-{quarter}"
            key, data = generate_data(key_base)
            calendar_data[key] = data

        elif period == "ปี":
            key_base = f"{year}"
            key, data = generate_data(key_base)
            calendar_data[key] = data

        return {
            "status": True,
            "period": period,
            "year": year,
            "month": month,
            "data": calendar_data
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "check_period Error")
        return {
            "status": False,
            "message": str(e),
            "data": {}
        }

        
        
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



# เช็ต equipment ที่กรอกได้ตาม period
@frappe.whitelist(allow_guest=True)
def get_equipment_inspector_details(period=None, year=None, month=None, day=None, equipment=None):

    try:
        if not period:
            frappe.throw("Period ต้องระบุ")

        # แปลงค่า input เป็น int
        year = int(year) if year else None
        month = int(month) if month else None
        day = int(day) if day else None

        filters = {"period": period}

        # กรองตาม period และวันที่
        if period == "วัน":
            if not (year and month and day):
                frappe.throw("สำหรับ period 'วัน' ต้องระบุ year, month, day")
            start_dt = datetime(year, month, day, 0, 0, 0)
            end_dt = datetime(year, month, day, 23, 59, 59)
            filters["date"] = ["between", [start_dt, end_dt]]

        elif period == "เดือน":
            if not (year and month):
                frappe.throw("สำหรับ period 'เดือน' ต้องระบุ year, month")
            start_dt = datetime(year, month, 1, 0, 0, 0)
            end_dt = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
            filters["date"] = ["between", [start_dt, end_dt]]

        elif period == "ไตรมาส":
            if not (year and month):
                frappe.throw("สำหรับ period 'ไตรมาส' ต้องระบุ year, month (เดือนเริ่มไตรมาส)")
            start_month = (month - 1) // 3 * 3 + 1
            end_month = start_month + 2
            start_dt = datetime(year, start_month, 1, 0, 0, 0)
            end_dt = datetime(year, end_month, monthrange(year, end_month)[1], 23, 59, 59)
            filters["date"] = ["between", [start_dt, end_dt]]

        elif period == "ปี":
            if not year:
                frappe.throw("สำหรับ period 'ปี' ต้องระบุ year")
            start_dt = datetime(year, 1, 1, 0, 0, 0)
            end_dt = datetime(year, 12, 31, 23, 59, 59)
            filters["date"] = ["between", [start_dt, end_dt]]

        # กรองตาม equipment ถ้ามี
        if equipment:
            filters["equipment"] = equipment

        # ดึง Equipment Inspector
        inspectors = frappe.get_all(
            "Equipment Inspector",
            filters=filters,
            fields=["name", "equipment", "date", "period"],
            order_by="date asc"
        )

        result = []
        used_equipment = set()

        for ins in inspectors:
            doc = frappe.get_doc("Equipment Inspector", ins.name)
            rec_date = getdate(doc.date) if doc.date else None
            if not rec_date:
                continue  # ข้าม record ที่ date เป็น None

            indicators = frappe.get_all(
                "Equipment Inspector Indicator",
                filters={"parent": ins.name, "parenttype": "Equipment Inspector"},
                fields=["title", "type", "value", "standard_grading", 
                        "standard_value_start", "standard_value_end"]
            )

            # ✅ ดึง title ของ equipment
            equipment_title = frappe.get_value("Equipment", ins.equipment, "title") or ins.equipment

            result.append({
                "equipment": equipment_title,   # ใช้ title แทน
                "code": ins.equipment,          # เก็บ code ไว้ด้วย
                "date": str(rec_date),
                "period": ins.period,
                "indicators": indicators
            })

            used_equipment.add(ins.equipment)

        # หา remaining_equipment
        all_equipment = [e.name for e in frappe.get_all("Equipment", fields=["name"])]
        remaining_equipment = [eq for eq in all_equipment if eq not in used_equipment]

        equipment_list = []
        for eq in remaining_equipment:
            title = frappe.get_value("Equipment", eq, "title")
            if title:
                equipment_list.append({"code": eq, "title": title})

        if not equipment_list:
            equipment_list = [{"code": "", "title": "ทุกข้อมูลกรอกหมดแล้ว"}]

        return {
            "status": True,
            "message": "success",
            "data": result,
            "remaining_equipment": equipment_list
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_equipment_inspector_details Error")
        return {"status": False, "message": str(e), "data": [], "remaining_equipment": []}
