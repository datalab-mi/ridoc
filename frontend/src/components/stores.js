import { readable, writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchResults = writable({
  'hits':[],
  'threshold': 1
});

export const suggestEntry = writable([]);

export const index_name = writable('bld')
export const isReindex = writable(false)

export const list_synonym = writable([])

// The searchList const describes the search inputs
export const searchList  = [
  [
    {
    bool: "must",
    query: {"multi_match": {"fields":["titre", "question","reponse"], "query":"$value"}},
    value: "",
    type: "search",
    placeholder: "Recherche par mots clefs",
    innerHtml: "",
    style: "w-5/6 p-2",
    highlight: true
    }
  ]
]

// The const item describe the behaviour and the display of an item.
// The key should match with their elasticsearch counterparts
export const item = {
  multiple: false,
  accept: '.odt',
  inputs: [
    {
      key: 'titre',
      type: 'text',
      placeholder: 'NA',
      value: '',
      innerHtml: '',
      highlight: false,
      metadata: false
    },
    {
      key: 'question',
      type: 'text',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Question :</b>',
      highlight: true,
      metadata: false

    },
    {
      key: 'reponse',
      type: 'textarea',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Réponse :</b>',
      highlight: false,
      metadata: true
    },
    {
      key: 'pieces jointes',
      type: 'text',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Pièces jointes :</b>',
      highlight: true,
      metadata: false
    }
  ]
}
