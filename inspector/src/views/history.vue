<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">ปฏิทินตรวจสอบย้อนหลัง</h2>

    <!-- เลือก Category -->
    <div class="mb-4">
      <label>ประเภทแบบฟรอม:</label>
      <select v-model="selectedCategory" @change="fetchCalendar" class="border p-2 rounded">
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <!-- เลือกเดือนและปี -->
    <div class="mb-4 flex gap-4">
      <div>
        <label>เดือน:</label>
        <select v-model="selectedMonth" @change="fetchCalendar" class="border p-2 rounded">
          <option v-for="(m, index) in monthNames" :key="index" :value="index">{{ m }}</option>
        </select>
      </div>
      <div>
        <label>ปี:</label>
        <select v-model="selectedYear" @change="fetchCalendar" class="border p-2 rounded">
          <option v-for="y in yearsRange" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>
    </div>

    <!-- แสดงเดือนและปี -->
    <div class="mb-4 font-semibold">
      {{ monthNames[selectedMonth] }} {{ selectedYear }}
    </div>

    <!-- ปฏิทิน -->
    <div class="grid grid-cols-7 gap-2">
      <!-- ชื่อวัน -->
      <div v-for="day in weekdays" :key="day" class="font-bold text-center">{{ day }}</div>

      <!-- ช่องว่างก่อนวันแรกของเดือน -->
      <div v-for="blank in firstDayOfMonth" :key="'b'+blank"></div>

      <!-- วันในเดือน -->
      <div
        v-for="day in daysInMonth"
        :key="day.date"
        class="h-12 flex items-center justify-center border rounded cursor-pointer"
        :class="day.status ? 'bg-green-200' : 'bg-white'"
        @click="goToDataHistory(day.date)"
      >
        <span>{{ day.number }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

// Categories
const categories = [
  "แบบฟอร์มตรวจสอบเครื่องจักร (day)",
  "แบบฟอร์มตรวจสอบเครื่องจักร (month)"
];
const selectedCategory = ref(categories[0]);

// วันและเดือน
const weekdays = ["อาทิตย์", "จันทร์ ", "อังคาร ", "พุธ", "พฤหัสบดี ", "ศุกร์ ", "เสาร์ "];
const monthNames = [
  "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
  "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
];

const now = new Date();
const selectedMonth = ref(now.getMonth());
const selectedYear = ref(now.getFullYear());

// สร้างช่วงปี เช่น ปีนี้ถึงปีนี้ + 10
const yearsRange = Array.from({ length: 11 }, (_, i) => now.getFullYear() + i);

// ปฏิทิน
const calendarData = ref({});
const firstDayOfMonth = ref(0);
const daysInMonth = ref([]);

// ฟังก์ชันแปลง date เป็น dd-mm-yyyy
const formatDateDDMMYYYY = (date) => {
  const dd = String(date.getDate()).padStart(2, "0");
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const yyyy = date.getFullYear();
  return `${dd}-${mm}-${yyyy}`;
};

// สร้าง array วันในเดือน พร้อม status
const generateDaysInMonth = () => {
  const lastDay = new Date(selectedYear.value, selectedMonth.value + 1, 0).getDate();
  const days = [];
  for (let i = 1; i <= lastDay; i++) {
    const fullDate = new Date(selectedYear.value, selectedMonth.value, i);
    const dateStr = formatDateDDMMYYYY(fullDate); 
    days.push({
      number: i,
      date: dateStr,
      status: calendarData.value[dateStr] || null
    });
  }
  daysInMonth.value = days;
  firstDayOfMonth.value = new Date(selectedYear.value, selectedMonth.value, 1).getDay();
};

// ดึงข้อมูลจาก backend
const fetchCalendar = async () => {
  try {
    const res = await axios.get(
      "http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.formmm.formmm.get_calendar",
      {
        params: { 
          category: selectedCategory.value,
          month: selectedMonth.value + 1,
          year: selectedYear.value
        }
      }
    );

    if (res.data.message.status === "success") {
      calendarData.value = res.data.message.data;
      generateDaysInMonth();
    }
  } catch (err) {
    console.error(err);
  }
};

// ไปหน้า datahistory
const goToDataHistory = (date) => {
  router.push({
    name: "dataHistory",
    query: {
      category: selectedCategory.value,
      date: date
    }
  });
};

onMounted(() => {
  fetchCalendar();
});
</script>

<style scoped>
.grid div {
  transition: background-color 0.3s;
}
</style>
