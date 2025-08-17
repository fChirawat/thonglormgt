<template>
    <div>
        Current User: {{ username }}
        <Button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout </Button>
    </div>
</template>

<script lang="ts" setup>
import { inject,onMounted,ref } from 'vue'
import Button from '@/volt/Button.vue';


const $auth = inject('$auth')
const $frappeApp = inject('$frappeApp')
const auth = $frappeApp.auth()

console.log('auth',$auth)
console.log('frappeApp',$frappeApp)


const username = ref('')

onMounted(async () => {
  let x = await auth.getLoggedInUser();
  console.log('x', x);
  username.value = x;
})

</script>