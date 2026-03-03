<script setup lang="ts">
</script>


<template>

    <!-- Sidebar togglem, use cookies -->
    <!-- App Theme toggle -->
     <div class="p-6 space-y-6">
        <Card>
            <CardHeader>
                <CardTitle>Settings</CardTitle>
                <CardDescription>Configure application settings and preferences.</CardDescription>
            </CardHeader>
            <CardContent>
                <div class="space-y-4">
                    <!-- Theme Selection -->
                    <div class="flex items center justify-between">
                        <div>
                            <h3 class="text-sm font-medium">Theme</h3>
                            <p class="text-sm text-muted-foreground">Choose between light, dark, or system theme.</p>
                        </div>
                        <ModeToggle />
                    </div>
                </div>
            </CardContent>  
        </Card>
     </div>
</template>