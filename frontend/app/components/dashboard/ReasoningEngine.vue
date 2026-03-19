<script setup lang="ts">
import { ArrowRight, CirclePlay } from 'lucide-vue-next';
import { useDashboard } from '~/composables/useDashboard';
import { useReasoningStore } from '~/store/reasoning';
import { computed } from 'vue';

const { sparqlStats } = useDashboard();
const reasoningStore = useReasoningStore();

const statusText = computed(() => reasoningStore.isEnabled ? 'Active' : 'Inactive');
const statusColor = computed(() => reasoningStore.isEnabled ? 'text-green-500' : 'text-gray-400');

</script>

<template>
    <Card class="flex flex-col justify-between">
        <CardHeader>Reasoning Engine</CardHeader>
        <CardContent class="space-y-2">
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Global Status</span>
                <span class="font-medium" :class="statusColor">{{ statusText }}</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Formalism</span>
                <span class="font-medium text-blue-400">{{ reasoningStore.activeFormalism }}</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Inferred Triples</span>
                <span class="font-medium text-gray-800 dark:text-gray-100">
                    {{ reasoningStore.isEnabled ? reasoningStore.inferredCount : '—' }}
                </span>
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
                    {{ reasoningStore.isEnabled ? 'Run Reasoning' : 'Enable Reasoning' }}
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
