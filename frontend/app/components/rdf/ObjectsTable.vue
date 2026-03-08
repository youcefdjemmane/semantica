<script setup lang="ts">
import type { Object } from '~/types/rdf';


defineProps<{
    objects: Object[]
}>()
</script>

<template>
    
    <Table >
        <TableHeader>
            <TableRow>
                <TableHead>Kind</TableHead>
                <TableHead>Value</TableHead>
                <TableHead>Prefix form</TableHead>
                <TableHead>language</TableHead>
                <TableHead>DataType</TableHead>
            </TableRow>
        </TableHeader>
          <TableBody>
            <TableRow v-for="obj in objects" :key="obj.id">
                <TableCell>{{ obj.kind }}</TableCell>
                <TableCell>{{ obj.value }}</TableCell>
                <TableCell>{{ obj.prefix_form }}</TableCell>
                <TableCell>{{ obj.language }}</TableCell>
                <TableCell>{{ obj.datatype }}</TableCell>
            </TableRow>
          </TableBody>
    </Table>
</template>