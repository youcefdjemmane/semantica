<script setup lang="ts">
import { Codemirror } from 'vue-codemirror'
import { oneDark } from '@codemirror/theme-one-dark'
import { keymap } from '@codemirror/view'
import { defaultKeymap } from '@codemirror/commands'
import { autocompletion, CompletionContext } from '@codemirror/autocomplete'
import { Eraser, Play, CircleDot, TriangleAlert, Star, Database } from 'lucide-vue-next'
import { sparql } from 'codemirror-lang-sparql';
import { useSparqlState, useSparqlActions } from '~/composables/useSparql';
import { useActiveGraphStore } from '~/store/active_graph';
import { useRuntimeConfig } from '#app';
import { ref } from 'vue';

const { query, activeGraphId, activeGraphName, schema } = useSparqlState();
const { runQuery, clearState, fetchHistory, fetchSchema } = useSparqlActions();
const activeGraphStore = useActiveGraphStore();
const availableGraphs = ref<any[]>([]);

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
    if (kw.toLowerCase().startsWith(word.text.toLowerCase())) {
      options.push({ label: kw, type: 'keyword', boost: 3 });
    }
  }

  const s = schema.value;

  for (const [prefix] of Object.entries(s.prefixes || {})) {
    if (prefix && `${prefix}:`.startsWith(word.text)) {
      options.push({ label: `${prefix}:`, type: 'namespace', info: s.prefixes[prefix], boost: 2 });
    }
  }

  for (const cls of s.classes || []) {
    const short = cls.split(/[/#]/).pop();
    if (short && short.toLowerCase().startsWith(word.text.toLowerCase())) {
      options.push({ label: short, detail: shortenURI(cls), type: 'class', boost: 1 });
    }
    if (cls.toLowerCase().startsWith(word.text.toLowerCase())) {
      options.push({ label: cls, type: 'class' });
    }
  }

  for (const prop of s.properties || []) {
    const short = prop.split(/[/#]/).pop();
    if (short && short.toLowerCase().startsWith(word.text.toLowerCase())) {
      options.push({ label: short, detail: shortenURI(prop), type: 'property', boost: 1 });
    }
  }

  return { from: word.from, options };
}

function shortenURI(uri) {
  return uri.split(/[/#]/).pop() || uri;
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

function onGraphSelect(event: any) {
  const selectElement = event.target as HTMLSelectElement;
  const id = selectElement.value;
  if (!id) return;
  const g = availableGraphs.value.find(x => x.id === id);
  if (g) {
      activeGraphStore.setGraph({ id: g.id, name: g.name || g.file_name });
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

    <div class="flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-sm">
        <div class="flex items-center gap-2">
            <template v-if="activeGraphId">
                <CircleDot class="w-3.5 h-3.5 text-green-500 shrink-0" />
                <span class="text-green-700 dark:text-green-300 font-medium truncate">
                    Graphe actif : {{ activeGraphName }}
                </span>
            </template>
            <template v-else>
                <div class="w-2.5 h-2.5 rounded-full bg-slate-400 shrink-0"></div>
                <span class="text-slate-600 dark:text-slate-400 font-medium">
                    Aucun graphe actif
                </span>
            </template>
        </div>

        <div class="shrink-0">
            <select
                class="bg-white dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs rounded px-2 py-1 outline-none max-w-[200px]"
                @change="onGraphSelect"
                :value="activeGraphId || ''"
            >
                <option value="" disabled>─ Sélectionner un graphe ─</option>
                <option v-for="g in availableGraphs" :key="g.id" :value="g.id">
                    {{ g.name || g.file_name }}
                </option>
            </select>
        </div>
    </div>

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
            <span v-if="detectedType === 'INSERT' || detectedType === 'DELETE' || detectedType === 'UPDATE'">Exécuter UPDATE</span>
            <span v-else>Exécuter</span>
          </Button>
        </div>
      </CardHeader>

      <CardContent class="flex-1 overflow-auto mt-0 p-0 border-t border-gray-100 dark:border-gray-800">
        <Codemirror v-model="query" :extensions="extensions" class="h-full text-sm" />
      </CardContent>
    </Card>

    <div class="flex items-center gap-2 text-xs text-muted-foreground px-1">
      <span class="px-1.5 py-0.5 rounded bg-muted font-mono text-[10px]">Ctrl+Space</span>
      <span>Autocomplétion (mots-clés, préfixes, classes, propriétés)</span>
      <span class="px-1.5 py-0.5 rounded bg-muted font-mono text-[10px]">Ctrl+Enter</span>
      <span>Exécuter</span>
    </div>

  </div>
</template>