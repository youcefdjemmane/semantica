<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue';
import GraphsTable from '~/components/rdf/GraphsTable.vue';
const config = useRuntimeConfig()


import type { GraphsStats } from '~/types/rdf';
const stats = ref<GraphsStats | undefined>(undefined);

const files = ref<any[]>([]);   


async function fetchStats() {
    try {
        stats.value = await $fetch<GraphsStats>(`${config.public.apiBase}/rdf/stats`)
    } catch (error) {
        console.error('Failed to fetch graphs stats:', error)
    }
}
async function fetchFiles() {
    try {
        files.value = await $fetch<any[]>(`${config.public.apiBase}/rdf/files`)
    } catch (error) {
        console.error('Failed to fetch graphs files:', error)
    }
}

onMounted(() => {
    fetchStats();
    fetchFiles();
});

definePageMeta({
    title: "RDF Graphs",
})

const refreshData = async () => {
    await Promise.all([fetchStats(), fetchFiles()])
}

</script>

<template>
    <div class="p-2 space-y-6">
        <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Graphs" :data="stats?.total_graphs || '0'" />
            <KpiCard title="Triples" :data="stats?.total_triples || '0'" />
            <KpiCard title="Subjects" :data="stats?.total_subjects || '0'" />
            <KpiCard title="Predicates" :data="stats?.total_predicates ||'0'" />
            <KpiCard title="Objects" :data="stats?.total_objects || '0'" />

        </div>
        <div class="w-full">
            <GraphsTable :graphs="files" @refresh="refreshData" />
        </div>

    </div>

</template>