<template>
  <div class="container">
    <header class="header">
      <h1>ตรวจสอบอุปกรณ์อาคาร</h1>
    </header>

    <main class="main-content">
      <section class="action-buttons">
        <button class="action-btn">
          <span class="icon">➕</span>
          <span>ตรวจอุปกรณ์</span>
        </button>
        <button class="action-btn">
          <span class="icon">🔔</span>
          <span>แจ้งเตือน</span>
        </button>
        <button class="action-btn">
          <span class="icon">📝</span>
          <span>ตรวจสอบย้อนหลัง</span>
        </button>
      </section>
    </main>

    <footer class="footer-nav">
      <nav class="nav-bar">
        <a href="#" class="nav-item active">
          <span class="icon">🏠</span>
          <span>หน้าหลัก</span>
        </a>
        <a href="#" class="nav-item">
          <span class="icon">⚙️</span>
          <span>ตั้งค่า</span>
        </a>
      </nav>
    </footer>
  </div>
</template>

<script>
export default {
  name: "BuildingInspectionPage",
};
</script>

<style scoped>
.container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 100%;             
  max-width: 1024px;      
  margin: auto;
  padding: 2rem;
  background-color: #f0f2f5;
  color: #333;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2rem;  
  font-weight: bold;
}

.main-content {
  flex-grow: 1;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.action-btn {
  background-color: #fff;
  border: none;
  border-radius: 15px;
  padding: 1.5rem 2rem;   
  text-align: left;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-size: 1.25rem;    
  color: #333;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.action-btn .icon {
  font-size: 2rem;          
}

.footer-nav {
  margin-top: auto;
  background-color: #fff;
  padding: 1rem 0;
  border-top: 1px solid #e0e0e0;
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
}

.nav-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #888;
  font-size: 1rem;
  padding: 0.75rem;
}

.nav-item.active {
  color: #007bff;
}

.nav-item .icon {
  font-size: 2rem;
  margin-bottom: 0.2rem;
}
</style>
