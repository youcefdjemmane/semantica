<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue'
import type { Ontology, OntologyFileStats } from '~/types/ontology'
import cytoscape from 'cytoscape'
import { useActiveOntologiesStore } from '~/store/active_ontology'

const config = useRuntimeConfig()
const id = useRoute().params.id

const stats = ref<OntologyFileStats>({
    id: '', name: '', format: '', file_size: 0,
    classes_count: 0, properties_count: 0, individuals_count: 0, uploaded_at: '',
})

async function fetchStats() {
    try {
        const { data, error } = await useFetch<OntologyFileStats>(
            `${config.public.apiBase}/ontology/${id}/stats`
        )
        if (!error.value && data.value) stats.value = data.value
    } catch (e) { console.error(e) }
}

const onto = ref<Ontology>({
    id: "4c69459c-326c-4118-bec4-7042e2934762",
    name: "filename",
    format: "owl",
    class_count: 5,
    object_property_count: 0,
    data_property_count: 0,
    individual_count: 0,
    nodes: [],
    edges: []
})


async function fetchToVisualise() {
    try {
        const { data, error } = await useFetch<Ontology>(
            `${config.public.apiBase}/ontology/${id}/owl`
        )
        if (!error.value && data.value) onto.value = data.value
    } catch (e) { console.error(e) }
}
const activeOntologiesStore = useActiveOntologiesStore()

const isActive = ref<Boolean>(
    activeOntologiesStore.isActive(id)
)


function toggleActive() { 
    if (isActive.value) {
        activeOntologiesStore.removeOntology(id);
        isActive.value = false
    }else{
        activeOntologiesStore.addOntology({
            id: stats.value.id,
            name: stats.value.name,
            format: stats.value.format
        })
        isActive.value = true
    }

}


const selectedNode = ref<any>(null)

const graphContainer = ref<HTMLElement | null>(null)
let cy: any = null

const NODE_COLORS: Record<string, string> = {
    root: '#6366f1',
    class: '#818cf8',
}
const EDGE_COLORS: Record<string, string> = {
    subClassOf: '#6366f1',
    disjointWith: '#f43f5e',
    equivalentClass: '#10b981',
}

function initCytoscape() {
    if (!graphContainer.value) return

    const elements = [
        ...onto.value.nodes.map(n => ({
            data: { id: n.id, label: n.label, nodeData: n },
        })),
        ...onto.value.edges.map((e, i) => ({
            data: {
                id: `e${i}`,
                source: e.source,
                target: e.target,
                edgeType: e.type,
            },
        })),
    ]

    cy = cytoscape({
        container: graphContainer.value,
        elements,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': (ele: any) =>
                        NODE_COLORS[ele.data('nodeData').type] ?? '#818cf8',
                    'label': 'data(label)',
                    'color': '#e2e8f0',
                    'font-size': '11px',
                    'font-family': 'ui-monospace, monospace',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 'label',
                    'height': 'label',
                    'padding': '10px',
                    'shape': 'roundrectangle',
                    'border-width': 2,
                    'border-color': '#4f46e5',
                    'text-wrap': 'wrap',
                    'text-max-width': '120px',
                    'transition-property': 'background-color, border-color, border-width',
                    'transition-duration': '150ms',
                } as any,
            },
            {
                selector: 'node:selected, node.highlighted',
                style: {
                    'background-color': '#4f46e5',
                    'border-color': '#a5b4fc',
                    'border-width': 3,
                } as any,
            },
            {
                selector: 'node[?nodeData.type = "root"]',
                style: {
                    'background-color': '#312e81',
                    'border-color': '#6366f1',
                } as any,
            },
            {
                selector: 'edge',
                style: {
                    'width': 1.5,
                    'line-color': (ele: any) => EDGE_COLORS[ele.data('edgeType')] ?? '#6366f1',
                    'target-arrow-color': (ele: any) => EDGE_COLORS[ele.data('edgeType')] ?? '#6366f1',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.7,
                    'label': 'data(edgeType)',
                    'font-size': '9px',
                    'color': '#94a3b8',
                    'text-rotation': 'autorotate',
                    'font-family': 'ui-monospace, monospace',
                } as any,
            },
            {
                selector: 'edge[edgeType = "disjointWith"]',
                style: {
                    'line-style': 'dashed',
                    'line-dash-pattern': [4, 4],
                } as any,
            },
            {
                selector: 'edge[edgeType = "equivalentClass"]',
                style: {
                    'line-style': 'dotted',
                    'target-arrow-shape': 'none',
                    'source-arrow-shape': 'none',
                } as any,
            },
        ],
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 40,
            spacingFactor: 1.6,
            roots: ['owl:Thing'],
        } as any,
        userZoomingEnabled: true,
        userPanningEnabled: true,
        boxSelectionEnabled: false,
    })

    cy.on('tap', 'node', (evt: any) => {
        const node = evt.target
        cy.nodes().removeClass('highlighted')
        node.addClass('highlighted')
        // highlight connected edges
        node.connectedEdges().style({ opacity: 1 })
        cy.edges().not(node.connectedEdges()).style({ opacity: 0.2 })
        selectedNode.value = node.data('nodeData')
    })

    cy.on('tap', (evt: any) => {
        if (evt.target === cy) {
            cy.nodes().removeClass('highlighted')
            cy.edges().style({ opacity: 0.7 })
            selectedNode.value = null
        }
    })
}

