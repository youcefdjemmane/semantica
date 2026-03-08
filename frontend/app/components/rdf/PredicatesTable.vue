<script setup lang="ts">
import type { Predicate } from '~/types/rdf'  
defineProps<{
    predicates: Predicate[]
}>()

</script>

<template>
    <Table>
        <TableHeader>
            <TableRow>
                <TableHead>URI</TableHead>
                <TableHead>Prefix form</TableHead>
                <TableHead>Usage count</TableHead>
                <TableHead>Domain</TableHead>
                <TableHead>Range</TableHead>
            </TableRow>
        </TableHeader>
          <TableBody>
            <TableRow v-for="predicate in predicates" :key="predicate.id">
                <TableCell>{{ predicate.uri }}</TableCell>
                <TableCell>{{ predicate.prefix_form }}</TableCell>
                <TableCell>{{ predicate.usage_count }}</TableCell>
                <TableCell>{{ predicate.domain }}</TableCell>
                <TableCell>{{ predicate.range }}</TableCell>
            </TableRow>
          </TableBody>
    </Table>
</template>