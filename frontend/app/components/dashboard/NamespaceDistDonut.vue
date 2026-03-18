<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, ArcElement)

import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { metrics } = useDashboard();

const chartData = computed(() => {
  const ns = metrics.value?.namespaces ?? [];
  const colors = [
    '#ff2159', '#1549e6', '#ff9900', '#22c55e', '#a855f7',
    '#06b6d4', '#f43f5e', '#f97316',
  ];
  return {
    labels: ns.map(n => n.prefix),
    datasets: [{
      label: 'Predicates',
      data: ns.map(n => n.count),
      borderColor: '#fff',
      borderWidth: 0,
      backgroundColor: colors.slice(0, ns.length),
    }],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true },
  },
}
</script>

<template>
  <Card class="flex flex-col">
    <CardHeader class="items-center pb-0">
      <CardTitle>Namespace Distribution</CardTitle>
    </CardHeader>
    <CardContent class="flex-1 pb-0">
      <Doughnut :options="chartOptions" :data="chartData" />
    </CardContent>
    <CardFooter class="flex-col gap-2 text-sm">
      <div class="leading-none text-muted-foreground text-center text-xs">
        {{ metrics?.namespaces?.length ?? 0 }} namespaces detected
      </div>
    </CardFooter>
  </Card>
</template>
