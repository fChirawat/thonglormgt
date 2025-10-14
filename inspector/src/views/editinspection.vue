<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Equipment Inspector</h2>

    <!-- Filters -->
    <div class="flex gap-4 mb-4">
      <!-- เลือกช่วงเวลา -->
      <select v-model="selectedPeriod" @change="loadEquipmentByPeriod" class="border p-2 rounded">
        <option value="">-- เลือกช่วงเวลา --</option>
        <option value="วัน">วัน</option>
        <option value="เดือน">เดือน</option>
        <option value="ไตรมาส">ไตรมาส</option>
        <option value="ปี">ปี</option>
      </select>

      <!-- เลือกประเภทอุปกรณ์ -->
      <select v-model="selectedEquipmentType" class="border p-2 rounded">
        <option value="">-- เลือกอุปกรณ์ --</option>
        <option v-for="type in uniqueEquipmentTypes" :key="type" :value="type">{{ type }}</option>
      </select>

      <!-- เลือกว่าจะโหลดทั้งหมดหรือเฉพาะตัว -->
      <select v-if="showEquipmentSelect" v-model="selectedEquipmentOption" class="border p-2 rounded">
        <option value="all">แสดงทั้งหมด</option>
        <option v-for="eq in matchedEquipments" :key="eq.code" :value="eq.code">{{ eq.title }}</option>
      </select>

      <button @click="loadIndicators" class="bg-blue-500 text-white px-4 py-2 rounded">Load</button>
    </div>

    <!-- เลือกวันที่ -->
    <input type="datetime-local" v-model="selectedDate" class="border p-2 rounded mb-4" />

    <!-- ตาราง indicators -->
    <div v-if="Object.keys(groupedIndicators).length">
      <div v-for="(indicatorList, equipmentName) in groupedIndicators" :key="equipmentName" class="mb-6 border border-gray-300 rounded-lg p-4">
        <h3 class="font-bold text-lg mb-1">{{ equipmentName }}</h3>
        <p class="text-sm text-gray-500 mb-2">{{ equipmentDescription[equipmentName] }}</p>
        <table class="min-w-full border border-gray-200">
          <thead>
            <tr class="bg-gray-100">
              <th class="border px-4 py-2">Code</th>
              <th class="border px-4 py-2">Title</th>
              <th class="border px-4 py-2">Type</th>
              <th class="border px-4 py-2">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="indicator in indicatorList" :key="indicator.name" :class="{'bg-red-100': indicator.status?.includes('❌')}">
              <td class="border px-4 py-2">{{ indicator.equipmentCode }}</td>
              <td class="border px-4 py-2">{{ indicator.title }}</td>
              <td class="border px-4 py-2">{{ indicator.type }}</td>
              <td class="border px-4 py-2">
                <input v-if="indicator.type==='float'||indicator.type==='int'" type="number" v-model.number="indicator.value" class="border px-2 py-1 w-full" />
                <select v-else-if="indicator.type==='select'" v-model="indicator.value" class="border px-2 py-1 w-full">
                  <option value="">-- เลือก --</option>
                  <option v-for="opt in getOptions(indicator)" :key="opt" :value="opt">{{ opt }}</option>
                </select>
                <span v-else>{{ indicator.value }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <button @click="saveIndicators" class="bg-green-500 text-white px-4 py-2 rounded mt-4" :disabled="indicators.length===0">
      Save
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import axios from "axios";

// ------------------ State ------------------
const selectedPeriod = ref("");
const selectedEquipmentType = ref("");
const selectedEquipmentOption = ref("all");
const selectedDate = ref(new Date().toISOString().slice(0,16));

const equipmentList = ref([]);
const matchedEquipments = ref([]);
const indicators = ref([]);
const equipmentDescription = ref({}); // เก็บ description ของแต่ละอุปกรณ์

// เวลาไทย +7
const tzOffset = 7*60;
selectedDate.value = new Date(new Date().getTime()+tzOffset*60*1000).toISOString().slice(0,16);

// ------------------ Computed ------------------
// ประเภทอุปกรณ์ไม่ซ้ำ
const uniqueEquipmentTypes = computed(() => {
  const types = equipmentList.value.map(eq => eq.title.replace(/\s*\d+$/, "").trim());
  return [...new Set(types)];
});

// แสดง select เลือกตัวหรือทั้งหมด ก็ต่อเมื่อมีหลายตัว
const showEquipmentSelect = computed(() => matchedEquipments.value.length > 1);

// แยก indicators ตามชื่ออุปกรณ์
const groupedIndicators = computed(() => {
  const groups = {};
  indicators.value.forEach(ind => {
    if (!groups[ind.equipmentName]) groups[ind.equipmentName] = [];
    groups[ind.equipmentName].push(ind);
  });
  return groups;
});

// ------------------ Watch ------------------
watch(selectedEquipmentType, () => {
  if (!selectedEquipmentType.value) {
    matchedEquipments.value = [];
    selectedEquipmentOption.value = "all";
    return;
  }
  matchedEquipments.value = equipmentList.value.filter(eq =>
    eq.title.replace(/\s*\d+$/, "").trim() === selectedEquipmentType.value
  );
  selectedEquipmentOption.value = "all";
});

// ------------------ Functions ------------------

// โหลดรายการอุปกรณ์ตามช่วงเวลา
const loadEquipmentByPeriod = async () => {
  if (!selectedPeriod.value) { equipmentList.value=[]; return; }
  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.get_equipment_by_period",
      { params: { period: selectedPeriod.value } }
    );
    equipmentList.value = res.data.message || [];
  } catch(err) {
    console.error(err); alert("โหลดอุปกรณ์ไม่สำเร็จ");
  }
};

