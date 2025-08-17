<template>
	<div>

		<Button label="Hello World" />


		<h1 class="text-3xl">Hello</h1>
		<button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</button>
		<router-view />
	</div>
</template>


<script setup lang='ts'>
import { inject } from 'vue'
import Button from '@/volt/Button.vue';


	const $auth = inject('$auth')
	console.log($auth)
</script>
