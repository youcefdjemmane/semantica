<script setup lang="ts">
import { computed } from 'vue'
import { useActiveGraphStore } from '~/store/active_graph'
import { useActiveOntologiesStore } from '~/store/active_ontology'
import { useReasoningStore } from '~/store/reasoning'
import { ShieldCheck, ShieldAlert, Shield } from 'lucide-vue-next'

const activeGraphStore = useActiveGraphStore()
const activeOntologiesStore = useActiveOntologiesStore()
const reasoningStore = useReasoningStore()

const score = computed(() => {
    let s = 0
    if (activeGraphStore.id) s += 35
    
    const ontoCount = activeOntologiesStore.getOntologiesIds.length
    if (ontoCount === 1) s += 25
    else if (ontoCount > 1) s += 35

    if (reasoningStore.isEnabled) s += 20
    if (reasoningStore.inferredCount > 0) s += 10
    
    return s
})

const colorClass = computed(() => {
    if (score.value < 40) return 'text-destructive'
    if (score.value < 75) return 'text-amber-500'
    return 'text-green-500'
})

const barColor = computed(() => {
    if (score.value < 40) return 'bg-destructive'
    if (score.value < 75) return 'bg-amber-500'
    return 'bg-green-500'
})

const Icon = computed(() => {
    if (score.value < 40) return ShieldAlert
    if (score.value < 75) return Shield
    return ShieldCheck
})

</script>

<template>
    <Card class="flex flex-col justify-between h-full hover:shadow-md transition-shadow duration-300">
        <CardHeader class="pb-2">
            <CardTitle class="text-xs tracking-wider uppercase font-semibold text-muted-foreground flex items-center justify-between">
                Graph Health Core
                <component :is="Icon" class="w-4 h-4" :class="colorClass" />
            </CardTitle>
        </CardHeader>
        <CardContent>
            <div class="flex items-baseline gap-1.5 mb-3 mt-1">
                <span class="text-4xl font-extrabold tracking-tighter" :class="colorClass">{{ score }}</span>
                <span class="text-sm font-medium text-muted-foreground">/ 100</span>
            </div>
            
            <div class="h-2 w-full bg-secondary/60 rounded-full overflow-hidden mb-5">
                <div class="h-full rounded-full transition-all duration-1000 ease-out" 
                     :class="barColor" 
                     :style="{ width: `${score}%` }">
                </div>
            </div>

            <div class="space-y-2 mt-2">
                <div class="flex items-center justify-between text-xs">
                    <span class="text-muted-foreground font-medium">Graph Presence</span>
                    <span class="font-bold inline-block w-8 text-right">{{ activeGraphStore.id ? '35' : '0' }}</span>
                </div>
                <div class="flex items-center justify-between text-xs">
                    <span class="text-muted-foreground font-medium">Ontology Depth</span>
                    <span class="font-bold inline-block w-8 text-right">{{ activeOntologiesStore.getOntologiesIds.length > 1 ? '35' : (activeOntologiesStore.getOntologiesIds.length === 1 ? '25' : '0') }}</span>
                </div>
                <div class="flex items-center justify-between text-xs">
                    <span class="text-muted-foreground font-medium">Reasoning Engine</span>
                    <span class="font-bold inline-block w-8 text-right">{{ reasoningStore.isEnabled ? (reasoningStore.inferredCount > 0 ? '30' : '20') : '0' }}</span>
                </div>
            </div>
        </CardContent>
    </Card>
</template>
