<script setup lang="ts">

defineProps<{
    title: string,
    data?: any,
    footer?: unknown
}>()
</script>


<template>
    <Card class="@container/card">

        <CardHeader>
            <p class="text-2xl">{{ title }}</p>
        </CardHeader>
        <CardContent v-if="data"  :class=" data === '0' ? 'text-indigo-500':  'text-slate-800  dark:text-gray-100'" >
            <p class="text-3xl font-semibold">{{ data }}</p>
        </CardContent>
        <slot name="content" />
        <CardFooter v-if="footer" class="text-xs text-gray-400 mt-1">{{ footer }}</CardFooter>
        <slot name="footer" />
    </Card>
</template>