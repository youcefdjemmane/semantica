<script setup lang="ts">
import { computed } from 'vue'
import { Sparkles, BrainCircuit, AlertCircle, Zap, Activity } from 'lucide-vue-next'
import { useActiveGraphStore } from '~/store/active_graph'
import { useActiveOntologiesStore } from '~/store/active_ontology'
import { useReasoningStore } from '~/store/reasoning'

const activeGraphStore = useActiveGraphStore()
const activeOntologiesStore = useActiveOntologiesStore()
const reasoningStore = useReasoningStore()

const insight = computed(() => {
    if (!activeGraphStore.id) {
        return {
            icon: Sparkles,
            title: 'Welcome to Semantica AI',
            description: 'Start by loading an RDF graph from the Data tab to analyze its semantic structure.',
            color: 'text-blue-500',
            bg: 'bg-blue-500/10'
        }
    }

    const ontologiesCount = activeOntologiesStore.getOntologiesIds.length

    if (ontologiesCount === 0) {
        return {
            icon: AlertCircle,
            title: 'Schema Missing',
            description: 'Your graph is loaded, but no ontologies are attached. Consider adding an OWL or RDFS ontology to provide structural meaning and schema definitions.',
            color: 'text-amber-500',
            bg: 'bg-amber-500/10'
        }
    }

    if (!reasoningStore.isEnabled) {
        return {
            icon: BrainCircuit,
            title: 'Unlock Hidden Knowledge',
            description: `You have ${ontologiesCount} ontologies linked. Enable the Reasoning Engine to discover implicit triples and hidden relationships based on your schema.`,
            color: 'text-purple-500',
            bg: 'bg-purple-500/10'
        }
    }

    if (reasoningStore.inferredCount === 0) {
        return {
            icon: Activity,
            title: 'Reasoning Active - No inferences',
            description: `The Engine is running ${reasoningStore.activeFormalism}, but yielded 0 inferences. Your graph might already be fully explicit, or the chosen formalism is too weak.`,
            color: 'text-indigo-500',
            bg: 'bg-indigo-500/10'
        }
    }

    return {
        icon: Zap,
        title: 'Knowledge Enriched',
        description: `Excellent! The Reasoning Engine successfully deduced ${reasoningStore.inferredCount} new facts using ${reasoningStore.activeFormalism}. Your overall knowledge graph is now semantically enriched.`,
        color: 'text-green-500',
        bg: 'bg-green-500/10'
    }
})

</script>

<template>
    <Card class="relative overflow-hidden bg-gradient-to-br from-card to-card/50 shadow-sm h-full group transition-all duration-300 hover:shadow-md border-primary/20">
        <div class="absolute right-0 top-0 w-48 h-48 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none group-hover:bg-primary/10 transition-colors duration-500"></div>
        <div class="absolute left-0 bottom-0 w-32 h-32 bg-secondary/5 rounded-full blur-2xl -ml-10 -mb-10 pointer-events-none"></div>
        
        <CardHeader class="pb-2">
            <div class="flex items-center gap-2">
                <Sparkles class="w-4 h-4 text-primary animate-pulse" />
                <CardTitle class="text-sm font-semibold tracking-wide flex items-center gap-2">
                    Semantica Copilot
                    <Badge variant="secondary" class="text-[10px] px-1.5 py-0 bg-primary/10 text-primary hover:bg-primary/20 transition-colors">AI</Badge>
                </CardTitle>
            </div>
        </CardHeader>
        <CardContent>
            <div class="flex items-start gap-4 mt-2">
                <div class="p-3 rounded-2xl shrink-0 transition-all duration-500 shadow-sm" :class="insight.bg">
                    <component :is="insight.icon" class="w-7 h-7 transition-colors duration-500" :class="insight.color" />
                </div>
                <div class="space-y-1.5 mt-0.5">
                    <h4 class="text-base font-semibold text-foreground tracking-tight">{{ insight.title }}</h4>
                    <p class="text-sm text-muted-foreground leading-relaxed pr-6 line-clamp-2">
                        {{ insight.description }}
                    </p>
                </div>
            </div>
        </CardContent>
        <div class="absolute bottom-0 left-0 w-full pt-0 pb-4 px-6 mt-4">
            <div class="flex items-center justify-between w-full mt-3">
                <span class="text-[11px] font-medium tracking-wide uppercase text-muted-foreground flex items-center gap-1.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                    Real-time analysis active
                </span>
                <NuxtLink v-if="insight.title === 'Schema Missing'" to="/ontology">
                    <Button variant="outline" size="sm" class="text-xs h-7 px-3">Go to Ontologies</Button>
                </NuxtLink>
                <NuxtLink v-else-if="!reasoningStore.isEnabled && activeGraphStore.id" to="/reasoning">
                    <Button variant="outline" size="sm" class="text-xs h-7 px-3">Configure Engine</Button>
                </NuxtLink>
            </div>
        </div>
    </Card>
</template>
