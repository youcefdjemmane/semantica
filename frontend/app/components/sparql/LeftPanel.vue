<script setup lang="ts">
import { Codemirror } from 'vue-codemirror'
import { keymap } from '@codemirror/view'
import { defaultKeymap } from '@codemirror/commands'
import { autocompletion } from '@codemirror/autocomplete'
import { Eraser, Play, Star, RefreshCw } from 'lucide-vue-next'
import { sparql } from 'codemirror-lang-sparql';
import { useSparqlState, useSparqlActions } from '~/composables/useSparql';
import { useActiveGraphStore } from '~/store/active_graph';
import { useRuntimeConfig } from '#app';
import { ref, computed, watch, onMounted } from 'vue';

const { query, activeGraphId, activeGraphName, schema } = useSparqlState();
const { runQuery, clearState, fetchHistory, fetchSchema } = useSparqlActions();
const activeGraphStore = useActiveGraphStore();
const availableGraphs = ref<any[]>([]);
const isLoadingGraph = ref(false);
const loadingProgress = ref(0);
let progressTimer: ReturnType<typeof setInterval> | null = null;

const SPARQL_KEYWORDS = [
  'SELECT','DISTINCT','REDUCED','WHERE','FILTER','OPTIONAL','UNION','GRAPH',
  'PREFIX','BASE','FROM','NAMED','ORDER','BY','ASC','DESC','LIMIT','OFFSET',
  'GROUP','HAVING','BIND','VALUES','AS','IN','NOT','EXISTS','MINUS','SERVICE',
  'SILENT','CONSTRUCT','DESCRIBE','ASK','INSERT','DELETE','DATA','LOAD','CLEAR',
  'DROP','CREATE','ADD','MOVE','COPY','WITH','USING','DEFAULT','ALL','NAMED',
  'OPTIONAL','UNION','MINUS','GRAPH','SERVICE','BIND','UNDEF','TRUE','FALSE',
  'STR','LANG','LANGMATCHES','DATATYPE','BOUND','IRI','URI','BNODE','RAND',
  'ABS','CEIL','FLOOR','ROUND','CONCAT','STRLEN','SUBSTR','UCASE','LCASE',
  'ENCODE_FOR_URI','CONTAINS','STRSTARTS','STRENDS','STRBEFORE','STRAFTER',
  'YEAR','MONTH','DAY','HOURS','MINUTES','SECONDS','TIMEZONE','TZ','NOW',
  'UUID','STRUUID','MD5','SHA1','SHA256','SHA384','SHA512','COALESCE',
  'IF','STRLANG','STRDT','SAMETERM','ISIRI','ISURI','ISBLANK','ISLITERAL',
  'ISNUMERIC','REGEX','SUBSTR','REPLACE','COUNT','SUM','MIN','MAX','AVG',
  'SAMPLE','GROUP_CONCAT','SEPARATOR',
  '<<','>>','ASSERTED','OCCURRENCES',
];

