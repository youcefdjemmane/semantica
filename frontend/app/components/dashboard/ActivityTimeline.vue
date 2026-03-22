<script setup lang="ts">
import { Clock, FileText, Database, Brain } from 'lucide-vue-next';
import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { recentQueries, loadedFiles } = useDashboard();

interface ActivityItem {
  type: 'query' | 'file';
  label: string;
  sublabel: string;
  when: string;
  date: Date;
  icon: any;
  color: string;
}

const activities = computed((): ActivityItem[] => {
  const items: ActivityItem[] = [];

  // Recent SPARQL queries
  for (const q of recentQueries.value.slice(0, 4)) {
    items.push({
      type: 'query',
      label: `${q.query_type} query`,
      sublabel: q.query.substring(0, 45) + (q.query.length > 45 ? '...' : ''),
      when: formatDate(q.executed_at),
      date: new Date(q.executed_at),
      icon: Brain,
      color: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20',
    });
  }

  // Loaded files (last 4)
  for (const f of loadedFiles.value.slice(0, 4)) {
    items.push({
      type: 'file',
      label: `${f.type} loaded`,
      sublabel: f.name,
      when: f.uploaded,
      date: new Date(f.uploaded),
      icon: f.type === 'RDF' ? Database : FileText,
      color: f.type === 'RDF'
        ? 'text-orange-500 bg-orange-50 dark:bg-orange-900/20'
        : 'text-purple-500 bg-purple-50 dark:bg-purple-900/20',
    });
  }

  // Sort by date descending
  return items.sort((a, b) => b.date.getTime() - a.date.getTime()).slice(0, 6);
});

function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleString('fr-FR', { 
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
}
</script>

<template>
  <Card class="flex flex-col">
    <CardHeader class="flex flex-row items-center gap-2 pb-2">
      <Clock class="h-4 w-4 text-gray-400" />
      Activity Timeline
    </CardHeader>
    <CardContent class="flex-1">
      <div v-if="activities.length === 0" class="text-sm text-gray-400 text-center py-4">
        No activity yet. Load an RDF file or run a SPARQL query to get started.
      </div>
      <ol v-else class="relative border-l border-gray-200 dark:border-gray-700 space-y-3 ml-2">
        <li v-for="item in activities" :key="item.label + item.when" class="ml-4">
          <div :class="['absolute -left-1.5 mt-1 flex items-center justify-center w-3 h-3 rounded-full ring-2 ring-white dark:ring-gray-900', item.color]">
            <component :is="item.icon" class="h-2 w-2" />
          </div>
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center">
            <div class="min-w-0 pr-2">
              <p class="text-xs font-medium text-gray-700 dark:text-gray-200">{{ item.label }}</p>
              <p class="text-xs text-gray-400 truncate max-w-[150px]">{{ item.sublabel }}</p>
            </div>
            <span class="shrink-0 text-xs text-gray-400 mt-1 sm:mt-0 font-mono">{{ item.when }}</span>
          </div>
        </li>
      </ol>
    </CardContent>
  </Card>
</template>
