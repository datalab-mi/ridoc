import { derived, writable } from 'svelte/store';
import { httpClient } from '../components/utils';

/**
 * Renvoie un store contenant les donnée de l'utilisateur.
 */
export const userData = (() => {

	const http = httpClient();

	/**
	 * Récupère les données.
	 * TODO adapter au client (ne pas appeler env.json)
	 * 
	 * @return Promise contenant les données
	 */
	const fetchUserData = () => http.fetchJson('user/env.json');

	/**
	 * Met à jour la valeur du store avec les données.
	 * @param  set  fonction 'set' du store
	 */
	const refreshData = async (set) => fetchUserData().then(data => set(data));

	const { subscribe, set } = writable({}, (set) => {
		refreshData(set);
		return () => console.debug('userData: no more subscribers');
	});

	return {
		subscribe,
		refresh: () => refreshData(set)
	}

})();

/**
 * Renvoie un store correspondant aux préférences de l'utilisateur.
 */
export const userPreferences = derived(userData, ($userData, set) => {
	set($userData.preferences || {});
	return () => console.debug('userPreferences: no more subscribers');
});