<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue';
import LoadedFilesTable from '~/components/dashboard/LoadedFilesTable.vue';
import NamespaceDistDonut from '~/components/dashboard/NamespaceDistDonut.vue';
import TopPredicatesBar from '~/components/dashboard/TopPredicatesBar.vue';
import TripleDistributionPie from '~/components/dashboard/TripleDistributionPie.vue';
import ReasoningEngine from '~/components/dashboard/ReasoningEngine.vue';
import OntologyOverview from '~/components/dashboard/OntologyOverview.vue';
import RecentSparql from '~/components/dashboard/RecentSparql.vue';
import ExportResults from '~/components/dashboard/ExportResults.vue';
import SparqlStatsCard from '~/components/dashboard/SparqlStatsCard.vue';
import GraphSizeBar from '~/components/dashboard/GraphSizeBar.vue';
import ActivityTimeline from '~/components/dashboard/ActivityTimeline.vue';
import SmartInsights from '~/components/dashboard/SmartInsights.vue';
import GraphHealthScore from '~/components/dashboard/GraphHealthScore.vue';

import { useDashboard } from '~/composables/useDashboard';
import { computed, onMounted } from 'vue';

definePageMeta({
    title: 'Dashboard',
})

const { metrics, ontologyStats, loadedFiles, isLoading, fetchAllDashboardData } = useDashboard();

onMounted(() => {
    fetchAllDashboardData();
});

// KPI computed values from real data
const totalTriples   = computed(() => metrics.value?.kpis?.total_triples    ?? '…');
const totalSubjects  = computed(() => metrics.value?.kpis?.total_subjects   ?? '…');
const totalPredicates= computed(() => metrics.value?.kpis?.total_predicates ?? '…');
const totalObjects   = computed(() => metrics.value?.kpis?.total_objects    ?? '…');
const totalOntologies= computed(() => ontologyStats.value?.total_ontologies ?? '…');
</script>



<template>
    <div class="p-2 space-y-4">

        <!-- ROW 1 — KPI Cards -->
        <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Total triples"  :data="totalTriples"    footer="across all graphs" />
            <KpiCard title="Subjects"       :data="totalSubjects"   footer="unique" />
            <KpiCard title="Predicates"     :data="totalPredicates" footer="unique" />
            <KpiCard title="Objects"        :data="totalObjects"    footer="unique" />
            <KpiCard title="Ontologies"     :data="totalOntologies" footer="loaded" />
        </div>

        <!-- ROW 1.5 — Copilot and Health Score -->
        <div class="grid grid-cols-5 gap-4">
            <div class="col-span-3">
                <SmartInsights />
            </div>
            <div class="col-span-2">
                <GraphHealthScore />
            </div>
        </div>

        <!-- ROW 2 — Charts -->
        <div class="grid grid-cols-3 gap-4">
            <TripleDistributionPie />
            <TopPredicatesBar />
            <NamespaceDistDonut />
        </div>

        <div class="grid grid-cols-3 gap-4">
            <SparqlStatsCard />
            <GraphSizeBar />
            <ActivityTimeline />
        </div>

        <!-- ROW 4 — Ontology + Reasoning -->
        <div class="grid grid-cols-2 gap-4">
            <OntologyOverview />
            <ReasoningEngine />
        </div>

        <!-- ROW 5 — Loaded Files -->
        <LoadedFilesTable :data="loadedFiles" />

        <!-- ROW 6 — SPARQL History + Export -->
        <div class="grid grid-cols-2 gap-4">
            <RecentSparql />
            <ExportResults />
        </div>

    </div>
</template>
