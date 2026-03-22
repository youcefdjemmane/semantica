<!-- pages/sparql/index.vue -->
<script setup lang="ts">
import LeftPanel from '~/components/sparql/LeftPanel.vue';
import RightPanel from '~/components/sparql/RightPanel.vue';
import RecentQueries from '~/components/sparql/RecentQueries.vue';

definePageMeta({
    title: "SPARQL Editor",
})
</script>

<template>
  <div class="flex flex-col gap-4 p-3 flex-1 w-full h-full min-h-0">

    <!-- Ligne 1 : deux colonnes — éditeur (gauche) + historique (droite) -->
    <div class="grid grid-cols-1 lg:grid-cols-[2fr_2fr] gap-4">
      <LeftPanel />
      <RecentQueries />
    </div>

    <!-- Ligne 2 : résultats pleine largeur -->
    <div class="w-full">
      <RightPanel />
    </div>

  </div>
</template>