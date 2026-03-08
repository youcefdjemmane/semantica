<script setup lang="ts">
import type { Subject } from '~/types/rdf'

defineProps<{
    subjects: Subject[]
}>()
</script>

<template>

    <Table>
        <TableHeader>
            <TableRow>
                <TableHead>URI</TableHead>
                <TableHead>Prefix form</TableHead>
                <TableHead>Rdf Type</TableHead>
                <TableHead>Predicates count</TableHead>
            </TableRow>
        </TableHeader>
          <TableBody>
            <TableRow v-for="subject in subjects" :key="subject.id">
                <TableCell>{{ subject.uri }}</TableCell>
                <TableCell>{{ subject.prefix_form }}</TableCell>
                <TableCell>{{ subject.rdf_type }}</TableCell>
                <TableCell>{{ subject.predicate_count }}</TableCell>
            </TableRow>
            
          </TableBody>
    </Table>
</template>