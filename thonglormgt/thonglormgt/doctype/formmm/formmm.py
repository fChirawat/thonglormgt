# Copyright (c) 2025, film and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, add_days, formatdate
import json
from frappe.utils import get_datetime
from frappe.utils import get_traceback
from frappe.utils import now_datetime
from calendar import monthrange
from datetime import date, datetime, timedelta
import calendar
from frappe.utils import today, get_first_day, get_last_day





class Formmm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Data | None
		datetime: DF.Datetime | None
		details: DF.Data | None
		equipment: DF.Data | None
		inspection: DF.Data | None
		inspection_value: DF.Data | None
		name: DF.Int | None
		number_value: DF.Float
		username: DF.Data | None
	# end: auto-generated types

	pass


# post ของรายเดือน
@frappe.whitelist(allow_guest=True)
def save_inspections():
    import json
    from frappe.utils import now_datetime

    try:
        # อ่าน raw POST body
        raw = frappe.request.get_data().decode("utf-8")
        if not raw:
            return {"status": "error", "message": "ไม่มีข้อมูลที่จะบันทึก (raw empty)"}

        try:
            j = json.loads(raw)
        except Exception as e:
            return {"status": "error", "message": f"JSON decode error: {e}"}

        data = j.get("data")
        if not data or not isinstance(data, list):
            return {"status": "error", "message": "ไม่มีข้อมูลที่จะบันทึก (data empty)"}

        saved_count = 0
        errors = []

        for row in data:
            try:
                # แปลงค่า number_value เป็น float
                number_value = row.get("number_value")
                if number_value is not None:
                    try:
                        number_value = float(number_value)
                    except ValueError:
                        number_value = None  # ถ้าแปลงไม่ได้ ให้เป็น None

                doc = frappe.get_doc({
                    "doctype": "Formmm",
                    "category": row.get("category"),
                    "equipment": row.get("equipment"),
                    "inspection": row.get("inspection"),
                    "details": row.get("details"),
                    "inspection_value": row.get("inspection_value"),
                    "number_value": number_value,   # <-- เพิ่มตรงนี้
                    "datetime": row.get("datetime") or now_datetime(),
                    "username": row.get("username")
                })
                doc.insert(ignore_permissions=True)
                saved_count += 1
            except Exception as e:
                errors.append({"row": row, "error": str(e)})

        if errors:
            return {
                "status": "partial_success",
                "message": f"บันทึกสำเร็จ {saved_count} row แต่มี error {len(errors)} row",
                "errors": errors
            }

        return {"message": "บันทึกข้อมูลสำเร็จ"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    
    
    
    
    
        
#get ของปฏิทิน รายเดือน
@frappe.whitelist(allow_guest=True)
def get_calendar(category=None, year=None, month=None):
    """
    สร้างปฏิทินของเดือน/ปีที่ระบุ
    - category: ถ้าระบุ จะ filter ตาม category
    - year: ปีที่ต้องการ (default = ปีปัจจุบัน)
    - month: เดือนที่ต้องการ (default = เดือนปัจจุบัน)
    คืนค่า dict ของวัน: ✅ หรือ ""
    """
    try:


        today = getdate()

        # ถ้าไม่ได้ระบุปี/เดือน ใช้ปัจจุบัน
        year = int(year) if year else today.year
        month = int(month) if month else today.month

        # จำนวนวันในเดือนนั้น
        num_days = monthrange(year, month)[1]

        # สร้าง filter ตาม category
        filters = {}
        if category:
            filters["category"] = category

        # filter datetime ของเดือน/ปีที่ระบุ
        start_datetime = f"{year}-{month:02d}-01 00:00:00"
        end_datetime = f"{year}-{month:02d}-{num_days} 23:59:59"
        filters["datetime"] = ["between", [start_datetime, end_datetime]]

        # ดึงข้อมูลจาก DocType Formmm
        records = frappe.get_all(
            "Formmm",
            filters=filters,
            fields=["datetime", "category"]
        )

        # สร้าง dict วัน: สถานะ
        calendar_data = {}
        for day in range(1, num_days + 1):
            day_date = datetime(year, month, day).date()
            day_str = formatdate(day_date)
            checked = any(
                r.datetime and getdate(r.datetime) == day_date
                for r in records
            )
            calendar_data[day_str] = "✅" if checked else ""

        return {
            "status": "success",
            "category": category if category else "all",
            "year": year,
            "month": month,
            "data": calendar_data
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Formmm Calendar GET Error")
        return {
            "status": "error",
            "message": str(e)
        }
    
    
    


# get รายละเอียดของวัน
@frappe.whitelist(allow_guest=True)
def get_data_by_date(category=None, date=None):
    if not category or not date:
        return {"status": "error", "message": "กรุณาระบุ category และ date"}

    try:
        day, month, year = map(int, date.split('-'))
        from datetime import datetime
        start_dt = datetime(year, month, day, 0, 0, 0)
        end_dt = datetime(year, month, day, 23, 59, 59)
    except Exception as e:
        return {"status": "error", "message": f"รูปแบบ date ไม่ถูกต้อง: {e}"}

    try:
        records = frappe.get_all(
            "Formmm",
            filters={
                "category": category,
                "datetime": ["between", [start_dt, end_dt]]
            },
            fields=[
                "category",
                "equipment",
                "inspection",
                "datetime",
                "username",
                "inspection_value",
                "number_value",
                "details"
            ],
            order_by="datetime asc"
        )
        return {"status": "success", "data": records}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {e}"}
    
    
    
    
    


# หน้า home 
@frappe.whitelist(allow_guest=True)
def get_inspection_status(category, equipment=None):
    """
    ดึงข้อมูลสถานะการตรวจสอบ
    category: 'day', 'month', 'quarter', 'year' (หรือ full text)
    equipment: optional
    return: list ของ dict {'date': ...,'month': ...,'status':'checked/unchecked','message':...}
    """

    now = get_datetime()
    status_list = []

    # Mapping ระหว่างข้อความเต็มกับ key สั้น
    category_map = {
        "แบบฟอร์มตรวจสอบเครื่องจักร (day)": "day",
        "แบบฟอร์มตรวจสอบเครื่องจักร (month)": "month",
        "แบบฟอร์มตรวจสอบเครื่องจักร (quarter)": "quarter",
        "แบบฟอร์มตรวจสอบเครื่องจักร (year)": "year",
    }

    cat_key = category_map.get(category)
    if not cat_key:
        return []

    # กำหนดช่วงเวลาเริ่ม-สิ้นสุด
    if cat_key == "day":
        start = get_datetime(f"{today()} 00:00:00")
        end = get_datetime(f"{today()} 23:59:59")

    elif cat_key == "month":
        start_date = get_first_day(now)  # date object
        end_date = get_last_day(now)     # date object
        start = datetime.combine(start_date, datetime.min.time())
        end = datetime.combine(end_date, datetime.max.time())

    elif cat_key == "quarter":
        month = now.month
        q_start_month = (month-1)//3*3 + 1
        q_end_month = q_start_month + 2
        start = datetime(now.year, q_start_month, 1)
        last_day = get_last_day(datetime(now.year, q_end_month,1)).day
        end = datetime(now.year, q_end_month, last_day, 23,59,59)

    else:  # year
        start = datetime(now.year, 1, 1)
        end = datetime(now.year, 12, 31, 23,59,59)

    # Query ข้อมูลที่ตรวจสอบแล้ว
    filters = {"category": category, "datetime": ["between", [start, end]]}
    if equipment:
        filters["equipment"] = equipment

    inspections = frappe.get_all(
        "Formmm",
        filters=filters,
        fields=["datetime", "username"]
    )

    # สร้าง list ของวันที่ตรวจสอบแล้ว
    checked_dates = [i["datetime"].date() for i in inspections]

    # สร้าง status list ตามประเภท
    if cat_key == "day":
        status_list.append({
            "date": today(),
            "status": "checked" if checked_dates else "unchecked",
            "message": "คุณตรวจสอบไปแล้ว" if checked_dates else "ยังไม่ตรวจสอบ"
        })

    elif cat_key == "month":
        day_count = (end.date() - start.date()).days + 1
        for i in range(day_count):
            day = start.date() + timedelta(days=i)
            status_list.append({
                "date": day,
                "status": "checked" if day in checked_dates else "unchecked",
                "message": "คุณตรวจสอบไปแล้ว" if day in checked_dates else "ยังไม่ตรวจสอบ"
            })

    else:  # quarter / year
        for m in range(start.month, end.month + 1):
            month_checked = any(d.month == m for d in checked_dates)
            status_list.append({
                "month": m,
                "status": "checked" if month_checked else "unchecked",
                "message": "คุณตรวจสอบไปแล้ว" if month_checked else "ยังไม่ตรวจสอบ"
            })

    return status_list