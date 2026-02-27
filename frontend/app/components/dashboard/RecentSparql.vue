<script setup lang="ts">
import { Play } from 'lucide-vue-next';
import { mapQueryToVariant } from '~/types/badge_variant';

type QueryTYpe = "SELECT" | "CONSTRUCT" | "DESCRIBE" | "ASK"
interface Query {
    type: QueryTYpe,
    query: string
}

const queries : Query[] = [
    {
        type: 'SELECT',
        query: 'SELECT ?s ?p ?o WHERE...'
    },
    {
        type: 'ASK',
        query: 'ASK { ?x a :Person }'
    },
    {
        type: 'CONSTRUCT',
        query: 'CONSTRUCT { ?s ?p ?o }...'
    },

]


</script>

<template>
    <Card class=" flex flex-col justify-between ">
        <CardHeader>Recent SPARQL Queries</CardHeader>
        <CardContent class="space-y-2">
            <Table>
                <TableBody>
                    <TableRow v-for="query in queries" :key="query.query">
                        <TableCell>
                            <Badge :variant="mapQueryToVariant(query.type)">{{ query.type }}</Badge>
                        </TableCell>
                        <TableCell>
                            {{ query.query }}
                        </TableCell>
                        <TableCell class="flex justify-end ">
                            <Button variant="outline">
                                <Play/>
                                Run
                            </Button>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            
        </CardContent>
        <CardFooter class="flex items-center justify-end space-x-2">

            <NuxtLink to="/sparql">
                <Button variant="secondary">

                    Go to SPARQL Editor →
                </Button>
            </NuxtLink>


        </CardFooter>
    </Card>

</template>