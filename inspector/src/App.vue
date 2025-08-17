<template>
	<div>
		<router-view />
	</div>
</template>


<script setup lang='ts'>
import { inject } from 'vue'
import Button from '@/volt/Button.vue';


	const $auth = inject('$auth')
	console.log($auth)
</script>
