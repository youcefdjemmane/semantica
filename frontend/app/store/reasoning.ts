import { defineStore } from "pinia";

export const useReasoningStore = defineStore('reasoning', {
  state: () => ({
    isEnabled: false,
    activeFormalism: 'RDFS',
    inferredCount: 0
  }),
  getters: {
    getIsEnabled: (state) => state.isEnabled,
    getActiveFormalism: (state) => state.activeFormalism,
    getInferredCount: (state) => state.inferredCount
  },
  actions: {
    toggleEnabled() {
      this.isEnabled = !this.isEnabled;
    },
    setEnabled(value: boolean) {
      this.isEnabled = value;
    },
    setFormalism(formalism: string) {
      this.activeFormalism = formalism;
    },
    setInferredCount(count: number) {
      this.inferredCount = count;
    }
  },
})
