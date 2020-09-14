import { readable, writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const searchList = writable([
  [
    {
    bool: "must",
    clause: "multi_match",
    fields: ["titre", "content"],
    query: "",
    type: "search",
    placeholder: "Recherche par mots clefs",
    innerHtml: "",
    style: "w-3/4 p-2",
    highlight: true
    }
  ]
]
)

export const searchResults = writable({
  'hits':[],
  'threshold':1
});

export const suggestEntry = writable([]);

export const index_name = writable('iga')
export const isReindex = writable(false)

export const list_synonym = writable([])

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
      metadata: true
    },
    {
      key: 'content',
      type: 'textarea',
      placeholder: 'NA',
      value: '',
      innerHtml: '',
      highlight: '<b>Content :</b>',
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
