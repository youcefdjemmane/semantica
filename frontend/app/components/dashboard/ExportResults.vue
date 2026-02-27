<script setup lang="ts">
import { FileDown } from 'lucide-vue-next';



</script>


<template>

    <Card class="flex flex-col justify-between">
        <CardHeader>Export Results</CardHeader>
        <CardContent class="space-y-2 mb-4">
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Last Query</span>
                <span class="text-gray-800 dark:text-gray-100 font-medium">SELECT</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Rows</span>
                <span class="text-gray-800 dark:text-gray-100 font-medium">342</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-500">Executed</span>
                <span class="text-gray-400">2 min ago</span>
            </div>
        </CardContent>
        <CardFooter class="flex justify-end space-x-2">
            <Button > 
                <FileDown/>
                 Export CSV
            </Button>
            <Button variant="outline">
                <FileDown/>
                 Export JSON
            </Button>
        </CardFooter>
    </Card>
</template>