<script setup lang="ts">
import { Play, Clock } from 'lucide-vue-next';
import { mapQueryToVariant } from '~/types/badge_variant';
import { useDashboard } from '~/composables/useDashboard';

const { recentQueries } = useDashboard();
const router = useRouter();

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleString('fr-FR', { 
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
}

function truncateQuery(q: string): string {
  return q.length > 50 ? q.substring(0, 50) + '...' : q;
}

function rerunQuery(query: string) {
  // Navigate to SPARQL editor with pre-filled query via query param
  router.push({ path: '/sparql', query: { q: query } });
}
</script>

<template>
    <Card class="flex flex-col justify-between">
        <CardHeader>Recent SPARQL Queries</CardHeader>
        <CardContent class="space-y-2">
            <Table v-if="recentQueries.length > 0">
                <TableBody>
                    <TableRow v-for="query in recentQueries.slice(0, 5)" :key="query.id">
                        <TableCell>
                            <Badge :variant="mapQueryToVariant(query.query_type as any)">{{ query.query_type }}</Badge>
                        </TableCell>
                        <TableCell class="text-xs font-mono text-gray-600 dark:text-gray-300 max-w-[200px] xl:max-w-[400px] truncate">
                            {{ truncateQuery(query.query) }}
                        </TableCell>
                        <TableCell class="text-xs text-gray-400 whitespace-nowrap">
                            <Clock class="inline h-3 w-3 mr-1" />
                            {{ formatDate(query.executed_at) }}
                        </TableCell>
                        <TableCell class="flex justify-end">
                            <Button variant="outline" size="sm" @click="rerunQuery(query.query)">
                                <Play class="h-3 w-3" />
                                Run
                            </Button>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            <div v-else class="text-sm text-gray-400 text-center py-4">
                No SPARQL queries executed yet.
            </div>
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
