<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { metrics } = useDashboard();

const chartData = computed(() => {
  const preds = metrics.value?.top_predicates ?? [];
  return {
    labels: preds.map(p => p.label || p.uri.split('/').pop() || p.uri),
    datasets: [{
      label: 'Occurrences',
      data: preds.map(p => p.count),
      borderColor: '#fff',
      borderWidth: 0,
      backgroundColor: [
        '#ff2159', '#1549e6', '#ff9900', '#22c55e', '#a855f7',
        '#06b6d4', '#f43f5e', '#f97316', '#84cc16', '#14b8a6',
      ],
    }],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true },
  },
  scales: {
    y: { beginAtZero: true, ticks: { display: false } },
    x: { ticks: { maxRotation: 30, font: { size: 10 } } },
  },
}
</script>

<template>
  <Card class="flex flex-col">
    <CardHeader class="items-center pb-0">
      <CardTitle>Top Predicates</CardTitle>
    </CardHeader>
    <CardContent class="flex-1 pb-0">
      <Bar :options="chartOptions" :data="chartData" />
    </CardContent>
    <CardFooter class="flex-col gap-2 text-sm">
      <div class="leading-none text-muted-foreground text-center text-xs">
        {{ metrics?.top_predicates?.length ?? 0 }} most-used predicates across all graphs
      </div>
    </CardFooter>
  </Card>
</template>
