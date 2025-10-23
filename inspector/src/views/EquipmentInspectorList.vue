<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Equipment Inspector List</h2>

    <p class="mb-4">
      ช่วงเวลา: <span class="font-semibold">{{ displayPeriod }}</span>
    </p>

    <!-- ปุ่มตรวจสอบอุปกรณ์ (แสดงเฉพาะ incomplete) -->
    <div v-if="showTopButton" class="mb-4">
      <button
        @click="goToInspectionTop"
        class="bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600"
      >
        ตรวจสอบอุปกรณ์
      </button>
    </div>

    <table class="border-collapse border w-full text-center">
      <thead class="bg-gray-200">
        <tr>
          <th>ชื่ออุปกรณ์</th>
          <th>สิ่งที่ตรวจสอบ</th>
          <th>ค่าที่ตรวจสอบได้</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in allEquipment" :key="item.code || item.equipment || item.title">
          <td class="align-top">{{ item.equipment || item.title }}</td>
          <td class="text-left">
            <ul class="pl-5">
              <li v-for="ind in item.indicators || []" :key="ind.title">
                {{ ind.title }}
              </li>
            </ul>
          </td>
          <td class="text-left">
            <ul class="pl-5">
              <li v-for="ind in item.indicators || []" :key="ind.title">
                {{ ind.value || 'ยังไม่ได้กรอก' }}
              </li>
            </ul>
            <span v-if="!item.indicators || item.indicators.length === 0" class="text-red-600">
              ยังไม่ได้กรอก
            </span>
          </td>
        </tr>

        <tr v-if="allEquipment.length === 0">
          <td colspan="3">ไม่พบข้อมูล</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const equipmentData = ref([])
const remainingEquipment = ref([])

// --- แสดงช่วงเวลา ---
const displayPeriod = computed(() => {
  const { period, day, month, year, quarter } = route.query
  if (!period) return 'ไม่ระบุช่วงเวลา'
  switch (period) {
    case 'วัน': return day && month && year ? `${day}/${month}/${year}` : 'ไม่ระบุวัน'
    case 'เดือน': return month && year ? `${month}/${year}` : 'ไม่ระบุเดือน'
    case 'ไตรมาส': return quarter && year ? `Q${quarter} ${year}` : 'ไม่ระบุไตรมาส'
    case 'ปี': return year || 'ไม่ระบุปี'
    default: return 'ไม่ระบุช่วงเวลา'
  }
})

// --- รวมข้อมูลอุปกรณ์พร้อม date และ value ---
const allEquipment = computed(() => [
  ...equipmentData.value.map(item => ({
    ...item,
    indicators: item.indicators.map(ind => ({
      ...ind,
      value: ind.value || 'ยังไม่ได้กรอก'
    })) || [],
    date: item.date || (route.query.period?.trim() === 'วัน' && route.query.year && route.query.month && route.query.day
      ? `${route.query.year}-${String(route.query.month).padStart(2, '0')}-${String(route.query.day).padStart(2, '0')}`
      : new Date().toISOString().split('T')[0]
    )
  })),
  ...remainingEquipment.value.map(item => ({
    equipment: item.title,
    indicators: item.indicators.map(ind => ({
      title: ind.title,
      value: ind.value || 'ยังไม่ได้กรอก'
    })) || [],
    date: item.date || (route.query.period?.trim() === 'วัน' && route.query.year && route.query.month && route.query.day
      ? `${route.query.year}-${String(route.query.month).padStart(2, '0')}-${String(route.query.day).padStart(2, '0')}`
      : new Date().toISOString().split('T')[0]
    ),
    code: item.code,
    period: item.period,
    day: item.day,
    month: item.month,
    year: item.year,
    quarter: item.quarter
  }))
])

// --- Fetch ข้อมูลอุปกรณ์ ---
async function fetchEquipment() {
  try {
    const params = { ...route.query }
    if (params.period === 'ไตรมาส' && params.quarter) {
      const quarterStartMonth = { '1': 1, '2': 4, '3': 7, '4': 10 }
      params.month = quarterStartMonth[params.quarter]
    }
    const res = await axios.get(
      'http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.get_equipment_inspector_details',
      { params }
    )
    const message = res.data.message
    if (message.status) {
      equipmentData.value = message.data.map(item => ({
        ...item,
        indicators: item.indicators.map(ind => ({
          ...ind,
          value: ind.value || 'ยังไม่ได้กรอก'
        }))
      }))
      remainingEquipment.value = message.remaining_equipment || []
    } else {
      equipmentData.value = []
      remainingEquipment.value = []
      if (message.message) alert(message.message)
    }
  } catch (err) {
    console.error(err)
    equipmentData.value = []
    remainingEquipment.value = []
  }
}

// --- แสดงปุ่มเฉพาะ incomplete สำหรับทุก period ---
const showTopButton = computed(() => {
  if (!route.query.period) return false

  const today = new Date()
  const yesterday = new Date()
  yesterday.setDate(today.getDate() - 1)

  return allEquipment.value.some(item => {
    const incomplete = item.indicators.some(ind => !ind.value || ind.value === 'ยังไม่ได้กรอก')
    if (!incomplete) return false

    const itemDate = new Date(item.date)

    switch (route.query.period) {
      case 'วัน':
        return itemDate.toDateString() === today.toDateString() ||
               itemDate.toDateString() === yesterday.toDateString()
      case 'เดือน':
        return itemDate.getMonth() + 1 === Number(route.query.month) &&
               itemDate.getFullYear() === Number(route.query.year)
      case 'ไตรมาส':
        const quarterStartMonth = { '1': 1, '2': 4, '3': 7, '4': 10 }
        const month = itemDate.getMonth() + 1
        const quarter = route.query.quarter
        const startMonth = quarterStartMonth[quarter]
        return month >= startMonth && month < startMonth + 3 &&
               itemDate.getFullYear() === Number(route.query.year)
      case 'ปี':
        return itemDate.getFullYear() === Number(route.query.year)
      default:
        return false
    }
  })
})

// --- ไปหน้า inspectionbacktest ---
function goToInspectionTop() {
  router.push({
    name: 'inspectionbacktest',
    query: {
      displayPeriod: displayPeriod.value,
      period: route.query.period,
      day: route.query.day,
      month: route.query.month,
      year: route.query.year,
      quarter: route.query.quarter
    }
  })
}

onMounted(() => {
  fetchEquipment()
})
</script>

<style scoped>
table, th, td { border: 1px solid #ccc; }
th, td { padding: 6px 12px; text-align: center; vertical-align: top; }
tbody tr:nth-child(odd) { background-color: #f9f9f9; }
.text-red-600 { color: #dc2626; }
ul { padding-left: 16px; margin: 0; }
button { cursor: pointer; }
</style>
