<template>
  <div class="p-6 max-w-4xl mx-auto">
    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <select v-model="selectedPeriod" @change="loadEquipmentByPeriod" class="border p-2 rounded">
        <option value="">-- เลือกช่วงเวลา --</option>
        <option value="วัน">วัน</option>
        <option value="เดือน">เดือน</option>
        <option value="ไตรมาส">ไตรมาส</option>
        <option value="ปี">ปี</option>
      </select>

      <select v-model="selectedEquipment" class="border p-2 rounded">
        <option value="">-- เลือกอุปกรณ์ --</option>
        <option v-for="eq in equipmentList" :key="eq.code" :value="eq.code" :disabled="eq.code === ''">
          {{ eq.title }}
        </option>
      </select>

      <button @click="loadIndicators" class="bg-blue-500 text-white px-4 py-2 rounded">
        Load
      </button>
    </div>

    <input type="datetime-local" v-model="selectedDate" class="border p-2 rounded mb-4" />

    <table class="min-w-full border border-gray-200" v-if="indicators.length">
      <thead>
        <tr class="bg-gray-100">
          <th class="border px-4 py-2">Code</th>
          <th class="border px-4 py-2">Title</th>
          <th class="border px-4 py-2">Type</th>
          <th class="border px-4 py-2">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="indicator in indicators" :key="indicator.name" :class="{'bg-red-100': indicator.status?.includes('❌')}">
          <td class="border px-4 py-2">{{ indicator.code }}</td>
          <td class="border px-4 py-2">{{ indicator.title }}</td>
          <td class="border px-4 py-2">{{ indicator.type }}</td>
          <td class="border px-4 py-2">
            <input
              v-if="indicator.type === 'float' || indicator.type === 'int'"
              type="number"
              v-model.number="indicator.value"
              class="border px-2 py-1 w-full"
            />
            <select
              v-else-if="indicator.type === 'select'"
              v-model="indicator.value"
              class="border px-2 py-1 w-full"
            >
              <option value="">-- เลือก --</option>
              <option v-for="opt in getOptions(indicator)" :key="opt" :value="opt">
                {{ opt }}
              </option>
            </select>
            <span v-else>{{ indicator.value }}</span>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="equipmentList.length === 1 && equipmentList[0].code === ''" class="text-red-500 font-bold">
      ทุกข้อมูลกรอกหมดแล้ว
    </p>

    <button @click="saveIndicators" class="bg-green-500 text-white px-4 py-2 rounded mt-4" :disabled="equipmentList.length === 1 && equipmentList[0].code === ''">
      Save
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const equipmentList = ref([]);
const selectedEquipment = ref("");
const selectedPeriod = ref("");
const indicators = ref([]);

const now = new Date();
const tzOffset = 7 * 60; // ไทย +7 ชั่วโมง
const localTime = new Date(now.getTime() + tzOffset * 60 * 1000);
const selectedDate = ref(localTime.toISOString().slice(0, 16));

// โหลดรายการอุปกรณ์ตามช่วงเวลา พร้อมเช็คว่า equipment มีข้อมูลแล้วหรือไม่
const loadEquipmentByPeriod = async () => {
  if (!selectedPeriod.value) {
    equipmentList.value = [];
    selectedEquipment.value = "";
    return;
  }

  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.get_equipment_by_period",
      { params: { period: selectedPeriod.value } }
    );
    equipmentList.value = res.data.message || [];
    selectedEquipment.value = "";

    if (equipmentList.value.length === 1 && equipmentList.value[0].code === "") {
      alert("ทุกข้อมูลกรอกหมดแล้ว");
    }
  } catch (err) {
    console.error(err);
    alert("โหลดอุปกรณ์ไม่สำเร็จ");
  }
};




// โหลด indicators ของอุปกรณ์
const loadIndicators = async () => {
  if (!selectedEquipment.value || !selectedPeriod.value) {
    alert("กรุณาเลือกอุปกรณ์และช่วงเวลา");
    return;
  }
  if (selectedEquipment.value === "") {
    alert("ทุกข้อมูลกรอกหมดแล้ว ไม่สามารถกรอกซ้ำได้");
    return;
  }
  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.get_equipment_indicators",
      { params: { equipment: selectedEquipment.value, period: selectedPeriod.value } }
    );
    indicators.value = res.data.message?.message || [];
    indicators.value.forEach((ind) => {
      if (!("value" in ind) || ind.value === null) ind.value = "";
    });
    indicators.value.sort((a, b) => parseInt(a.code) - parseInt(b.code));
  } catch (err) {
    console.error(err);
    alert("โหลด indicators ไม่สำเร็จ");
  }
};

// ดึง options สำหรับ select
const getOptions = (indicator) => {
  if (!indicator.option) return [];
  if (indicator.option.includes("\n")) return indicator.option.split("\n").map((o) => o.trim());
  if (indicator.option.includes(",")) return indicator.option.split(",").map((o) => o.trim());
  return [indicator.option];
};

// บันทึกค่า indicators
const saveIndicators = async () => {
  if (!selectedEquipment.value || !selectedPeriod.value || !selectedDate.value) {
    alert("กรุณากรอกข้อมูลให้ครบ");
    return;
  }

  const emptyValue = indicators.value.find((ind) => ind.value === "" || ind.value === null);
  if (emptyValue) {
    alert(`กรุณากรอกค่า Value สำหรับ "${emptyValue.title}"`);
    return;
  }

  try {
    const payload = {
      date: selectedDate.value,
      equipment: selectedEquipment.value,
      period: selectedPeriod.value,
      equipment_inspector_indicator: indicators.value.map((ind) => {
        let value = ind.value;
        let start = ind.standard_value_start;
        let end = ind.standard_value_end;
        if (ind.type === "float" || ind.type === "int") {
          value = value !== "" && value != null ? parseFloat(value) : null;
          start = start !== "" && start != null ? parseFloat(start) : null;
          end = end !== "" && end != null ? parseFloat(end) : null;
        }
        return {
          title: ind.title,
          type: ind.type,
          option: ind.option,
          value,
          standard_grading: ind.standard_grading,
          standard_value_start: start,
          standard_value_end: end,
        };
      }),
    };

    const res = await axios.post(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.submit_equipment_inspector",
      payload
    );

    const alerts = res.data.message?.alerts || [];
    if (alerts.length) {
      alert("⚠️ มีค่าเกินมาตรฐาน:\n" + alerts.join("\n"));
    } else {
      alert("บันทึกสำเร็จ ✅");
    }

    // ล้างค่า
    indicators.value = [];
    selectedEquipment.value = "";
    selectedPeriod.value = "";
    selectedDate.value = new Date(new Date().getTime() + tzOffset * 60 * 1000).toISOString().slice(0, 16);
    await loadEquipmentByPeriod();
  } catch (err) {
    console.error(err);
    alert("บันทึกไม่สำเร็จ");
  }
};
</script>

<style scoped>
.bg-red-100 {
  background-color: #fee2e2 !important;
}
</style>
