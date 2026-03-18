<script setup lang="ts">
import type { LoadedFile } from '~/types/loaded_files';
import { useDashboard } from '~/composables/useDashboard';
import { useRouter } from 'vue-router';

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'
import { CirclePlus, DiamondPlus, Eye, Trash, Loader2 } from 'lucide-vue-next';

defineProps<{
    data: Array<LoadedFile>
}>()

const { deleteFile, isLoading } = useDashboard();
const router = useRouter();

function viewFile(file: LoadedFile) {
    if (file.type === 'RDF') {
        router.push(`/rdf/${file.id}`);
    } else {
        router.push(`/ontology/${file.id}`);
    }
}
</script>

<template>
    <div class="rounded-xl p-4 shadow-sm border">
        <div class="flex items-center justify-between mb-3">
            <p class="text-sm font-semibold text-gray-700 dark:text-gray-100">
                Loaded Files
                <Badge v-if="data.length > 0" variant="secondary" class="ml-2">{{ data.length }}</Badge>
            </p>
            <div class="flex gap-2">
                <NuxtLink to="/rdf">
                    <Button>
                        <CirclePlus/>
                        Load RDF
                    </Button>
                </NuxtLink>
                <NuxtLink to="/ontology">
                    <Button variant="outline">
                        <DiamondPlus />
                        Load Ontology
                    </Button>
                </NuxtLink>
            </div>
        </div>
        
        <!-- Empty state -->
        <div v-if="data.length === 0 && !isLoading" class="text-center py-8 text-gray-400 text-sm">
            No files loaded yet. Upload an RDF graph or ontology to get started.
        </div>

        <!-- Loading state -->
        <div v-else-if="isLoading && data.length === 0" class="text-center py-8">
            <Loader2 class="h-5 w-5 animate-spin mx-auto text-gray-400" />
        </div>

        <Table v-else>
            <TableCaption>{{ data.length }} file(s) loaded.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Format</TableHead>
                    <TableHead>Triples</TableHead>
                    <TableHead>Uploaded</TableHead>
                    <TableHead class="text-right">Actions</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                <TableRow v-for="file in data" :key="file.id || file.name">
                    <TableCell class="font-medium">
                        {{ file.name }}
                    </TableCell>
                    <TableCell>
                        <Badge :variant="file.type == 'RDF' ? 'rdf' : 'ontology'">
                            {{ file.type }}
                        </Badge>
                    </TableCell>
                    <TableCell>{{ file.format }}</TableCell>
                    <TableCell>{{ file.triples }}</TableCell>
                    <TableCell>{{ file.uploaded }}</TableCell>
                    <TableCell>
                        <div class="flex items-center space-x-2 justify-end">
                            <Button variant="secondary" @click="viewFile(file)">
                                <Eye/>
                                Show
                            </Button>
                            <Button variant="destructive" @click="deleteFile(file.id, file.type)">
                                <Trash/>
                                Delete
                            </Button>
                        </div>
                    </TableCell>
                </TableRow>
            </TableBody>
        </Table>
    </div>
</template>
