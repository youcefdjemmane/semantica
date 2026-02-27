type QueryType = "SELECT" | "CONSTRUCT" | "DESCRIBE" | "ASK";

type BadgeVariant =
  | "default"
  | "secondary"
  | "destructive"
  | "outline"
  | "rdf"
  | "ontology"
  | "select"
  | "ask"
  | "construct"
  | "describe";

export function mapQueryToVariant(type: QueryType): BadgeVariant {
  switch (type) {
    case "SELECT":
      return "select";
    case "ASK":
      return "ask";
    case "CONSTRUCT":
      return "construct";
    case "DESCRIBE":
      return "describe"; // or whatever style you want
    default:
      return "default";
  }
}
