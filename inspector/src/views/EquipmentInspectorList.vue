<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h2 class="text-xl font-bold mb-4">Equipment Inspector List</h2>

    <p class="mb-4">
      ช่วงเวลา: <span class="font-semibold">{{ displayPeriod }}</span>
    </p>

    <table class="border-collapse border w-full text-center">
      <thead class="bg-gray-200">
        <tr>
          <th>ชื่ออุปกรณ์</th>
          <th>สิ่งที่ตรวจสอบ</th>
          <th>ค่าที่ตรวจสอบได้</th>
        </tr>
      </thead>
      <tbody>
        <!-- ข้อมูล inspector -->
        <template v-if="equipmentData.length">
          <tr v-for="item in equipmentData" :key="item.code">
            <td class="align-top">{{ item.equipment }}</td>
            <td class="text-left">
              <ul class="list-disc pl-5">
                <li v-for="ind in item.indicators" :key="ind.title">{{ ind.title }}</li>
              </ul>
            </td>
            <td class="text-left">
              <ul class="list-disc pl-5">
                <li v-for="ind in item.indicators" :key="ind.title">{{ ind.value }}</li>
              </ul>
            </td>
          </tr>
        </template>

        <!-- ถ้าไม่มีข้อมูล inspector -->
        <template v-else>
          <tr v-for="item in remainingEquipment" :key="item.code">
            <td>{{ item.title }}</td>
            <td colspan="2" class="text-red-600">ยังไม่ได้กรอก</td>
          </tr>
          <tr v-if="!remainingEquipment.length">
            <td colspan="3">ไม่พบข้อมูล</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const equipmentData = ref([])
const remainingEquipment = ref([])

const displayPeriod = computed(() => {
  const q = route.query
  if (!q.period) return ''
  if (q.period === 'วัน') return `${q.day}/${q.month}/${q.year}`
  if (q.period === 'เดือน') return `${q.month}/${q.year}`
  if (q.period === 'ไตรมาส') return `Q${q.quarter} ${q.year}`
  if (q.period === 'ปี') return q.year
  return ''
})

async function fetchEquipment() {
  try {
    const params = { ...route.query }

    // แปลง quarter → month สำหรับ backend
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
          value: ind.value
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

onMounted(fetchEquipment)
</script>

<style scoped>
table, th, td { border: 1px solid #ccc; }
th, td { padding: 6px 12px; text-align: center; vertical-align: top; }
tbody tr:nth-child(odd) { background-color: #f9f9f9; }
.text-red-600 { color: #dc2626; }
ul { padding-left: 16px; margin: 0; }
</style>
