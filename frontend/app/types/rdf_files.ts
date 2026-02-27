export interface RDFfile {
    id: string
    name: string
    format: string
    triples: number
    size: number
    uploaded: string
    status: 'ACTIVE' | 'INACTIVE'
}