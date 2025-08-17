<template>
    <div>
        <Navbar></Navbar>
        <router-view></router-view>
        <div>Footer</div>
    </div>
</template>

<script setup lang='ts'>
import Navbar from "../components/Navbar.vue"
</script>