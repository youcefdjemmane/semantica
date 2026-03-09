<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue';
import OntologiesTable from '~/components/ontology/OntologiesTable.vue';
import type { OntologiesStats } from '~/types/ontology';
const config = useRuntimeConfig()


const stats = ref<OntologiesStats | null>(null)
const files = ref<any[]>([])

async function fetchStats() {
    try {
        stats.value = await $fetch<OntologiesStats>(`${config.public.apiBase}/ontology/stats`)
    } catch (error) {
        console.error('Failed to fetch ontology stats:', error)
    }
}
async function fetchFiles() {
    try {
        files.value = await $fetch<any[]>(`${config.public.apiBase}/ontology/files`)
    } catch (error) {
        console.error('Failed to fetch ontology files:', error)
    }
}
onMounted(() => {
    fetchStats();
    fetchFiles();
});


const refreshData = async () => {
    await Promise.all([fetchStats(), fetchFiles()])
}


</script>

<template>
    <div class="p-2 space-y-6">
        <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Ontologies" :data="stats?.total_ontologies || '0'" />
            <KpiCard title="Classes" :data="stats?.total_classes || '0'" />
            <KpiCard title="Properties" :data="stats?.total_properties || '0'" />
            <KpiCard title="Individuals" :data="stats?.total_individuals || '0'" />
            <KpiCard title="Formats">
                <template #content>

                    <div class="ml-6">
                        <p>
                            OWL : {{ stats?.owl_count }}
                        </p>
                        <p>
                            RDFS : {{ stats?.rdfs_count }}
                        </p>
                    </div>
                </template>
            </KpiCard>
        </div>
        <OntologiesTable :ontologies="files"  @refresh="refreshData" />
    </div>
</template>