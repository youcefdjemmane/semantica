<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

import { useDashboard } from '~/composables/useDashboard';
import { computed } from 'vue';

const { metrics } = useDashboard();

const chartData = computed(() => {
    const graphs = metrics.value?.graph_distribution || [];
    
    // Trier par triples (décroissant) et prendre le top 5
    const sorted = [...graphs].sort((a, b) => b.triples - a.triples).slice(0, 5);

    return {
        labels: sorted.map(g => g.name.length > 20 ? g.name.substring(0, 20) + '...' : g.name),
        datasets: [{
            label: 'Triples Count',
            data: sorted.map(g => g.triples),
            backgroundColor: '#8b5cf6',
            borderRadius: 4,
        }]
    };
});

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y' as const, // Horizontal bar chart
    plugins: {
        legend: { display: false },
        tooltip: {
            callbacks: {
                label: (context: any) => ` ${context.raw.toLocaleString()} triples`
            }
        }
    },
    scales: {
        x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#9ca3af', font: { size: 10 } }
        },
        y: {
            grid: { display: false },
            ticks: { color: '#d1d5db', font: { size: 11 } }
        }
    }
};
</script>

<template>
    <Card class="flex flex-col">
        <CardHeader class="pb-2">Top Graphs by Size</CardHeader>
        <CardContent class="flex-1 flex flex-col justify-center min-h-[200px]">
            <div class="h-[200px] w-full">
                <Bar 
                    v-if="chartData.labels.length > 0"
                    :data="chartData" 
                    :options="chartOptions" 
                />
                <div v-else class="h-full flex items-center justify-center text-sm text-gray-400">
                    No graph data available.
                </div>
            </div>
        </CardContent>
    </Card>
</template>