// โหลด indicators
const loadIndicators = async () => {
  if (!selectedEquipmentType.value) { alert("กรุณาเลือกอุปกรณ์"); return; }
  let equipmentsToLoad = [];
  if (selectedEquipmentOption.value === "all") equipmentsToLoad = matchedEquipments.value;
  else equipmentsToLoad = matchedEquipments.value.filter(eq => eq.code === selectedEquipmentOption.value);

  const allIndicators = [];
  const descriptions = {};
  for (const eq of equipmentsToLoad) {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.get_equipment_indicators",
      { params: { equipment: eq.code, period: selectedPeriod.value } }
    );
    const indicatorsData = res.data.message?.message || [];
    indicatorsData.forEach(ind => {
      if (!("value" in ind) || ind.value===null) ind.value="";
      ind.equipmentCode = eq.code;
      ind.equipmentName = eq.title;
    });
    allIndicators.push(...indicatorsData);

    // เก็บ description
    descriptions[eq.title] = eq.description || eq.equipment_description || "";
  }
  indicators.value = allIndicators.sort((a,b)=>parseInt(a.code)-parseInt(b.code));
  equipmentDescription.value = descriptions;
};

// ดึง options สำหรับ select
const getOptions = (indicator) => {
  if (!indicator.option) return [];
  if (indicator.option.includes("\n")) return indicator.option.split("\n").map(o=>o.trim());
  if (indicator.option.includes(",")) return indicator.option.split(",").map(o=>o.trim());
  return [indicator.option];
};

// บันทึก indicators เฉพาะที่กรอกค่า
const saveIndicators = async () => {
  if (!selectedDate.value || indicators.value.length === 0) {
    alert("กรุณาเลือกวันที่และโหลดอุปกรณ์");
    return;
  }

  try {
    const groupedByEquipment = {};
    indicators.value.forEach(ind => {
      const eq = ind.equipmentCode || ind.equipmentName;
      if (!groupedByEquipment[eq]) groupedByEquipment[eq] = [];
      groupedByEquipment[eq].push(ind);
    });

    for (const eq of Object.keys(groupedByEquipment)) {
      // เฉพาะ indicator ที่กรอกค่า
      const indicatorsToSend = groupedByEquipment[eq].filter(ind => ind.value !== "" && ind.value != null).map(ind => {
        let value = ind.value;
        if (ind.type === "float" || ind.type === "int") value = parseFloat(value);
        return { ...ind, value };
      });

      if (indicatorsToSend.length === 0) continue;

      const payload = {
        date: selectedDate.value,
        period: selectedPeriod.value,
        equipment: eq,
        equipment_inspector_indicator: indicatorsToSend,
      };

      await axios.post(
        "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.submit_equipment_inspector",
        payload
      );
    }

    alert("บันทึกสำเร็จ ✅");
    indicators.value = [];
    selectedEquipmentType.value = "";
    selectedEquipmentOption.value = "all";
    selectedPeriod.value = "";
    await loadEquipmentByPeriod();

  } catch(err) {
    console.error(err);
    alert("บันทึกไม่สำเร็จ");
  }
};
</script>

<style scoped>
.bg-red-100 { background-color: #fee2e2 !important; }
</style>
