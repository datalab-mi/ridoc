import { readable, writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchResults = writable({
  'hits':[],
  'threshold': 1
});

export const suggestEntry = writable([]);

export const index_name = writable('iga')
export const isReindex = writable(false)

export const list_synonym = writable([])

// The searchList const describes the search inputs
export const searchList  = [
  [
    {
    bool: "must",
    query: {"multi_match": {"fields":["titre", "content"], "query":"$value"}},
    value: "",
    type: "search",
    placeholder: "Recherche par mots clefs",
    innerHtml: "",
    style: "w-5/6 p-2",
    highlight: true
    }
  ],
  [
    {
    bool: "filter",
    query: {"match": {"fields":"author","query":"$value"}},
    value: "",
    type: "search",
    placeholder: "Paul Dupond, Anne-Marie",
    innerHtml: "Nom ou Prénom",
    style: "w-3/4 p-2",
    highlight: true
    },
    {
    bool: "filter",
    query: {"range": {"date": {"gte":"$value"}}},
    value: "",
    type: "date",
    innerHtml: "A partir de : ",
    style: "w-3/4 p-2",
    highlight: true
    },
    {
    bool: "filter",
    query: {"range": {"date": {"gte":"$value"}}},
    value: "",
    type: "date",
    innerHtml: "Jusqu'à : ",
    style: "w-3/4 p-2",
    highlight: true
    }
  ]
]

// The const item describe the behaviour and the display of an item.
// The key should match with their elasticsearch counterparts
export const item = {
  multiple: false,
  accept: '.pdf',
  inputs: [
    {
      key: 'title',
      type: 'textarea',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Titre :</b>',
      highlight:  true,
      metadata: true
    },
    {
      key: 'content',
      type: 'textarea',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Contenu :</b>',
      highlight:  true,
      metadata: false
    },
    {
      key: 'author',
      type: 'text',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Auteurs :</b>',
      highlight: true,
      metadata: true

    },
    {
      key: 'date',
      type: 'date',
      placeholder: 'NA',
      value: '',
      innerHtml: '<b>Date :</b>',
      highlight: false,
      metadata: true
    }
  ]

}
