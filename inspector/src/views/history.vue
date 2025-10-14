<template>
  <div class="p-6 max-w-6xl mx-auto">
    <!-- เลือก Period -->
    <div class="mb-4 flex gap-4">
      <label class="font-semibold mr-2">Period:</label>
      <select v-model="selectedPeriod" class="border p-2 rounded">
        <option value="day">วัน</option>
        <option value="month">เดือน</option>
        <option value="quarter">ไตรมาส</option>
        <option value="year">ปี</option>
      </select>
    </div>

    <!-- ปฏิทิน วัน -->
    <div v-if="selectedPeriod === 'day'">
      <div class="flex justify-between mb-2">
        <button @click="prevMonth" class="border p-1 rounded">‹ เดือนก่อน</button>
        <span class="font-semibold text-lg">{{ monthNames[currentMonth] }} {{ currentYear }}</span>
        <button @click="nextMonth" class="border p-1 rounded">เดือนถัด ›</button>
      </div>
      <table class="border-collapse border w-full text-center">
        <thead class="bg-gray-200">
          <tr>
            <th v-for="day in weekDays" :key="day">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(week, idx) in dayCalendar" :key="idx">
            <td v-for="d in week" :key="d" 
                :class="getCellColor(formatDate(currentYear, currentMonth, d), 'day')"
                :title="getCellTooltip(formatDate(currentYear, currentMonth, d), 'day')"
                @click="handleCellClick(formatDate(currentYear, currentMonth, d), 'day')">
              {{ d || '' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ปฏิทิน เดือน -->
    <div v-if="selectedPeriod === 'month'">
      <div class="flex justify-between mb-2">
        <button @click="prevYear" class="border p-1 rounded">‹ ปีก่อน</button>
        <span class="font-semibold text-lg">{{ currentYear }}</span>
        <button @click="nextYear" class="border p-1 rounded">ปีถัด ›</button>
      </div>
      <table class="border-collapse border w-full text-center">
        <tbody>
          <tr>
            <td v-for="(month, idx) in monthNames" :key="idx" 
                :class="getCellColor(formatMonth(currentYear, idx), 'month')"
                :title="getCellTooltip(formatMonth(currentYear, idx), 'month')"
                @click="handleCellClick(formatMonth(currentYear, idx), 'month')">
              {{ idx + 1 }}/{{ currentYear }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ปฏิทิน ไตรมาส -->
    <div v-if="selectedPeriod === 'quarter'">
      <div class="flex justify-between mb-2">
        <button @click="prevYear" class="border p-1 rounded">‹ ปีก่อน</button>
        <span class="font-semibold text-lg">{{ currentYear }}</span>
        <button @click="nextYear" class="border p-1 rounded">ปีถัด ›</button>
      </div>
      <table class="border-collapse border w-full text-center">
        <tbody>
          <tr>
            <td v-for="q in 4" :key="q" 
                :class="getCellColor(formatQuarter(currentYear, q), 'quarter')"
                :title="getCellTooltip(formatQuarter(currentYear, q), 'quarter')"
                @click="handleCellClick(formatQuarter(currentYear, q), 'quarter')">
              {{ quarterMonths[q - 1] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ปฏิทิน ปี -->
    <div v-if="selectedPeriod === 'year'">
      <div class="flex justify-between mb-2">
        <button @click="prevDecade" class="border p-1 rounded">‹ 10 ปีก่อน</button>
        <span class="font-semibold text-lg">{{ yearStart }} - {{ yearStart + 9 }}</span>
        <button @click="nextDecade" class="border p-1 rounded">10 ปีถัด ›</button>
      </div>
      <table class="border-collapse border w-full text-center">
        <tbody>
          <tr>
            <td v-for="y in 10" :key="y" 
                :class="getCellColor(String(yearStart + (y-1)), 'year')"
                :title="getCellTooltip(String(yearStart + (y-1)), 'year')"
                @click="handleCellClick(String(yearStart + (y-1)), 'year')">
              {{ yearStart + (y-1) + 543 }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup Modal ตาราง (แสดงทั้งตรวจแล้วและยังไม่ได้กรอก) -->
    <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded shadow-lg max-w-lg w-full max-h-[80vh] overflow-auto">
        <h3 class="text-lg font-bold mb-4">สถานะอุปกรณ์</h3>
        <table class="table-auto border-collapse border w-full text-left mb-4">
          <thead>
            <tr class="bg-gray-200">
              <th class="border px-2 py-1">ลำดับ</th>
              <th class="border px-2 py-1">ชื่ออุปกรณ์</th>
              <th class="border px-2 py-1">สถานะ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in popupItems" :key="index" :class="item.status === '❌' ? 'bg-red-100' : 'bg-green-100'">
              <td class="border px-2 py-1">{{ index + 1 }}</td>
              <td class="border px-2 py-1">{{ item.title }}</td>
              <td class="border px-2 py-1 font-semibold" :class="item.status === '❌' ? 'text-red-600' : 'text-green-600'">{{ item.status }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="showPopup = false" class="bg-blue-500 text-white px-4 py-2 rounded">ปิด</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const selectedPeriod = ref('day')
const currentDate = new Date()
const currentMonth = ref(currentDate.getMonth())
const currentYear = ref(currentDate.getFullYear())
const monthNames = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
const weekDays = ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.']
const quarterMonths = ['ม.ค.-มี.ค.', 'เม.ย.-มิ.ย.', 'ก.ค.-ก.ย.', 'ต.ค.-ธ.ค.']
const calendarData = ref({})
const yearStart = ref(currentDate.getFullYear())

// Popup
const showPopup = ref(false)
const popupItems = ref([])

function formatDate(year, month, day) { return `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}` }
function formatMonth(year, monthIndex) { return `${year}-${monthIndex+1}` }
function formatQuarter(year, q) { return `${year}-${q}` }

const dayCalendar = computed(() => {
  const weeks = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  let week = Array(7).fill(null)
  let dayCounter = 1
  const startIndex = (firstDay + 6) % 7
  for (let i = startIndex; i < 7; i++) week[i] = dayCounter++
  weeks.push([...week])
  while (dayCounter <= daysInMonth) {
    week = Array(7).fill(null)
    for (let i = 0; i < 7 && dayCounter <= daysInMonth; i++) week[i] = dayCounter++
    weeks.push([...week])
  }
  return weeks
})

function nextMonth() { if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++ } else currentMonth.value++ }
function prevMonth() { if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value-- } else currentMonth.value-- }
function nextYear() { currentYear.value++ }
function prevYear() { currentYear.value-- }
function nextDecade() { yearStart.value += 10 }
function prevDecade() { yearStart.value -= 10 }

async function fetchCalendar() {
  try {
    let params = { period: '', year: currentYear.value }
    if (selectedPeriod.value === 'day') params.period = 'วัน', params.month = currentMonth.value + 1
    else if (selectedPeriod.value === 'month') params.period = 'เดือน'
    else if (selectedPeriod.value === 'quarter') params.period = 'ไตรมาส'
    else if (selectedPeriod.value === 'year') params.period = 'ปี'

    const res = await axios.get('http://localhost:8001/api/method/thonglormgt.thonglormgt.doctype.equipment_inspector.equipment_inspector.check_period', { params })
    calendarData.value = res.data.message.status ? res.data.message.data : {}
  } catch (err) {
    console.error(err)
    calendarData.value = {}
  }
}

// สีช่อง
function getCellColor(key, type = 'day') {
  if (!key) return ''
  let matchedKey
  if (type === 'day') matchedKey = Object.keys(calendarData.value).find(k => k.startsWith(key))
  else matchedKey = Object.keys(calendarData.value).find(k => k === key || k === key + '✅')
  if (!matchedKey) return ''
  const data = calendarData.value[matchedKey]
  if (!data) return ''
  if (matchedKey.endsWith('✅')) return 'bg-green-200'
  const anyCheck = data.some(item => item.status === '✅')
  return anyCheck ? 'bg-orange-200' : ''
}

// tooltip
function getCellTooltip(key, type = 'day') {
  if (!key) return ''
  let matchedKey
  if (type === 'day') matchedKey = Object.keys(calendarData.value).find(k => k.startsWith(key))
  else matchedKey = Object.keys(calendarData.value).find(k => k === key || k === key + '✅')
  if (!matchedKey) return ''
  const data = calendarData.value[matchedKey]
  if (!data) return ''
  const missing = data.filter(item => item.status === '❌').map(item => item.title)
  if (missing.length) return 'Equipment ยังไม่ได้กรอก: ' + missing.join(', ')
  return ''
}

// คลิกช่อง
function handleCellClick(key, type = 'day') {
  if (!key) return

  // หา key ที่ตรงกับ calendarData
  let matchedKey
  if (type === 'day') matchedKey = Object.keys(calendarData.value).find(k => k.startsWith(key))
  else matchedKey = Object.keys(calendarData.value).find(k => k === key || k === key + '✅')
  if (!matchedKey) return

  const data = calendarData.value[matchedKey]
  if (!data || !data.length) return

  // ตรวจสอบ ✅ ทั้งหมด
  const isAllGreen = data.every(item => item.status === '✅') || matchedKey.endsWith('✅')

  if (isAllGreen) {
    // ส่งไปหน้า EquipmentInspectorList
    let query = { period: '', year: currentYear.value }
    if (type === 'day') {
      const [y, m, d] = key.split('-')
      query.period = 'วัน'; query.day = d; query.month = m; query.year = y
    } else if (type === 'month') {
      const [y, m] = key.split('-')
      query.period = 'เดือน'; query.month = m; query.year = y
    } else if (type === 'quarter') {
      const [y, q] = key.split('-')
      query.period = 'ไตรมาส'; query.quarter = q; query.year = y
    } else if (type === 'year') {
      query.period = 'ปี'; query.year = key
    }
    router.push({ name: 'EquipmentInspectorList', query })
  } else {
    // ถ้ายังมี ❌ → แสดง popup
    popupItems.value = data
    showPopup.value = true
  }
}


watch([selectedPeriod, currentMonth, currentYear], fetchCalendar, { immediate: true })
</script>

<style scoped>
table, th, td { border: 1px solid #ccc; }
th, td { padding: 6px 12px; text-align: center; }
tbody tr:nth-child(odd) { background-color: #f9f9f9; }
.bg-green-200 { background-color: #c6f6d5 !important; cursor: pointer; }
.bg-orange-200 { background-color: #fcd34d !important; cursor: pointer; }
</style>
