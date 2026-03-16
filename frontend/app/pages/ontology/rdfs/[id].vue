<script setup lang="ts">
import KpiCard from '~/components/KpiCard.vue'
import { ChevronsUpDown } from 'lucide-vue-next'
import { useActiveOntologiesStore } from '~/store/active_ontology'

const config = useRuntimeConfig()
const id = useRoute().params.id

const activeOntologiesStore = useActiveOntologiesStore()
const isActive = ref<Boolean>(activeOntologiesStore.isActive(id))

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

const openStates = ref<Record<string, boolean>>({})
function toggleClass(uri: string) {
    openStates.value[uri] = !openStates.value[uri]
}

const search = ref('')

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

onMounted(async () => {
    await fetchToVisualise()
})


const filteredClasses = computed(() =>
    onto.value.classes.filter(c =>
        c.label?.toLowerCase().includes(search.value.toLowerCase()) ||
        c.prefix_form?.toLowerCase().includes(search.value.toLowerCase()) || 
        c.uri?.toLowerCase().includes(search.value.toLowerCase())
    )
)

function dataProps(properties: any[]) {
    return properties.filter(p => p.range?.startsWith('xsd:') || !p.range)
}
function objectProps(properties: any[]) {
    return properties.filter(p => p.range && !p.range.startsWith('xsd:'))
}
</script>

<template>
    <div class="p-2 space-y-6">

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

        <div class="grid grid-cols-3 gap-4">
            <KpiCard title="Classes"    :data="String(onto.class_count)"     />
            <KpiCard title="Properties" :data="String(onto.property_count)"  />
            <KpiCard title="Namespaces" :data="String(onto.namespace_count)" />
        </div>

        <!-- SEARCH + SECTION TITLE -->
        <div class="flex items-center justify-between ml-1">
            <p class="text-xl">Classes :</p>
            <input
                v-model="search"
                placeholder="Search classes..."
                class="text-sm border border-border rounded-lg px-3 py-1.5 w-56 bg-background focus:outline-none focus:ring-2 focus:ring-ring"
            />
        </div>

        <!-- CLASS LIST -->
        <div class="space-y-3">
            <Card
                v-for="cls in filteredClasses"
                :key="cls.uri"
            >
                <Collapsible
                    :open="openStates[cls.uri]"
                    @update:open="toggleClass(cls.uri)"
                    class="flex w-full flex-col gap-2"
                >
                    <!-- ROW HEADER -->
                    <CollapsibleTrigger as-child class="w-full cursor-pointer">
                        <CardHeader class="w-full hover:bg-muted/50 transition-colors rounded-t-xl">
                            <p class="flex w-full text-lg justify-between items-center">
                                <span class="flex items-center gap-3">
                                    <!-- colored dot -->
                                    <span class="w-2.5 h-2.5 rounded-full bg-blue-400 shrink-0"></span>
                                    {{ cls.prefix_form }}
                                    <span class="flex gap-2 text-muted-foreground font-normal">
                                        <span v-if="cls.parents.length">
                                            {{ cls.parents.length }} parent{{ cls.parents.length > 1 ? 's' : '' }}
                                            ,
                                        </span>
                                        <span v-if="cls.children.length">
                                             {{ cls.children.length }} child{{ cls.children.length > 1 ? 'ren' : '' }},
                                        </span>
                                        <span v-if="cls.properties.length">
                                            {{ cls.properties.length }} properties
                                        </span>
                                    </span>
                                </span>
                                <ChevronsUpDown class="w-4 h-4 text-muted-foreground" />
                            </p>
                        </CardHeader>
                    </CollapsibleTrigger>

                    <CollapsibleContent>
                        <CardContent class="flex flex-col gap-4 pt-0">
                            <Card class="p-4 flex flex-col gap-4">

                                <div v-if="cls.comment">
                                    <p class="text-lg text-foreground">Comment</p>
                                    <p class="text-sm text-muted-foreground mt-1 italic">{{ cls.comment }}</p>
                                </div>

                                <div class="grid grid-cols-2 gap-x-8 gap-y-2">
                                    <div class="flex gap-2">
                                        <span class="text-base w-24 shrink-0 text-muted-foreground">Parents :</span>
                                        <div class="flex flex-wrap gap-1">
                                            <Badge
                                                v-if="cls.parents.length"
                                                v-for="p in cls.parents" :key="p"
                                                variant="secondary"
                                            >{{ p }}</Badge>
                                            <span v-else class="text-sm text-muted-foreground">—</span>
                                        </div>
                                    </div>
                                    <div class="flex gap-2">
                                        <span class="text-base w-24 shrink-0 text-muted-foreground">Children :</span>
                                        <div class="flex flex-wrap gap-1">
                                            <Badge
                                                v-if="cls.children.length"
                                                v-for="c in cls.children" :key="c"
                                                variant="secondary"
                                            >{{ c }}</Badge>
                                            <span v-else class="text-sm text-muted-foreground">—</span>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="objectProps(cls.properties).length">
                                    <p class="text-lg text-foreground mb-2">Object Properties</p>
                                    <div class="space-y-1.5">
                                        <div
                                            v-for="p in objectProps(cls.properties)" :key="p.label"
                                            class="flex items-center gap-2 bg-secondary rounded-lg px-3 py-1.5"
                                        >
                                            <span class="text-chart-1 font-medium text-sm">{{ p.label }}</span>
                                            <span class="text-primary">→</span>
                                            <span class="text-sm text-foreground font-mono">{{ p.range ?? '—' }}</span>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="dataProps(cls.properties).length">
                                    <p class="text-lg text-foreground mb-2">Data Properties</p>
                                    <div class="space-y-1.5">
                                        <div
                                            v-for="p in dataProps(cls.properties)" :key="p.label"
                                            class="flex items-center gap-2 bg-secondary rounded-lg px-3 py-1.5"
                                        >
                                            <span class="text-chart-2 font-medium text-sm">{{ p.label }}</span>
                                            <span class="text-primary">→</span>
                                            <span class="text-sm font-mono text-muted-foreground">{{ p.range ?? 'xsd:string' }}</span>
                                        </div>
                                    </div>
                                </div>

                                <p v-if="!cls.properties.length" class="text-sm text-muted-foreground italic">
                                    No properties defined for this class.
                                </p>

                            </Card>
                        </CardContent>
                    </CollapsibleContent>
                </Collapsible>
            </Card>

            <Card v-if="filteredClasses.length === 0" class="py-12 text-center">
                <p class="text-3xl mb-2">🔍</p>
                <p class="text-sm text-muted-foreground">No classes match your search</p>
            </Card>
        </div>
    </div>
</template>