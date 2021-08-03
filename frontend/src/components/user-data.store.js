import { derived, writable } from 'svelte/store';
import { httpClient } from './utils';
import { userData } from './store.utils';


// retrieve json from static folder
// General environment variables
export const envJson = userData("env.json")

// Define result items display
export const itemJson = userData("item.json", {inputs: []})

// Define search bar display
export const searchJson = userData("search.json", [])

export const searchRateJson =userData("searchRate.json")

/**
 * Renvoie un store correspondant aux préférences de l'utilisateur.
 */
export const userPreferences = derived(envJson, ($envJson, set) => {
	set($envJson.preferences || {});
	return () => console.debug('userPreferences: no more subscribers');
});
