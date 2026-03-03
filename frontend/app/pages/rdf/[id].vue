<script setup lang="ts">
import { Waypoints } from 'lucide-vue-next'
import { useRoute } from 'vue-router'
import KpiCard from '~/components/KpiCard.vue'
import ObjectsTable from '~/components/rdf/ObjectsTable.vue'
import PredicatesTable from '~/components/rdf/PredicatesTable.vue'
import SubjectsTable from '~/components/rdf/SubjectsTable.vue'
const route = useRoute()
definePageMeta({
    title: "Graph details",
})
const isActive = ref(false)
function toggleActive() {
    isActive.value = !isActive.value
    console.log(isActive.value);
}
</script>

<template>
    <div class="p-2 space-y-6">
        <Card class="flex flex-row px-5  justify-between items-center">
            <CardTitle>
                Graph name (file.ttl)
            </CardTitle>
            <div class="space-x-2 flex items-center">
                <Button size="sm" variant="outline">
                    <Waypoints/>
                    Visualise
                </Button>
                <Button size="sm" v-on:click="toggleActive()">
                    {{ isActive ? 'Set as Inactive' : 'Set as Active' }}
                </Button>
                <Badge v-if="isActive" variant="active">
                    Active
                </Badge>
                <Badge v-else variant="inactive">
                    Inactive
                </Badge>
            </div>
        </Card>
        <div class="grid grid-cols-3 gap-4">
            <KpiCard title="Subjects" data="20" />
            <KpiCard title="Predicates" data="20" />

            <KpiCard title="Objects" data="20" />

        </div>
        <div class="flex w-full flex-col  gap-6">
            <Tabs default-value="subjects">
                <TabsList>
                    <TabsTrigger value="subjects">
                        Subjects
                    </TabsTrigger>
                    <TabsTrigger value="predicates">
                        Predicates
                    </TabsTrigger>
                    <TabsTrigger value="objects">
                        Objects
                    </TabsTrigger>
                </TabsList>
                <TabsContent value="subjects">
                    <SubjectsTable/>
                </TabsContent>
                <TabsContent value="predicates">
                    <PredicatesTable />
                </TabsContent>
                <TabsContent value="objects">
                    <ObjectsTable/>
                </TabsContent>
            </Tabs>
        </div>
    </div>
</template>