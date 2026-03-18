<script setup lang="ts">
import { BarChart3, ChevronRight } from 'lucide-vue-next';
import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { sparqlStats } = useDashboard();

const total = computed(() => sparqlStats.value?.total_queries ?? 0);
const byType = computed(() => sparqlStats.value?.by_type ?? {});
const lastQuery = computed(() => sparqlStats.value?.last_query ?? null);

const typeColors: Record<string, string> = {
  SELECT:    'bg-blue-500',
  ASK:       'bg-green-500',
  CONSTRUCT: 'bg-orange-500',
  DESCRIBE:  'bg-purple-500',
  INSERT:    'bg-teal-500',
  DELETE:    'bg-red-500',
};

const typeList = computed(() =>
  Object.entries(byType.value).map(([type, count]) => ({
    type,
    count,
    pct: total.value > 0 ? Math.round((count as number / total.value) * 100) : 0,
    color: typeColors[type] ?? 'bg-gray-400',
  })).sort((a, b) => (b.count as number) - (a.count as number))
);

function formatLastDate(iso: string): string {
  const d = new Date(iso);
  const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60)    return `${Math.floor(diff)}s ago`;
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return d.toLocaleDateString();
}
</script>

<template>
  <Card class="flex flex-col justify-between">
    <CardHeader class="flex flex-row items-center gap-2">
      <BarChart3 class="h-4 w-4 text-blue-500" />
      SPARQL Statistics
    </CardHeader>
    <CardContent class="space-y-3">
      <!-- Total badge -->
      <div class="flex items-center justify-between">
        <span class="text-sm text-gray-500">Total Queries</span>
        <Badge class="text-base px-3 py-1">{{ total }}</Badge>
      </div>

      <!-- Type breakdown bars -->
      <div v-if="typeList.length > 0" class="space-y-1.5">
        <div v-for="item in typeList" :key="item.type" class="space-y-0.5">
          <div class="flex justify-between text-xs text-gray-500">
            <span>{{ item.type }}</span>
            <span>{{ item.count }} ({{ item.pct }}%)</span>
          </div>
          <div class="h-1.5 rounded-full bg-gray-100 dark:bg-gray-800 overflow-hidden">
            <div
              :class="[item.color, 'h-full rounded-full transition-all duration-700']"
              :style="{ width: item.pct + '%' }"
            />
          </div>
        </div>
      </div>
      <div v-else class="text-xs text-gray-400">No queries executed yet.</div>

      <!-- Last query -->
      <div v-if="lastQuery" class="pt-1 border-t text-xs text-gray-400 space-y-0.5">
        <div class="flex justify-between">
          <span>Last query</span>
          <span>{{ formatLastDate(lastQuery.executed_at) }}</span>
        </div>
        <p class="font-mono truncate text-gray-500 dark:text-gray-300">{{ lastQuery.query_snippet }}</p>
      </div>
    </CardContent>
    <CardFooter class="flex items-center justify-end">
      <NuxtLink to="/sparql">
        <Button variant="secondary" size="sm">
          Open Editor <ChevronRight class="h-3 w-3 ml-1" />
        </Button>
      </NuxtLink>
    </CardFooter>
  </Card>
</template>
