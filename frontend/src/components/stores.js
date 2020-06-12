import { writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchInput = writable({
  fullText: {
      value: "",
      placeholder: "Tapez votre recherche..."
      }
    }
    )
export const searchResults = writable([]);

export const index_name = writable('iga')

export const list_synonym = writable([])
export const list_expression = writable([])
