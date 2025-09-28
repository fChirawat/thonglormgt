<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">บันทึกรายวัน</h2>

    <!-- Category -->
    <p class="mb-4">
      <span class="font-semibold"></span> {{ fixedCategory }}
    </p>

    <!-- Global datetime & username -->
    <div class="mb-4 flex gap-4">
      <div class="flex-1">
        <label class="font-semibold">เวลาในการตรวจ:</label>
        <input type="datetime-local" v-model="globalDatetime" class="border p-2 rounded w-full"/>
      </div>
      <div class="flex-1">
        <label class="font-semibold">ชื่อผู้ตรวจ:</label>
        <select v-model="globalUsername" class="border p-2 rounded w-full">
          <option value="" disabled>-- เลือก ชื่อผู้ตรวจ --</option>
          <option v-for="user in users" :key="user.name" :value="user.full_name">
            {{ user.full_name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <table class="w-full border-collapse border mb-4">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-2 py-1">อุปกรณ์</th>
          <th class="border px-2 py-1">สิ่งที่ต้องตรวจ</th>
          <th class="border px-2 py-1">ค่าที่ได้ผ่าน/ไม่ผ่าน</th>
          <th class="border px-2 py-1">Details</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(item, i) in inspectionData" :key="i">
          <tr v-for="(insp, j) in item.inspections" :key="j">
            <td class="border px-2 py-1">{{ item.equipment_name }}</td>
            <td class="border px-2 py-1">{{ insp.inspection }}</td>
            <td class="border px-2 py-1">
              <select v-model="insp.new.inspection_value" class="border p-1 w-full">
                <option disabled value="">-- เลือกค่า --</option>
                <option value="Yes">ผ่าน</option>
                <option value="No">ไม่ผ่าน</option>
              </select>
            </td>
            <td class="border px-2 py-1">
              <input type="text" v-model="insp.new.details" class="border p-1 w-full"/>
            </td>
          </tr>
        </template>
      </tbody>
    </table>

    <!-- ปุ่มบันทึกทั้งหมด -->
    <div class="text-right">
      <button 
        @click="submitAllInspections"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        บันทึกทั้งหมด
      </button>
    </div>

    <!-- Loading & Error -->
    <p v-if="loading" class="text-blue-500">กำลังโหลดข้อมูล...</p>
    <p v-if="error" class="text-red-500">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const fixedCategory = "แบบฟอร์มตรวจสอบเครื่องจักร (day)";
const globalDatetime = ref("");
const globalUsername = ref("");
const inspectionData = ref([]);
const users = ref([]);
const loading = ref(false);
const error = ref("");

// ดึงข้อมูลผู้ใช้จาก backend
const fetchUsers = async () => {
  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.username.username.get_all_users"
    );
    users.value = res.data.message || [];
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

// ดึงข้อมูล Inspection
const fetchInspectionData = async () => {
  loading.value = true;
  error.value = "";
  inspectionData.value = [];

  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.inspection.inspection.inspection_data",
      { params: { category: fixedCategory } }
    );

    if (res.data.message?.status === "success") {
      inspectionData.value = res.data.message.data.map(item => ({
        ...item,
        inspections: item.inspections.map(insp => ({
          ...insp,
          new: { details: "", inspection_value: "" }
        }))
      }));
    } else {
      error.value = typeof res.data.message === "string" ? res.data.message : JSON.stringify(res.data.message);
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

// Submit inspections
const submitAllInspections = async () => {
  if (!globalDatetime.value || !globalUsername.value) {
    alert("กรุณาเลือก เวลาในการตรวจ และ ชื่อผู้ตรวจ ก่อน");
    return;
  }

  // ✅ ตรวจสอบว่าทุก inspection ต้องมีค่า inspection_value และ number_value
  for (const item of inspectionData.value) {
    for (const insp of item.inspections) {
      if (!insp.new.inspection_value) {
        alert(`กรุณาเลือกค่าผ่าน/ไม่ผ่าน สำหรับอุปกรณ์ "${item.equipment_name}" หัวข้อ "${insp.inspection}"`);
        return;
      }
      if (insp.new.number_value === null || insp.new.number_value === "") {
        alert(`กรุณากรอกค่าที่ตรวจสอบได้ (number_value) สำหรับอุปกรณ์ "${item.equipment_name}" หัวข้อ "${insp.inspection}"`);
        return;
      }
    }
  }

  // ✅ ยืนยันก่อนบันทึก
  const confirmSave = confirm("คุณต้องการบันทึกข้อมูลทั้งหมดใช่หรือไม่?");
  if (!confirmSave) return;

  const dataToSend = inspectionData.value.flatMap(item =>
    item.inspections.map(insp => ({
      category: fixedCategory,
      equipment: item.equipment_name,
      inspection: insp.inspection,
      details: insp.new.details,
      inspection_value: insp.new.inspection_value,
      number_value: insp.new.number_value, // เพิ่ม number_value
      datetime: globalDatetime.value,
      username: globalUsername.value
    }))
  );

  if (!dataToSend.length) {
    alert("ไม่มีข้อมูลที่จะบันทึก");
    return;
  }

  try {
    const res = await axios.post(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.formmm.formmm.save_inspections",
      { data: dataToSend },
      { headers: { "Content-Type": "application/json" } }
    );

    if (res.data.status === "success") {
      alert("✅ บันทึกข้อมูลเรียบร้อยแล้ว");
      // เคลียร์ฟอร์ม
      inspectionData.value.forEach(item => {
        item.inspections.forEach(insp => {
          insp.new.details = "";
          insp.new.inspection_value = "";
          insp.new.number_value = null;
        });
      });
    } else if (res.data.status === "partial_success") {
      const msg = `${res.data.message}\nErrors:\n${JSON.stringify(res.data.errors, null, 2)}`;
      alert(msg);
    } else {
      alert(typeof res.data.message === "string" ? res.data.message : JSON.stringify(res.data.message));
    }
  } catch (err) {
    alert("Error: " + err.message);
  }
};



onMounted(() => {
  fetchUsers();
  fetchInspectionData();
});
</script>

<style>
body {
  font-family: "Prompt", sans-serif;
}
table th, table td {
  border: 1px solid #ccc;
}
</style>
