import { writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchInput = writable({
  content: {
    value: "",
    type: "text",
    placeholder: "Saisissez votre recherche...",
    innerHtml:""
    },
  author: {
    value: "",
    type: "text",
    placeholder: "Paul Dupond, Anne-Marie",
    innerHtml:"Auteurs :"

    }
  }
)

export const searchResults = writable([]);

export const index_name = writable('iga')

export const list_synonym = writable([])
export const list_expression = writable([])