function sparqlCompletionSource(context) {
  const word = context.matchBefore(/[\w:<>?!]+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const options = [];
  for (const kw of SPARQL_KEYWORDS) {
    if (kw.toLowerCase().startsWith(word.text.toLowerCase()))
      options.push({ label: kw, type: 'keyword', boost: 3 });
  }
  const s = schema.value;
  for (const [prefix] of Object.entries(s.prefixes || {})) {
    if (prefix && `${prefix}:`.startsWith(word.text))
      options.push({ label: `${prefix}:`, type: 'namespace', info: s.prefixes[prefix], boost: 2 });
  }
  for (const cls of s.classes || []) {
    const short = cls.split(/[/#]/).pop();
    if (short && short.toLowerCase().startsWith(word.text.toLowerCase()))
      options.push({ label: short, detail: shortenURI(cls), type: 'class', boost: 1 });
  }
  for (const prop of s.properties || []) {
    const short = prop.split(/[/#]/).pop();
    if (short && short.toLowerCase().startsWith(word.text.toLowerCase()))
      options.push({ label: short, detail: shortenURI(prop), type: 'property', boost: 1 });
  }
  return { from: word.from, options };
}

function shortenURI(uri) {
  return uri.split(/[/#]/).pop() || uri;
}

function startLoadingProgress() {
  loadingProgress.value = 0;
  progressTimer = setInterval(() => {
    if (loadingProgress.value < 88) loadingProgress.value += Math.random() * 7 + 2;
  }, 180);
}

function stopLoadingProgress() {
  if (progressTimer) clearInterval(progressTimer);
  progressTimer = null;
  loadingProgress.value = 100;
  setTimeout(() => { loadingProgress.value = 0; }, 500);
}

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase || 'http://localhost:8000/api/v1';
  try {
    const res = await fetch(`${apiBase}/rdf/files`);
    if (res.ok) availableGraphs.value = await res.json();
  } catch (e) {
    console.error("Failed to load graphs", e);
  }
  await fetchHistory();
  if (activeGraphId.value) {
    await fetchSchema(activeGraphId.value);
  }
});

async function onGraphSelect(event: any) {
  const id = (event.target as HTMLSelectElement).value;
  if (!id) return;
  const g = availableGraphs.value.find(x => x.id === id);
  if (!g) return;
  isLoadingGraph.value = true;
  startLoadingProgress();
  try {
    activeGraphStore.setGraph({ id: g.id, name: g.name || g.file_name });
    await fetchSchema(g.id);
  } finally {
    stopLoadingProgress();
    isLoadingGraph.value = false;
  }
}

async function reloadSchema() {
  if (!activeGraphId.value || isLoadingGraph.value) return;
  isLoadingGraph.value = true;
  startLoadingProgress();
  try {
    await fetchSchema(activeGraphId.value);
  } finally {
    stopLoadingProgress();
    isLoadingGraph.value = false;
  }
}

watch(activeGraphId, async (id) => {
  if (id) await fetchSchema(id);
});

const extensions = computed(() => [
  sparql(),
  autocompletion({ override: [sparqlCompletionSource] }),
  keymap.of([
    ...defaultKeymap,
    { key: 'Ctrl-Enter', run: () => { runQuery(); return true } }
  ])
]);

const detectedType = computed(() => {
  if (!query.value) return null;
  const cleaned = query.value.replace(/#.*$/gm, '').trim();
  const match = cleaned.match(/\b(SELECT|ASK|CONSTRUCT|DESCRIBE|INSERT|DELETE|UPDATE)\b/i);
  return match ? match[1].toUpperCase() : null;
});

const hasRdfStar = computed(() => /<</.test(query.value || ''));

const badgeVariant = computed(() => {
  const t = detectedType.value;
  if (t === 'SELECT') return 'select';
  if (t === 'ASK') return 'ask';
  if (t === 'CONSTRUCT') return 'construct';
  if (t === 'INSERT') return 'default';
  if (t === 'DELETE') return 'destructive';
  if (t === 'UPDATE') return 'secondary';
  return 'secondary';
});

function clearEditor() { clearState(); }
</script>

<template>
  <div class="w-full flex flex-col gap-3">

    <!-- ───── Barre graphe actif ───── -->
    <div
      class="relative rounded-xl border overflow-hidden transition-all duration-300 bg-card text-card-foreground"
      :class="
        isLoadingGraph
          ? 'border-border/60'
          : activeGraphId
            ? 'border-border'
            : 'border-border/40'
      "
    >
      <div class="flex items-center gap-3 px-4 py-2.5">

        <!-- Point de statut -->
        <div
          class="w-2 h-2 rounded-full flex-shrink-0 transition-all duration-300"
          :class="
            isLoadingGraph
              ? 'bg-muted-foreground/50 animate-pulse'
              : activeGraphId
                ? 'bg-foreground/40'
                : 'bg-muted-foreground/30'
          "
        />

        <!-- Icône conteneur -->
        <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors duration-300 bg-muted">
          <!-- Spinner chargement -->
          <div
            v-if="isLoadingGraph"
            class="w-3.5 h-3.5 rounded-full border-2 border-muted-foreground/40 border-t-transparent animate-spin"
          />
          <!-- Icône graphe SVG -->
          <svg v-else width="15" height="15" viewBox="0 0 16 16" fill="none">
            <circle cx="4"  cy="8"  r="2" :fill="activeGraphId ? 'currentColor' : 'currentColor'" class="text-muted-foreground" style="fill:currentColor;opacity:0.7"/>
            <circle cx="12" cy="4"  r="2" style="fill:currentColor;opacity:0.7" class="text-muted-foreground"/>
            <circle cx="12" cy="12" r="2" style="fill:currentColor;opacity:0.7" class="text-muted-foreground"/>
            <line x1="6" y1="7.2" x2="10" y2="5"  stroke="currentColor" stroke-width="1.2" class="text-muted-foreground" style="opacity:0.4"/>
            <line x1="6" y1="8.8" x2="10" y2="11" stroke="currentColor" stroke-width="1.2" class="text-muted-foreground" style="opacity:0.4"/>
          </svg>
        </div>

        <!-- Texte info -->
        <div class="flex-1 min-w-0">
          <p class="text-[10px] leading-none mb-0.5 text-muted-foreground">
            {{ isLoadingGraph ? 'Chargement en cours…' : 'Graphe actif' }}
          </p>
          <p
            class="text-sm font-medium leading-snug truncate transition-colors duration-200"
            :class="activeGraphId ? 'text-foreground' : 'text-muted-foreground'"
          >
            {{ activeGraphId ? activeGraphName : 'Sélectionnez un graphe pour commencer' }}
          </p>
        </div>

        <!-- Séparateur -->
        <div class="w-px h-5 bg-border flex-shrink-0" />

        <!-- Select graphe -->
        <div class="relative flex-shrink-0">
          <select
            class="appearance-none
                   bg-background
                   border border-border
                   text-foreground
                   text-sm font-normal rounded-lg pl-3 pr-7 py-1.5
                   outline-none cursor-pointer min-w-[160px]
                   hover:border-border/80
                   focus:ring-1 focus:ring-ring
                   disabled:opacity-40 disabled:cursor-not-allowed
                   transition-colors"
            :disabled="isLoadingGraph"
            :value="activeGraphId || ''"
            @change="onGraphSelect"
          >
            <option value="" disabled>─ Choisir un graphe ─</option>
            <option v-for="g in availableGraphs" :key="g.id" :value="g.id">
              {{ g.name || g.file_name }}
            </option>
          </select>
          <!-- Chevron -->
          <svg
            class="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-muted-foreground"
            width="11" height="11" viewBox="0 0 12 12" fill="none"
          >
            <path d="M2 4.5L6 8L10 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </div>

        <!-- Bouton recharger -->
        <button
          v-if="activeGraphId"
          :disabled="isLoadingGraph"
          @click="reloadSchema"
          class="w-8 h-8 rounded-lg border border-border
                 flex items-center justify-center
                 text-muted-foreground
                 hover:bg-muted hover:text-foreground
                 disabled:opacity-30 disabled:cursor-not-allowed
                 transition-all flex-shrink-0"
          title="Recharger le schéma"
        >
          <RefreshCw
            class="w-3.5 h-3.5"
            :class="{ 'animate-spin': isLoadingGraph }"
          />
        </button>

      </div>

      <!-- Barre de progression -->
      <div
        class="absolute bottom-0 left-0 h-[2px] bg-foreground/30 transition-all duration-300 ease-out"
        :style="{ width: isLoadingGraph ? `${loadingProgress}%` : '0%', opacity: isLoadingGraph ? 1 : 0 }"
      />
    </div>
    <!-- ───── Fin barre graphe actif ───── -->

    <!-- ───── Éditeur SPARQL ───── -->
    <Card class="flex flex-col min-h-[450px]">
      <CardHeader class="flex flex-row justify-between items-center py-3">
        <CardTitle>Query Editor</CardTitle>
        <div class="flex items-center gap-2 flex-wrap">
          <Badge v-if="detectedType" :variant="badgeVariant">
            {{ detectedType }}
          </Badge>
          <Badge v-if="hasRdfStar" variant="secondary" class="flex items-center gap-1">
            <Star class="w-3 h-3 text-yellow-500" /> RDF-star
          </Badge>
          <Button @click="clearEditor" variant="outline" size="sm">
            <Eraser class="w-3 h-3 mr-1" /> Vider
          </Button>
          <Button @click="runQuery" size="sm">
            <Play class="w-3 h-3 mr-1" />
            <span v-if="detectedType === 'INSERT' || detectedType === 'DELETE' || detectedType === 'UPDATE'">
              Exécuter UPDATE
            </span>
            <span v-else>Exécuter</span>
          </Button>
        </div>
      </CardHeader>

      <CardContent class="flex-1 overflow-auto mt-0 p-0 border-t border-gray-100 dark:border-gray-800">
        <Codemirror v-model="query" :extensions="extensions" class="h-full text-sm" />
      </CardContent>
    </Card>

    <!-- ───── Raccourcis clavier ───── -->
    <div class="flex items-center gap-2 text-xs text-muted-foreground px-1">
      <span class="px-1.5 py-0.5 rounded bg-muted font-mono text-[10px]">Ctrl+Space</span>
      <span>Autocomplétion (mots-clés, préfixes, classes, propriétés)</span>
      <span class="px-1.5 py-0.5 rounded bg-muted font-mono text-[10px]">Ctrl+Enter</span>
      <span>Exécuter</span>
    </div>

  </div>
</template>