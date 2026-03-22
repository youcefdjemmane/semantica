import { ref } from 'vue';
import { useRuntimeConfig } from '#app';

export interface RdfKpis {
  total_graphs: number;
  total_triples: number;
  total_subjects: number;
  total_predicates: number;
  total_objects: number;
}

export interface TopPredicate {
  uri: string;
  label: string;
  count: number;
}

export interface NamespaceEntry {
  prefix: string;
  count: number;
}

export interface GraphDistEntry {
  name: string;
  triples: number;
}

export interface DashboardMetrics {
  kpis: RdfKpis;
  top_predicates: TopPredicate[];
  namespaces: NamespaceEntry[];
  graph_distribution: GraphDistEntry[];
}

export interface OntologyStats {
  total_ontologies: number;
  total_classes: number;
  total_properties: number;
  total_individuals: number;
  owl_count: number;
  rdfs_count: number;
}

export interface SparqlStats {
  total_queries: number;
  by_type: Record<string, number>;
  last_query: {
    query_type: string;
    executed_at: string;
    query_snippet: string;
  } | null;
}

export interface GraphHealth {
  graph_id: string;
  name: string;
  score: number;
  quality: 'good' | 'fair' | 'poor';
  issues: { level: string; message: string }[];
  insight: string | null;
  triples: number;
  subjects: number;
  predicates: number;
  objects: number;
}

export interface SparqlHistoryEntry {
  id: string;
  query: string;
  query_type: string;
  graph_id: string;
  executed_at: string;
}

export interface LoadedFile {
  id: string;
  name: string;
  type: 'RDF' | 'Ontology';
  format: string;
  triples: number;
  uploaded: string;
}

// Module-level reactive state (shared across all uses of this composable)
const metrics = ref<DashboardMetrics | null>(null);
const ontologyStats = ref<OntologyStats | null>(null);
const sparqlStats = ref<SparqlStats | null>(null);
const healthData = ref<GraphHealth | null>(null);
const recentQueries = ref<SparqlHistoryEntry[]>([]);
const loadedFiles = ref<LoadedFile[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

export function useDashboard() {
  const config = useRuntimeConfig();
  const apiBase = (config.public.apiBase as string) || 'http://localhost:8000/api/v1';

  const fetchAllDashboardData = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const [
        metricsRes,
        ontoStatsRes,
        sparqlStatsRes,
        sparqlRes,
        rdfFilesRes,
        ontoFilesRes,
      ] = await Promise.all([
        fetch(`${apiBase}/rdf/dashboard-metrics`),
        fetch(`${apiBase}/ontology/stats`),
        fetch(`${apiBase}/sparql/stats`),
        fetch(`${apiBase}/sparql/recent`),
        fetch(`${apiBase}/rdf/files`),
        fetch(`${apiBase}/ontology/files`),
      ]);

      if (metricsRes.ok)      metrics.value      = await metricsRes.json();
      if (ontoStatsRes.ok)    ontologyStats.value = await ontoStatsRes.json();
      if (sparqlStatsRes.ok)  sparqlStats.value   = await sparqlStatsRes.json();
      if (sparqlRes.ok)       recentQueries.value = await sparqlRes.json();

      // Fusionner les fichiers RDF et Ontologies
      const rdfFiles  = rdfFilesRes.ok  ? await rdfFilesRes.json()  : [];
      const ontoFiles = ontoFilesRes.ok ? await ontoFilesRes.json() : [];

      const formattedRdf: LoadedFile[] = rdfFiles.map((f: any) => ({
        id:       f.id,
        name:     f.file_name || f.name,
        type:     'RDF' as const,
        format:   f.format?.toUpperCase() || 'RDF',
        triples:  f.triples_count ?? 0,
        uploaded: new Date(f.uploaded_at).toLocaleDateString(),
      }));

      const formattedOnto: LoadedFile[] = ontoFiles.map((f: any) => ({
        id:       f.id,
        name:     f.file_name || f.name,
        type:     'Ontology' as const,
        format:   (f.format || 'owl').toUpperCase(),
        triples:  (f.classes_count ?? 0) + (f.properties_count ?? 0) + (f.individuals_count ?? 0),
        uploaded: new Date(f.uploaded_at).toLocaleDateString(),
      }));

      loadedFiles.value = [...formattedRdf, ...formattedOnto];

      // Health du premier graphe RDF si disponible
      if (rdfFiles.length > 0) {
        const firstId = rdfFiles[0].id;
        const healthRes = await fetch(`${apiBase}/rdf/${firstId}/health`);
        if (healthRes.ok) healthData.value = await healthRes.json();
      }

    } catch (e: any) {
      error.value = e.message;
      console.error('[useDashboard] fetch error:', e);
    } finally {
      isLoading.value = false;
    }
  };

  const deleteFile = async (id: string, type: string): Promise<boolean> => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')) return false;
    try {
      const endpoint = type === 'RDF'
        ? `${apiBase}/rdf/${id}`
        : `${apiBase}/ontology/${id}`;
      const res = await fetch(endpoint, { method: 'DELETE' });
      if (res.ok) {
        await fetchAllDashboardData();
        return true;
      }
      alert('Erreur lors de la suppression');
      return false;
    } catch (e) {
      console.error(e);
      alert('Erreur lors de la suppression');
      return false;
    }
  };

  return {
    metrics,
    ontologyStats,
    sparqlStats,
    healthData,
    recentQueries,
    loadedFiles,
    isLoading,
    error,
    fetchAllDashboardData,
    deleteFile,
  };
}
