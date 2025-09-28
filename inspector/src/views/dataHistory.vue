<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">
      {{ category }}
    </h2>

    <div v-if="dataHistory.length === 0" class="text-gray-500">ไม่มีข้อมูลที่บันทึก</div>

    <div v-else>
      <!-- แสดง username + datetime ข้างบน -->
      <div class="mb-2 font-semibold">
        ชื่อคนตรวจ: {{ dataHistory[0].username }} 
        <br>
        เวลาในการตรวจ: {{ dataHistory[0].datetime }}
      </div>

      <table class="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-gray-200">
            <th class="border px-2 py-1">อุปกรณ์</th>
            <th class="border px-2 py-1">สิ่งที่ต้องตรวจ</th>
            <th class="border px-2 py-1">ค่าที่ตรวจสอบได้</th>
            <th class="border px-2 py-1">รายลเอียด</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in processedData" :key="index">
            <!-- แสดง Equipment แค่ครั้งแรกและใช้ rowspan -->
            <td
              v-if="item.showEquipment"
              :rowspan="item.rowspan"
              class="border px-2 py-1 text-center align-middle"
            >
              {{ item.equipment }}
            </td>

            <td class="border px-2 py-1">{{ item.inspection }}</td>

            <!-- เปลี่ยนจาก inspection_value เป็น number_value ตาม category -->
            <td class="border px-2 py-1">
              {{ category === "แบบฟอร์มตรวจสอบเครื่องจักร (month)" ? item.number_value : item.inspection_value }}
            </td>

            <td class="border px-2 py-1">{{ item.details }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const category = route.query.category;
const date = route.query.date;

const dataHistory = ref([]);

// ดึงข้อมูลจาก backend
onMounted(async () => {
  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.formmm.formmm.get_data_by_date",
      { params: { category, date } }
    );

    if (res.data.message.status === "success") {
      dataHistory.value = res.data.message.data;
    }
  } catch (err) {
    console.error(err);
  }
});

// process data เพื่อ merge Equipment
const processedData = computed(() => {
  const result = [];
  const equipmentMap = {};

  dataHistory.value.forEach((item) => {
    if (!equipmentMap[item.equipment]) {
      equipmentMap[item.equipment] = { count: 1 };
    } else {
      equipmentMap[item.equipment].count += 1;
    }
  });

  const equipmentShown = {};
  dataHistory.value.forEach((item) => {
    let showEquipment = false;
    let rowspan = 1;

    if (!equipmentShown[item.equipment]) {
      showEquipment = true;
      rowspan = equipmentMap[item.equipment].count;
      equipmentShown[item.equipment] = true;
    }

    result.push({
      ...item,
      showEquipment,
      rowspan
    });
  });

  return result;
});
</script>

<style scoped>
table th, table td {
  text-align: left;
}
</style>
