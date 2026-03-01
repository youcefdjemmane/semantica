<script setup lang="ts">
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
                <!-- Object/ data -->
                <TableHead>Type</TableHead>
            </TableRow>
        </TableHeader>
          <TableBody>
            <TableRow>
                <TableCell>http://xmlns.com/foaf/0.1/knows</TableCell>
                <TableCell>foaf:knows</TableCell>
                <TableCell>34</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>Object Property</TableCell>
            </TableRow>
            <TableRow>
                <TableCell>http://xmlns.com/foaf/0.1/knows</TableCell>
                <TableCell>foaf:knows</TableCell>
                <TableCell>34</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>Data Property</TableCell>
            </TableRow>
            <TableRow>
                <TableCell>http://xmlns.com/foaf/0.1/knows</TableCell>
                <TableCell>foaf:knows</TableCell>
                <TableCell>34</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>foaf:Person</TableCell>
                <TableCell>Object Property</TableCell>
            </TableRow>
          </TableBody>
    </Table>
</template>