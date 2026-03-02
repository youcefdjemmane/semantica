<script setup>
import { Download, Settings } from 'lucide-vue-next';

const results = ref({
    type: 'ASK',
    result: 'FALSE',
    execution_time: 1000
})
const error = ref(null)
const running = ref(false)
const history = ref([])
</script>

<template>
    <Card class="w-[50%] h-[89vh]    rounded-xl   flex flex-col overflow-hidden">

        <!-- Results Header -->
        <CardHeader class="flex flex-row  items-center justify-between    ">


            <CardTitle>Results</CardTitle>
            <!-- Export (only for SELECT) -->
            <div class="flex space-x-2">
                <Button @click="exportResults('json')" size="sm">
                    <Download /> JSON
                </Button>
                <Button @click="exportResults('csv')" variant="outline" size="sm">
                    <Download /> CSV
                </Button>
            </div>
        </CardHeader>

        <!-- Results Body -->
        <CardContent class="flex-1 overflow-auto p-6">

            <!-- Empty state -->
            <div v-if="!results && !running && !error"
                class="h-full flex flex-col items-center justify-center text-gray-300">
                <p class="text-4xl mb-3">🔍</p>
                <p class="text-sm font-medium">Run a query to see results</p>
                <p class="text-xs mt-1">Ctrl+Enter to run</p>
            </div>

            <!-- Loading -->
            <div v-if="running" class="h-full flex-col flex items-center justify-center">


                <Settings class=" animate-spin" />
                <p class="text-sm">Executing query...</p>

            </div>

            <!-- Error -->
            <div v-if="error" class="h-full flex-col flex items-center justify-center">
                <p class="text-sm font-semibold text-red-600 mb-1">Query Error</p>
                <p class="text-xs text-red-500 font-mono whitespace-pre-wrap">{{ error }}</p>
            </div>

            <!-- SELECT → Table -->
            <div v-if="results?.type === 'SELECT' && !running">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="text-left text-xs text-gray-400 uppercase tracking-wide border-b ">
                            <th v-for="v in results.vars" :key="v" class="pb-2 pr-4 font-medium">?{{ v }}</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-50">
                        <tr v-for="(row, i) in results.rows" :key="i" class="hover:bg-gray-50">
                            <td v-for="v in results.vars" :key="v" class="py-2 pr-4 text-xs">
                                <span class="font-mono text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded">
                                    {{ row[v] ?? '—' }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ASK → Boolean -->
            <div v-if="results?.type === 'ASK' && !running" class="h-full ">

                <p class="text-2xl font-bold" :class="results.result == 'TRUE' ? 'text-green-600' : 'text-red-500'">
                    {{ results.result }}
                </p>
                <p class=" text-primary">execution time: {{ results.execution_time }}ms</p>
            </div>

            <!-- CONSTRUCT → Mini Cytoscape Graph -->
            <div v-if="results?.type === 'CONSTRUCT' && !running" class="h-full flex flex-col gap-2">
                <p class="text-xs text-gray-400">{{ results.triple_count }} triples constructed</p>
                <div ref="constructGraph" class="flex-1 rounded-xl border  bg-gray-50"></div>
            </div>

        </CardContent>
    </Card>
</template>