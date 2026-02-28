<script setup lang="ts">
import { useRoute } from 'vue-router'
import KpiCard from '~/components/KpiCard.vue'
const route = useRoute()
definePageMeta({
    title: "Ontology details",
})
const isActive = ref(false)
function toggleActive()  {
    isActive.value = !isActive.value
    console.log(isActive.value);   
}
</script>

<template>
    <div class="p-6 space-y-6">
        <Card class="flex flex-row px-5  justify-between items-center">
                <CardTitle>
                    Ontology name (file.owl)
                </CardTitle>
                <Badge v-if="isActive" variant="rdf">
                    Active
                </Badge>
                <Button v-else v-on:click="toggleActive()">
                    Set as active
                </Button>
        </Card>
         <div class="grid grid-cols-5 gap-4">
            <KpiCard title="Classes" data="20" />
            <KpiCard title="Object Properties" data="20" />
            <KpiCard title="Data Properties" data="20" />
            <KpiCard title="Annotations" data="20" />
            <KpiCard title="Individuals" data="20" />
         </div>
    </div>
</template>