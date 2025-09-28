<template>
   <button class="flex flex-col items-center text-sm text-gray-700">
        <span class="text-2xl">⚙️</span>
        <span>ตั้งค่า</span>
   </button>
  <div class="min-h-screen bg-white flex flex-col items-center p-6">
    
    <h1 class="text-lg font-bold mb-6">ตรวจสอบอุปกรณ์อาคาร</h1>

    <div class="w-full max-w-md space-y-3">
      <button
        v-for="item in menuItems"
        :key="item.label"
        class="w-full flex items-center justify-between px-4 py-3 border rounded-xl shadow-sm hover:bg-gray-50"
      >
        <span class="flex items-center space-x-2">
          <span class="text-xl font-bold">+</span>
          <span>{{ item.label }}</span>
        </span>
      </button>
    </div>

    <div class="fixed bottom-0 w-full max-w-md bg-white border-t flex justify-around py-2">

    </div>
  </div>
</template>

<script setup>
const menuItems = [
  { label: "รายวัน" },
  { label: "รายเดือน" },
  { label: "รายปี" },
  { label: "ไตรมาส" },
];
</script>
