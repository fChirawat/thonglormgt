<template>
  <div class="min-h-screen bg-white flex flex-col items-center p-6">
    <h1 class="text-lg font-bold mb-4">ตรวจสอบอุปกรณ์อาคาร</h1>

    <div class="w-full max-w-md mb-6">
      <h2 class="text-sm font-medium mb-2">แนวโน้ม</h2>
      <div class="bg-gray-100 rounded-lg p-4">
      
        <svg viewBox="0 0 300 100" class="w-full h-32">
          
          <rect v-for="(value, index) in data" 
                :key="index"
                :x="index * 40 + 10"
                :y="100 - value"
                width="20"
                :height="value"
                fill="#4b7350"
                rx="3"
          />
        </svg>
   
        <div class="flex justify-between text-xs text-gray-500 mt-2">
          <span v-for="(label, index) in labels" :key="index">{{ label }}</span>
        </div>
      </div>
    </div>


    <div class="w-full max-w-md mt-2 space-y-3">

      <div class="bg-gray-100 rounded-lg shadow">
        <button
          @click="toggleAccordion"
          class="w-full flex justify-between items-center px-4 py-3"
        >
          <span class="flex items-center space-x-2">
            <span class="text-xl">➕</span>
            <span>ตรวจอุปกรณ์</span>
          </span>
          <span class="text-gray-500">{{ isOpen ? "⌄" : ">" }}</span>
        </button>

        <div v-if="isOpen" class="px-8 py-2 space-y-2">
          <button class="w-full text-left flex items-center space-x-2">
            <span class="text-sm">➕</span>
            <span>ตรวจอุปกรณ์รายวัน</span>
          </button>
          <button class="w-full text-left flex items-center space-x-2">
            <span class="text-sm">➕</span>
            <span>ตรวจอุปกรณ์รายเดือน</span>
          </button>
        </div>
      </div>

      <button
        class="w-full flex items-center space-x-2 bg-white px-4 py-3 rounded-lg border shadow"
      >
        <span class="text-xl">🔔</span>
        <span>แจ้งเตือน</span>
      </button>

      <button
        class="w-full flex items-center space-x-2 bg-white px-4 py-3 rounded-lg border shadow"
      >
        <span class="text-xl">📋</span>
        <span>ตรวจสอบย้อนหลัง</span>
      </button>
    </div>

    <div
      class="fixed bottom-0 w-full max-w-md flex justify-around bg-white border-t py-2"
    >
      <button class="flex flex-col items-center text-gray-800">
        <span class="text-2xl">🏠</span>
        <span class="text-xs">หน้าหลัก</span>
      </button>
      <button class="flex flex-col items-center text-gray-500">
        <span class="text-2xl">⚙️</span>
        <span class="text-xs">ตั้งค่า</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const isOpen = ref(false);
const toggleAccordion = () => {
  isOpen.value = !isOpen.value;
};

const data = [40, 60, 30, 80, 50, 70, 60];
const labels = ["month 1", "month 2", "month 3", "month 4", "month 5", "month 6", "month 7"];
</script>
