import { writable, derived } from 'svelte/store';

export const promiseSearch = writable(Promise.resolve({ hits: [] }))
export const suggestEntry = writable([]);
