// Copyright (c) 2025, film and contributors
// For license information, please see license.txt
function capitalizeFirstLetter(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}



frappe.ui.form.on("Equipment Inspector", {
    refresh(frm) {

    },
    open_form(frm) {
        let indicators = frm.doc.equipment_inspector_indicator
        fields = indicators.map(d => {
            return {
                label: d.title,
                fieldname: d.name,
                fieldtype: capitalizeFirstLetter(d.type),
                options: d.option,
                default: d.value,
                
            }
        })
        console.log(fields)
        let d = new frappe.ui.Dialog({
            title: 'Enter details',
            fields: fields,
            size: 'small', // small, large, extra-large 
            primary_action_label: 'Submit',
            primary_action(values) {
                console.log(values);
                d.hide();
                frm.doc.equipment_inspector_indicator.forEach(d => {
                    frappe.model.set_value("Equipment Inspector Indicator", d.name, "value", values[d.name] || null);

                })
                frm.refresh_field("equipment_inspector_indicator")
            }
        });

        d.show();

    },
    load_indicator(frm) {

        let period_dict = {
            'วัน': 'period_day',
            'เดือน': 'period_month',
            'ไตรมาส': 'period_quarter',
            'ปี': 'period_year',
        }
        let equipment = frm.doc.equipment
        if (equipment == null) {
            frappe.msgprint("กรุณาเลือก อุปกรณ์")
            return
        }
        let period = frm.doc.period

        let filters = {
            equipment: equipment,
        }

        if (period in period_dict) {
            filters[period_dict[period]] = 1
        }
        frappe.db.get_list("Equipment Indicator", {
            fields: ["*"],
            filters: filters,
        }).then(r => {
            console.log(r)
            frm.refresh_field("equipment_inspector_indicator")
            frm.clear_table("equipment_inspector_indicator")
            frm.refresh_field("equipment_inspector_indicator")

            frm.doc.equipment_inspector_indicator.splice(0, frm.doc.equipment_inspector_indicator.length)
            r.forEach(d => {
                var row = frm.add_child('equipment_inspector_indicator');
                frappe.model.set_value(row.doctype, row.name, "equipment_indicator", d.name);
                frappe.model.set_value(row.doctype, row.name, "title", d.title);
                frappe.model.set_value(row.doctype, row.name, "description", d.description);
                frappe.model.set_value(row.doctype, row.name, "type", d.type);
                frappe.model.set_value(row.doctype, row.name, "option", d.option);
                frappe.model.set_value(row.doctype, row.name, "value", d.value);
    


            })
            frm.refresh_field("equipment_inspector_indicator")

        })

    },
});
