import { writable } from 'svelte/store';

export const searchInput = writable({
  fullText: {
      value: "",
      placeholder: "Tapez votre recherche..."
      }
    }
    )
