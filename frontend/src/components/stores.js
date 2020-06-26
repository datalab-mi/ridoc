import { writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchInput = writable({
  content: {
    value: "",
    type: "text",
    placeholder: "Recherche par mots clefs",
    innerHtml: ""
    },
  author: {
    value: "",
    type: "text",
    placeholder: "Paul Dupond, Anne-Marie",
    innerHtml: "Nom ou Prénom"

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
    innerHtml: "Jusqu'à : "
  }
  }
)

export const searchResults = writable({
  'hits':[],
  'threshold':1
});

export const index_name = writable('iga')
export const isReindex = writable(false)

export const list_synonym = writable([])
export const list_expression = writable([])