function fitGraph() { cy?.fit(undefined, 40) }
function resetLayout() {
    cy?.layout({
        name: 'breadthfirst', directed: true, padding: 40,
        spacingFactor: 1.6, roots: ['owl:Thing'],
    } as any).run()
    cy?.fit(undefined, 40)
}

function restrictionLabel(r: any): string {
    if (r.exact_cardinality !== null) return `exactly ${r.exact_cardinality}`
    const parts = []
    if (r.min_cardinality !== null) parts.push(`min ${r.min_cardinality}`)
    if (r.max_cardinality !== null) parts.push(`max ${r.max_cardinality}`)
    if (r.some_values_from) parts.push(`some values from ${r.some_values_from}`)
    if (r.all_values_from) parts.push(`all values from ${r.all_values_from}`)
    return parts.join(', ') || '—'
}

onMounted(async () => {
    await fetchToVisualise()
    await fetchStats()
    await nextTick()
    initCytoscape()
})

onBeforeUnmount(() => { cy?.destroy() })


</script>

<template>
    <div class="p-2 space-y-6">

        <!-- Header -->
        <Card class="flex flex-row px-5 justify-between items-center">
            <div class="flex flex-col gap-0.5">
                <CardTitle>{{ onto.name }}</CardTitle>
                <p class="text-sm text-muted-foreground">OWL Ontology</p>
            </div>
            <div class="space-x-2 flex items-center">
                <Button size="sm" @click="toggleActive()">
                    {{ isActive ? 'Set as Inactive' : 'Set as Active' }}
                </Button>
                <Badge v-if="isActive" variant="active">Active</Badge>
                <Badge v-else variant="inactive">Inactive</Badge>
            </div>
        </Card>

        <!-- KPIs -->
        <div class="grid grid-cols-3 gap-4">
            <KpiCard title="Classes" :data="stats.classes_count ?? 0" />
            <KpiCard title="Properties" :data="stats.properties_count ?? 0" />
            <KpiCard title="Individuals" :data="stats.individuals_count ?? 0" />
        </div>

        <!-- Graph section -->
        <div class="flex items-center justify-between ml-1">
            <p class="text-xl">Class Hierarchy</p>
            <div class="flex gap-2">
                <!-- Legend -->
                <div class="flex items-center gap-3 text-xs text-muted-foreground mr-2">
                    <span class="flex items-center gap-1">
                        <span class="w-4 h-0.5 bg-indigo-500 inline-block"></span> subClassOf
                    </span>
                    <span class="flex items-center gap-1">
                        <span class="w-4 h-0.5 bg-rose-500 border-dashed border-b border-rose-500 inline-block"></span>
                        disjointWith
                    </span>
                    <span class="flex items-center gap-1">
                        <span class="w-4 h-0.5 bg-emerald-500 inline-block"></span> equivalentClass
                    </span>
                </div>
                <Button size="sm" variant="outline" @click="fitGraph">Fit</Button>
                <Button size="sm" variant="outline" @click="resetLayout">Reset Layout</Button>
            </div>
        </div>

        <!-- Graph + Detail panel -->
        <div class="flex gap-4 items-start">

            <!-- Cytoscape canvas -->
            <Card class="flex-1 overflow-hidden" style="height: 520px;">
                <div ref="graphContainer" class="w-full h-full" />
            </Card>

            <!-- Detail panel -->
            <div class="w-80 shrink-0 transition-all duration-200">
                <Card v-if="selectedNode" class="p-4 flex flex-col gap-4">

                    <div class="flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-indigo-400 shrink-0"></span>
                        <p class="font-semibold text-base leading-tight">{{ selectedNode.id }}</p>
                    </div>

                    <p v-if="selectedNode.comment" class="text-sm text-muted-foreground italic -mt-2">
                        {{ selectedNode.comment }}
                    </p>

                    <div class="space-y-3">
                        <div v-if="selectedNode.equivalent_classes?.length" class="flex flex-col gap-1">
                            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Equivalent</p>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="e in selectedNode.equivalent_classes" :key="e" variant="outline">{{ e }}
                                </Badge>
                            </div>
                        </div>

                        <div v-if="selectedNode.disjoint_classes?.length" class="flex flex-col gap-1">
                            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Disjoint</p>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="d in selectedNode.disjoint_classes" :key="d" variant="destructive">{{ d }}
                                </Badge>
                            </div>
                        </div>

                        <div v-if="selectedNode.union_of?.length" class="flex flex-col gap-1">
                            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Union of</p>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="u in selectedNode.union_of" :key="u" variant="secondary">{{ u }}</Badge>
                            </div>
                        </div>

                        <div v-if="selectedNode.intersection_of?.length" class="flex flex-col gap-1">
                            <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Intersection of
                            </p>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="i in selectedNode.intersection_of" :key="i" variant="secondary">{{ i }}
                                </Badge>
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedNode.object_properties?.length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">Object
                            Properties</p>
                        <div class="space-y-1">
                            <div v-for="p in selectedNode.object_properties" :key="p.label"
                                class="flex items-center gap-2 bg-secondary rounded-md px-2.5 py-1">
                                <span class="text-chart-1 font-medium text-xs">{{ p.label }}</span>
                                <span class="text-primary text-xs">→</span>
                                <span class="text-xs font-mono">{{ p.range ?? '—' }}</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedNode.data_properties?.length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">Data
                            Properties</p>
                        <div class="space-y-1">
                            <div v-for="p in selectedNode.data_properties" :key="p.label"
                                class="flex items-center gap-2 bg-secondary rounded-md px-2.5 py-1">
                                <span class="text-chart-2 font-medium text-xs">{{ p.label }}</span>
                                <span class="text-primary text-xs">→</span>
                                <span class="text-xs font-mono text-muted-foreground">{{ p.range ?? 'xsd:string'
                                    }}</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedNode.restrictions?.length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">Restrictions
                        </p>
                        <div class="space-y-1">
                            <div v-for="(r, i) in selectedNode.restrictions" :key="i"
                                class="flex items-center gap-2 bg-secondary rounded-md px-2.5 py-1">
                                <span class="text-chart-4 font-medium text-xs">{{ r.property }}</span>
                                <span class="text-primary text-xs">·</span>
                                <span class="text-xs text-muted-foreground">{{ restrictionLabel(r) }}</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="selectedNode.individuals?.length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">
                            Individuals
                            <span class="normal-case font-normal">({{ selectedNode.individual_count }})</span>
                        </p>
                        <div class="flex flex-wrap gap-1">
                            <Badge v-for="ind in selectedNode.individuals" :key="ind.uri" variant="secondary">
                                {{ ind.label }}
                            </Badge>
                        </div>
                    </div>

                    <p v-if="!selectedNode.object_properties?.length && !selectedNode.data_properties?.length
                        && !selectedNode.restrictions?.length && !selectedNode.individuals?.length
                        && !selectedNode.equivalent_classes?.length && !selectedNode.disjoint_classes?.length"
                        class="text-xs text-muted-foreground italic">
                        No additional details for this class.
                    </p>
                </Card>

                <!-- Empty state -->
                <Card v-else class="p-6 text-center flex flex-col items-center gap-2 border-dashed">
                    <p class="text-2xl">🔍</p>
                    <p class="text-sm text-muted-foreground">Click a node to inspect its details</p>
                </Card>
            </div>
        </div>

    </div>
</template>