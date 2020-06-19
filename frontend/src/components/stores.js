import { writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchInput = writable({
  content: {
    value: "",
    type: "text",
    placeholder: "Saisissez votre recherche...",
    innerHtml: ""
    },
  author: {
    value: "",
    type: "text",
    placeholder: "Paul Dupond, Anne-Marie",
    innerHtml: ""

  },
  from_date: {
    value: "",
    type: "text",
    placeholder: "01/01/2018",
    innerHtml: "A partir de : "

  },
  to_date: {
    value: "",
    type: "text",
    placeholder: "01/01/2018",
    innerHtml: "Jusqu'à"
  }
  }
)

export const searchResults = writable([]);

export const index_name = writable('iga')

export const list_synonym = writable([])
export const list_expression = writable([])
