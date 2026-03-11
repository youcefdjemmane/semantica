export interface OntologiesStats {
  total_ontologies: number
  total_classes: number
  total_properties: number
  total_individuals: number
  owl_count: number
  rdfs_count: number
}


export interface OntologyFileStats {
  id: string
  name: string
  format: string
  file_size: number
  classes_count: number
  properties_count: number
  individuals_count: number
  uploaded_at: string
}


export interface OntologyEdge {
  source: string
  target: string
  type: string
}


export interface OntologyNode {
  id: string
  label: string
  type: string
  comment: string | null

  equivalent_classes: string[]
  disjoint_classes: string[]
  union_of: string[]
  intersection_of: string[]

  object_properties: string[]
  data_properties: string[]

  restrictions: any[]
  individuals: string[]

  individual_count: number
}


export interface Ontology {
  id: string
  name: string
  format: string

  class_count: number
  object_property_count: number
  data_property_count: number
  individual_count: number

  nodes: OntologyNode[]
  edges: OntologyEdge[]
}