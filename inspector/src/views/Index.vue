<template>
<<<<<<< HEAD
  <div class="min-h-screen bg-white flex flex-col items-center p-6 relative">
    
    <div class="fixed top-6 right-6">
      <button
        class="w-14 h-14 flex items-center justify-center rounded-full shadow-lg bg-red-500 hover:bg-red-600 text-white relative"
      >
        <span class="text-2xl">🔔</span>
        <span
          v-if="badgeCount > 0"
          class="absolute -top-1 -right-1 bg-white text-red-600 text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center border"
        >
          {{ badgeCount }}
        </span>
      </button>
    </div>
=======
  <div class="min-h-screen bg-white flex flex-col items-center p-6">
    <!-- ปุ่ม Logout -->
    <button @click="logout" class="flex flex-col items-center text-sm text-gray-700 mb-4">
      <span class="text-2xl">⚙️</span>
      <span>ออกจากระบบ</span>
    </button>
>>>>>>> 2c0ec257df8b67e1f17359536c85b58edb9deca5

    <h1 class="text-lg font-bold mb-6">ตรวจสอบอุปกรณ์อาคาร</h1>

    <!-- เมนู -->
    <div class="w-full max-w-md space-y-3">
      <button
        v-for="item in menuItems"
        :key="item.label"
        :class="[
          'w-full flex items-center justify-between px-4 py-3 border rounded-xl shadow-sm',
          item.checked ? 'bg-green-400 text-white cursor-not-allowed' : 'hover:bg-gray-50'
        ]"
        @click="goToPage(item)"
      >
        <span class="flex items-center space-x-2">
          <span class="text-xl font-bold">+</span>
          <span>{{ item.label }}</span>
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
<<<<<<< HEAD
import { ref } from "vue";

const menuItems = [
  { label: "รายวัน" },
  { label: "รายเดือน" },
  { label: "รายปี" },
  { label: "ไตรมาส" },
];

const badgeCount = ref(1); 
=======
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

// รายการเมนู
const menuItems = ref([
  { label: "แบบฟอร์ม", checked: false },
  { label: "ปฏิทินย้อนหลัง", checked: false },
]);

// Mapping ป้ายชื่อไปยัง route
const routeMap = {
  "แบบฟอร์ม": "/InspectionDay",
  "ปฏิทินย้อนหลัง": "/history",
};

// ฟังก์ชันไปยังหน้าเฉพาะ
const goToPage = (item) => {
  if (item.checked) {
    alert("คุณตรวจสอบไปแล้ว");
    return; // ไม่เข้าไปหน้าอื่น
  }

  const path = routeMap[item.label];
  if (path) router.push(path);
};

// ดึงสถานะจาก API
const fetchStatus = async () => {
  try {
    // ใช้ Promise.all ดึงทุก category
    const categories = ["แบบฟอร์มตรวจสอบเครื่องจักร (day)", "แบบฟอร์มตรวจสอบเครื่องจักร (month)", "แบบฟอร์มตรวจสอบเครื่องจักร (quarter)", "แบบฟอร์มตรวจสอบเครื่องจักร (year)"];
    const requests = categories.map(cat =>
      axios.get("http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.formmm.formmm.get_inspection_status", { params: { category: cat } })
    );

    const responses = await Promise.all(requests);

    // Mapping category => menuItems index
    const catMap = {
      "แบบฟอร์มตรวจสอบเครื่องจักร (day)": 0,
      "แบบฟอร์มตรวจสอบเครื่องจักร (month)": 1,
      "แบบฟอร์มตรวจสอบเครื่องจักร (year)": 2,
      "แบบฟอร์มตรวจสอบเครื่องจักร (quarter)": 3,
    };

    responses.forEach(res => {
      const data = res.data.message;
      const cat = data.length > 0 && data[0].status !== undefined ? Object.keys(catMap).find(k => catMap[k] === catMap[k]) : null;

      // ตรวจสอบว่ามี checked หรือไม่
      const isChecked = data.some(d => d.status === "checked");
      // อัพเดท menuItems
      const idx = catMap[res.config.params.category];
      if (idx !== undefined) menuItems.value[idx].checked = isChecked;
    });

  } catch (error) {
    console.error(error);
  }
};

// ตรวจสอบว่า session ของ Frappe ยังอยู่
const checkLogin = async () => {
  try {
    const res = await fetch("/api/method/frappe.auth.get_logged_user", { credentials: "include" });
    const data = await res.json();
    if (!data.message || data.message === "Guest") router.replace("/login");
  } catch (error) {
    console.error(error);
    router.replace("/login");
  }
};

// Logout → ไปหน้า login
const logout = async () => {
  try { await fetch("/api/method/logout", { credentials: "include" }); } 
  catch (error) { console.error(error); } 
  finally { router.replace("/login"); }
};

onMounted(() => {
  checkLogin();
  fetchStatus();
});
>>>>>>> 2c0ec257df8b67e1f17359536c85b58edb9deca5
</script>
