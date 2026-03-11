import { defineStore } from "pinia";
interface GraphDetails {
    id : string,
    name : string
}

export const useActiveGraphStore = defineStore('active_graph', {
  state: () => ({ 
        id: 'fadel',
        name: 'fadel' 
    }),
  getters: {
    getName: (state) => state.id,
    getId:(state) => state.name
  },
  actions: {
    setGraph(graph: GraphDetails){
        this.$state = graph
    }
  },
})