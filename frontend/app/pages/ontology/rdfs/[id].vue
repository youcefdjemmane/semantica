<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue'
import cytoscape from 'cytoscape'
import { useActiveOntologiesStore } from '~/store/active_ontology'

const config = useRuntimeConfig()
const id = useRoute().params.id

const activeOntologiesStore = useActiveOntologiesStore()
const isActive = ref<Boolean>(activeOntologiesStore.isActive(id))

const onto = ref({
    id: '',
    name: 'Loading...',
    format: 'rdfs',
    class_count: 0,
    property_count: 0,
    namespace_count: 0,
    classes: [] as any[]
})

async function fetchToVisualise() {
    try {
        const data: any = await $fetch(
            `${config.public.apiBase}/ontology/${id}/rdfs`
        )
        if (data) onto.value = data
    } catch (e) { console.error(e) }
}

function toggleActive() { 
    if (isActive.value) {
        activeOntologiesStore.removeOntology(id);
        isActive.value = false
    }else{
        activeOntologiesStore.addOntology({
            id: onto.value.id,
            name: onto.value.name,
            format: onto.value.format
        })
        isActive.value = true
    }
}

function dataProps(properties: any[]) {
    return (properties || []).filter(p => p.range?.startsWith('xsd:') || !p.range)
}
function objectProps(properties: any[]) {
    return (properties || []).filter(p => p.range && !p.range.startsWith('xsd:'))
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
}

function initCytoscape() {
    if (!graphContainer.value) return

    const nodes: any[] = []
    const edges: any[] = []
    const nodeIds = new Set<string>()

    onto.value.classes.forEach(c => {
        const nodeId = c.prefix_form || c.uri
        nodes.push({
            data: { id: nodeId, label: c.label || nodeId, nodeData: { ...c, id: nodeId, type: 'class' } }
        })
        nodeIds.add(nodeId)
    })

    onto.value.classes.forEach(c => {
        const sourceId = c.prefix_form || c.uri
        if(c.parents && c.parents.length > 0) {
            c.parents.forEach((p: string) => {
                const targetId = p;
                if (!nodeIds.has(targetId)) {
                    nodes.push({
                        data: { id: targetId, label: targetId, nodeData: { id: targetId, label: targetId, type: 'root', properties: [] } }
                    })
                    nodeIds.add(targetId)
                }
                edges.push({
                    data: {
                        id: `${sourceId}-${targetId}`,
                        source: sourceId,
                        target: targetId,
                        edgeType: 'subClassOf'
                    }
                })
            })
        }
    })

    const elements = [...nodes, ...edges]

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
            }
        ],
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 40,
            spacingFactor: 1.6,
        } as any,
        userZoomingEnabled: true,
        userPanningEnabled: true,
        boxSelectionEnabled: false,
    })

    cy.on('tap', 'node', (evt: any) => {
        const node = evt.target
        cy.nodes().removeClass('highlighted')
        node.addClass('highlighted')
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
        spacingFactor: 1.6,
    } as any).run()
    cy?.fit(undefined, 40)
}

onMounted(async () => {
    await fetchToVisualise()
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
                <p class="text-sm text-muted-foreground">RDFS Ontology</p>
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
            <KpiCard title="Classes"    :data="String(onto.class_count)"     />
            <KpiCard title="Properties" :data="String(onto.property_count)"  />
            <KpiCard title="Namespaces" :data="String(onto.namespace_count)" />
        </div>

        <div class="flex items-center justify-between ml-1">
            <p class="text-xl">Class Hierarchy</p>
            <div class="flex gap-2">
                <div class="flex items-center gap-3 text-xs text-muted-foreground mr-2">
                    <span class="flex items-center gap-1">
                        <span class="w-4 h-0.5 bg-indigo-500 inline-block"></span> subClassOf
                    </span>
                </div>
                <Button size="sm" variant="outline" @click="fitGraph">Fit</Button>
                <Button size="sm" variant="outline" @click="resetLayout">Reset Layout</Button>
            </div>
        </div>

        <div class="flex gap-4 items-start">

            <Card class="flex-1 overflow-hidden" style="height: 520px;">
                <div ref="graphContainer" class="w-full h-full" />
            </Card>

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
                        <div v-if="selectedNode.parents?.length" class="flex gap-2 items-center">
                            <span class="text-xs w-16 shrink-0 font-medium text-muted-foreground uppercase">Parents:</span>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="p in selectedNode.parents" :key="p" variant="secondary">{{ p }}</Badge>
                            </div>
                        </div>

                        <div v-if="selectedNode.children?.length" class="flex gap-2 items-center">
                            <span class="text-xs w-16 shrink-0 font-medium text-muted-foreground uppercase">Children:</span>
                            <div class="flex flex-wrap gap-1">
                                <Badge v-for="c in selectedNode.children" :key="c" variant="secondary">{{ c }}</Badge>
                            </div>
                        </div>
                    </div>

                    <div v-if="objectProps(selectedNode.properties).length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">Object Properties</p>
                        <div class="space-y-1">
                            <div v-for="p in objectProps(selectedNode.properties)" :key="p.label"
                                class="flex items-center gap-2 bg-secondary rounded-md px-2.5 py-1">
                                <span class="text-chart-1 font-medium text-xs">{{ p.label }}</span>
                                <span class="text-primary text-xs">→</span>
                                <span class="text-xs font-mono">{{ p.range ?? '—' }}</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="dataProps(selectedNode.properties).length">
                        <p class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">Data Properties</p>
                        <div class="space-y-1">
                            <div v-for="p in dataProps(selectedNode.properties)" :key="p.label"
                                class="flex items-center gap-2 bg-secondary rounded-md px-2.5 py-1">
                                <span class="text-chart-2 font-medium text-xs">{{ p.label }}</span>
                                <span class="text-primary text-xs">→</span>
                                <span class="text-xs font-mono text-muted-foreground">{{ p.range ?? 'xsd:string' }}</span>
                            </div>
                        </div>
                    </div>

                    <p v-if="!(selectedNode.properties?.length) && !(selectedNode.parents?.length) && !(selectedNode.children?.length)"
                        class="text-xs text-muted-foreground italic">
                        No additional details for this class.
                    </p>
                </Card>

                <Card v-else class="p-6 text-center flex flex-col items-center gap-2 border-dashed">
                    <p class="text-2xl">🔍</p>
                    <p class="text-sm text-muted-foreground">Click a node to inspect its details</p>
                </Card>
            </div>
        </div>

    </div>
</template>