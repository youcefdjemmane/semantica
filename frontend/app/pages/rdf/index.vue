<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue';
import GraphsTable from '~/components/rdf/GraphsTable.vue';
const config = useRuntimeConfig()


import type { GraphsStats } from '~/types/rdf';
const stats = ref<GraphsStats | undefined>(undefined);

const files = ref<any[]>([]);   


async function fetchStats() {
    try {
        const { data, pending, error } = await useFetch<GraphsStats>(`${config.public.apiBase}/rdf/stats`)
        
        if (error.value) {
            console.error('Error fetching graphs stats:', error.value);
            return;
        }
        stats.value = data.value;
    } catch (error) {
        console.error('Failed to fetch graphs stats:', error);
    }
}
async function fetchFiles()
{
    try {
        const { data, pending, error } = await useFetch<any[]>(`${config.public.apiBase}/rdf/files`)
        
        if (error.value) {
            console.error('Error fetching graphs files:', error.value);
            return;
        }
        if (data.value) {
             files.value = data.value;
        }
    } catch (error) {
        console.error('Failed to fetch graphs files:', error);
    }
}

onMounted(() => {
    fetchStats();
    fetchFiles();
});

definePageMeta({
    title: "RDF Graphs",
})
/**
 * {
  "total_graphs": 1,
  "total_triples": 59,
  "total_subjects": 13,
  "total_predicates": 37,
  "total_objects": 54
}
 * 
 */

</script>

<template>
    <div class="p-2 space-y-6">
        <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Total graphs" :data="stats?.total_graphs || 0" />
            <KpiCard title="Total triples" :data="stats?.total_triples || 0" />
            <KpiCard title="Total subjects" :data="stats?.total_subjects || 0" />
            <KpiCard title="Total predicates" :data="stats?.total_predicates ||0" />
            <KpiCard title="Total objects" :data="stats?.total_objects || 0" />

        </div>
        <div class="w-full">
            <GraphsTable :graphs="files" />
        </div>

    </div>

</template>