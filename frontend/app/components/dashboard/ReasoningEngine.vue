<script setup lang="ts">
import { ArrowRight, CirclePlay } from 'lucide-vue-next';
import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { sparqlStats, metrics } = useDashboard();

const inferredCount = computed(() => metrics.value?.kpis?.total_triples ?? 0);
</script>

<template>
    <Card class="flex flex-col justify-between">
        <CardHeader>Reasoning Engine</CardHeader>
        <CardContent class="space-y-2">
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Status</span>
                <span class="font-medium text-green-500">Active</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Formalism</span>
                <span class="font-medium text-blue-400">RDFS / OWL 2 RL</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Inferred Triples</span>
                <span class="font-medium text-gray-800 dark:text-gray-100">0</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">SPARQL Queries Run</span>
                <span class="font-medium text-gray-800 dark:text-gray-100">
                    {{ sparqlStats?.total_queries ?? 0 }}
                </span>
            </div>
        </CardContent>
        <CardFooter class="flex items-center justify-end space-x-2">
            <NuxtLink to="/reasoning">
                <Button>
                    <CirclePlay />
                    Run Reasoning
                </Button>
            </NuxtLink>
            <NuxtLink to="/reasoning">
                <Button variant="outline">
                    <ArrowRight/>
                    Go to Reasoning 
                </Button>
            </NuxtLink>
        </CardFooter>
    </Card>
</template>
