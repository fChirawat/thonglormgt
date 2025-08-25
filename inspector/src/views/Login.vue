<template>
  <div class="login-page">
    <div class="login-box">
      <h2>ตรวจสอบอุปกรณ์อาคาร</h2>

    
      <input
        v-model="username"
        type="text"
        placeholder="ชื่อผู้ใช้"
        class="input-field"
      />

    
      <select v-model="userType" class="input-field">
        <option value="" disabled>ประเภทผู้ใช้งาน</option>
        <option value="inspector">เจ้าหน้าที่ตรวจสอบ</option>
        <option value="admin">แอดมิน</option>
      </select>

     
      <input
        v-model="password"
        type="password"
        placeholder="รหัสผ่าน"
        class="input-field"
      />

    
      <button @click="handleLogin" class="login-button">
        ล็อกอิน
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const username = ref("");
const userType = ref("");
const password = ref("");

const handleLogin = () => {
  if (!username.value || !userType.value || !password.value) {
    alert("กรุณากรอกข้อมูลให้ครบ");
    return;
  }
  alert(`ล็อกอิน: ${username.value} (${userType.value})`);
  
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}


.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
  background-color: #f8fafc; 
}

.login-box {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
}

.login-box h2 {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 25px;
}


.input-field {
  padding: 12px;
  margin-bottom: 15px;
  border: none;
  background-color: #f2f4f7;
  border-radius: 8px;
  font-size: 14px;
}

.input-field:focus {
  outline: none;
  box-shadow: 0 0 0 2px #4da6ff;
}


.login-button {
  padding: 12px;
  background-color: #00a2ff;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 15px;
  font-weight: bold;
  transition: background 0.3s ease;
}

.login-button:hover {
  background-color: #008ad1;
  cursor: pointer;
}
</style>
