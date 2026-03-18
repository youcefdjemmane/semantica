<script setup lang="ts">
import { FileCode, FileSpreadsheet, FileJson } from 'lucide-vue-next';
import { useDashboard } from '~/composables/useDashboard';
import { useRuntimeConfig } from '#app';
import { computed } from 'vue';

const { recentQueries } = useDashboard();
const config = useRuntimeConfig();

const lastQuery = computed(() => recentQueries.value[0] ?? null);

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleString('fr-FR', { 
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
}

function exportResult(format: 'csv' | 'json' | 'xml') {
  if (!lastQuery.value) return;
  const apiBase = (config.public.apiBase as string) || 'http://localhost:8000/api/v1';
  // Note: GET /export requires graph_id, query, format
  const qStr = encodeURIComponent(lastQuery.value.query);
  const gId = lastQuery.value.graph_id;
  const url = `${apiBase}/sparql/export?graph_id=${gId}&query=${qStr}&format=${format}`;
  
  // Ouvre le lien dans un nouvel onglet, ce qui déclenche le téléchargement du fichier généré par FileResponse
  window.open(url, '_blank');
}
</script>

<template>
    <Card class="flex flex-col justify-between">
        <CardHeader>Last Query Export</CardHeader>
        <CardContent class="space-y-2 mb-4">
            <template v-if="lastQuery">
                <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Last Query</span>
                    <span class="text-gray-800 dark:text-gray-100 font-medium whitespace-nowrap overflow-hidden text-ellipsis max-w-[120px]">{{ lastQuery.query_type }}</span>
                </div>
                <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Executed</span>
                    <span class="text-gray-400">{{ formatDate(lastQuery.executed_at) }}</span>
                </div>
            </template>
            <div v-else class="text-sm text-gray-400 text-center py-4">
                No queries executed yet.
            </div>
        </CardContent>
        <CardFooter class="flex justify-end gap-2">
            <Button size="sm" variant="outline" :disabled="!lastQuery" @click="exportResult('csv')">
                <FileSpreadsheet class="h-4 w-4 mr-2" />
                 CSV
            </Button>
            <Button size="sm" variant="outline" :disabled="!lastQuery" @click="exportResult('json')">
                <FileJson class="h-4 w-4 mr-2" />
                 JSON
            </Button>
            <Button size="sm" variant="outline" :disabled="!lastQuery" @click="exportResult('xml')">
                <FileCode class="h-4 w-4 mr-2" />
                 XML
            </Button>
        </CardFooter>
    </Card>
</template>
