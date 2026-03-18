<script setup lang="ts">
import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';
import { ArrowRight } from 'lucide-vue-next';

const { ontologyStats } = useDashboard();

const classes     = computed(() => ontologyStats.value?.total_classes     ?? '—');
const properties  = computed(() => ontologyStats.value?.total_properties  ?? '—');
const individuals = computed(() => ontologyStats.value?.total_individuals ?? '—');
const owl         = computed(() => ontologyStats.value?.owl_count         ?? '—');
const rdfs        = computed(() => ontologyStats.value?.rdfs_count        ?? '—');
const total       = computed(() => ontologyStats.value?.total_ontologies  ?? '—');
</script>

<template>
     <Card class="flex flex-col justify-between">
                <CardHeader>Ontology Overview</CardHeader>
                <CardContent class="space-y-2">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Total Ontologies</span>
                        <span class="font-semibold text-gray-800 dark:text-gray-100">{{ total }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Classes</span>
                        <span class="font-medium text-gray-800 dark:text-gray-100">{{ classes }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Properties</span>
                        <span class="font-medium text-gray-800 dark:text-gray-100">{{ properties }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Individuals</span>
                        <span class="font-medium text-gray-800 dark:text-gray-100">{{ individuals }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">OWL / RDFS</span>
                        <span class="font-medium text-gray-800 dark:text-gray-100">
                            <Badge variant="secondary" class="mr-1">OWL {{ owl }}</Badge>
                            <Badge variant="outline">RDFS {{ rdfs }}</Badge>
                        </span>
                    </div>
                </CardContent>
                <CardFooter  class="flex items-center justify-end space-x-2">                    
                    <NuxtLink to="/ontology">
                        <Button variant="secondary">
                            <ArrowRight/>
                            View Hierarchy 
                        </Button>
                    </NuxtLink>
                </CardFooter>
            </Card>
</template>