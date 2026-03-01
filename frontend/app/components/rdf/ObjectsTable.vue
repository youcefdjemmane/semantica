<script setup lang="ts">
</script>

<template>
    
    <Table>
        <TableHeader>
            <TableRow>
                <TableHead>Value</TableHead>
                <TableHead>Kind</TableHead>
                <TableHead>Datatype</TableHead>
                <TableHead>Language tag</TableHead>
            </TableRow>
        </TableHeader>
          <TableBody>
            <TableRow>
                <TableCell>foaf:John</TableCell>
                <TableCell>URI</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
            </TableRow>
             <TableRow>
                <TableCell>John Doe</TableCell>
                <TableCell>Litteral</TableCell>
                <TableCell>xsd:string</TableCell>
                <TableCell>@en</TableCell>
            </TableRow>
          </TableBody>
    </Table>
</template>