<template>
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
  </div>
</template>

<script setup>
import { ref } from "vue";

const menuItems = [
  { label: "รายวัน" },
  { label: "รายเดือน" },
  { label: "รายปี" },
  { label: "ไตรมาส" },
];

const badgeCount = ref(1); 
</script>
