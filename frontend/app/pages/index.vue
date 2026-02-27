<script setup lang="ts">
import KpiCard from '~/components/dashboard/KpiCard.vue';
import LoadedFilesTable from '~/components/dashboard/LoadedFilesTable.vue';
import type { LoadedFile } from '~/types/loaded_files';
import NamespaceDistDonut from '~/components/dashboard/NamespaceDistDonut.vue';
import TopPredicatesBar from '~/components/dashboard/TopPredicatesBar.vue';
import TripleDistributionPie from '~/components/dashboard/TripleDistributionPie.vue';
import ReasoningEngine from '~/components/dashboard/ReasoningEngine.vue';
import OntologyOverview from '~/components/dashboard/OntologyOverview.vue';

definePageMeta({
    title: 'Dashboard',
})

const dataCard = ref({
    totalRevenue: 0,
    newCustomers: 0,
    activeAccount: 0,
    growthRate: 0,
})
onMounted(() => {
    dataCard.value = {
        totalRevenue: 1250.44,
        newCustomers: 1234,
        activeAccount: 45678,
        growthRate: 4.5,
    }
})



const files: LoadedFile[] = [
  {
    name: "my-graph.ttl",
    type: "RDF",
    format: "Turtle",
    triples: 1243,
    uploaded: "today",
  },
  {
    name: "foaf.owl",
    type: "Ontology",
    format: "OWL",
    triples: 89,
    uploaded: "today",
  },
  {
    name: "schema.rdf",
    type: "RDF",
    format: "RDF/XML",
    triples: 542,
    uploaded: "yesterday",
  },
]
</script>


<template>
    <div class="p-6 space-y-4">

        <!-- ROW 1 — KPI Cards -->
        <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Total triples" data="1243" footer="in active graph" />
            <KpiCard title="Subjects" data="340" footer="unique" />
            <KpiCard title="Predicates" data="28" footer="unique" />
            <KpiCard title="Objects" data="890" footer="unique" />
            <KpiCard title="Inferred" data="0" footer="reasoning off" />
        </div>

        <!-- ROW 2 — Charts -->
        <div class="grid grid-cols-3 gap-4">
            
            <TripleDistributionPie />
            <TopPredicatesBar />
            <NamespaceDistDonut />

        </div>

        <!-- ROW 3 — Ontology + Reasoning -->
        <div class="grid grid-cols-2 gap-4">
           <OntologyOverview />

            <ReasoningEngine />
        </div>

        <!-- ROW 4 — Loaded Files -->
            
            <!--replace by shadcn table  -->
            <LoadedFilesTable :data="files" />

        <!-- ROW 5 — SPARQL History + Export -->
        <div class="grid grid-cols-2 gap-4">
            <div class=" rounded-xl p-4 shadow-sm border ">
                <p class="text-sm font-semibold text-gray-700 dark:text-gray-100 mb-3">Recent SPARQL Queries</p>
                <div class="space-y-2">
                    <div
                        class="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 transition-colors">
                        <div class="flex items-center gap-2 min-w-0">
                            <span
                                class="text-xs bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded font-mono shrink-0">SELECT</span>
                            <span class="text-xs text-gray-600 truncate">SELECT ?s ?p ?o WHERE...</span>
                        </div>
                        <button class="text-xs text-indigo-500 hover:text-indigo-700 font-medium shrink-0 ml-2">▶
                            Run</button>
                    </div>
                    <div
                        class="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 transition-colors">
                        <div class="flex items-center gap-2 min-w-0">
                            <span
                                class="text-xs bg-amber-100 text-amber-600 px-1.5 py-0.5 rounded font-mono shrink-0">ASK</span>
                            <span class="text-xs text-gray-600 truncate">ASK { ?x a :Person }</span>
                        </div>
                        <button class="text-xs text-indigo-500 hover:text-indigo-700 font-medium shrink-0 ml-2">▶
                            Run</button>
                    </div>
                    <div
                        class="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 transition-colors">
                        <div class="flex items-center gap-2 min-w-0">
                            <span
                                class="text-xs bg-purple-100 text-purple-600 px-1.5 py-0.5 rounded font-mono shrink-0">CONSTRUCT</span>
                            <span class="text-xs text-gray-600 truncate">CONSTRUCT { ?s ?p ?o }...</span>
                        </div>
                        <button class="text-xs text-indigo-500 hover:text-indigo-700 font-medium shrink-0 ml-2">▶
                            Run</button>
                    </div>
                </div>
                <NuxtLink to="/sparql"
                    class="mt-3 inline-block text-xs text-indigo-500 hover:text-indigo-700 font-medium">
                    Go to SPARQL Editor →
                </NuxtLink>
            </div>

            <div class=" rounded-xl p-4 shadow-sm border ">
                <p class="text-sm font-semibold text-gray-700 dark:text-gray-100 mb-3">Export Results</p>
                <div class="space-y-2 mb-4">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Last Query</span>
                        <span class="text-gray-800 dark:text-gray-100 font-medium">SELECT</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Rows</span>
                        <span class="text-gray-800 dark:text-gray-100 font-medium">342</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Executed</span>
                        <span class="text-gray-400">2 min ago</span>
                    </div>
                </div>
                <div class="flex gap-2">
                    <button
                        class="text-xs bg-gray-800 hover:bg-gray-900 text-white px-3 py-1.5 rounded-lg font-medium transition-colors">
                        📥 Export CSV
                    </button>
                    <button
                        class="text-xs bg-gray-800 hover:bg-gray-900 text-white px-3 py-1.5 rounded-lg font-medium transition-colors">
                        📥 Export JSON
                    </button>
                </div>
            </div>
        </div>

    </div>
</template>
