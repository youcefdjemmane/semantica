<script setup lang="ts">
import { PolarArea } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, RadialLinearScale, ArcElement } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, RadialLinearScale, ArcElement)

import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { metrics } = useDashboard();

const chartData = computed(() => {
  const kpis = metrics.value?.kpis;
  const s = kpis?.total_subjects   ?? 0;
  const p = kpis?.total_predicates ?? 0;
  const o = kpis?.total_objects    ?? 0;
  return {
    labels: ['Subjects', 'Predicates', 'Objects'],
    datasets: [{
      label: 'Count',
      data: [s, p, o],
      borderColor: '#fff',
      borderWidth: 0,
      backgroundColor: ['#ff2159', '#1549e6', '#ff9900'],
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
    r: {
      pointLabels: { display: false },
      ticks: { display: false },
      grid: { display: false },
    },
  },
}
</script>

<template>
  <Card class="flex flex-col">
    <CardHeader class="items-center pb-0">
      <CardTitle>Triples Distribution</CardTitle>
    </CardHeader>
    <CardContent class="flex-1 pb-0">
      <PolarArea :options="chartOptions" :data="chartData" />
    </CardContent>
    <CardFooter class="flex-col gap-2 text-sm">
      <div class="flex items-center justify-center gap-4 text-xs text-muted-foreground">
        <span class="flex items-center gap-1"><span class="inline-block w-2 h-2 rounded-full bg-[#ff2159]"></span>Subjects</span>
        <span class="flex items-center gap-1"><span class="inline-block w-2 h-2 rounded-full bg-[#1549e6]"></span>Predicates</span>
        <span class="flex items-center gap-1"><span class="inline-block w-2 h-2 rounded-full bg-[#ff9900]"></span>Objects</span>
      </div>
    </CardFooter>
  </Card>
</template>
