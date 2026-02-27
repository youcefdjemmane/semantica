<script setup lang="ts">

defineProps<{
    title: string,
    data: string,
    footer?: unknown
}>()
</script>


<template>
    <Card class=" rounded-xl p-4 shadow-sm border ">
        <p class="text-xs text-gray-500 font-medium uppercase tracking-wide">{{ title }}</p>
        <p class="text-2xl font-bold   mt-1" :class=" data === '0' ? 'text-indigo-500':  'text-gray-800  dark:text-gray-100'" >{{ data }}</p>
        <p class="text-xs text-gray-400 mt-1">{{ footer }}</p>
    </Card>
</template>