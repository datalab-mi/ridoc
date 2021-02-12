import { writable } from 'svelte/store';
import { httpClient } from '../utils';

/**
 * Renvoie un store contenant la configuration des champs de résultats de recherche.
 */
export const itemConfig = (() => {

	const http = httpClient();

	/**
	 * Récupère les données.
	 * 
	 * @return Promise contenant les données
	 */
	const fetchItemConfig = () => http.fetchJson('user/item.json');

	/**
	 * Met à jour la valeur du store avec les données.
	 * @param  set  fonction 'set' du store
	 */
	const refreshData = async (set) => fetchItemConfig().then(data => set(data));

	const { subscribe, set } = writable({}, (set) => {
		refreshData(set);
		return () => console.debug('itemConfig: no more subscribers');
	});

	return {
		subscribe,
		refresh: () => refreshData(set)
	}

})();