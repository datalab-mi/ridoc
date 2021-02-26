import { writable } from 'svelte/store';
import { httpClient } from './utils';

/**
 * Fonction de génération d'un store très simple qui contient un booléen pour gérer l'ouverture/fermeture.
 * valeurs : true = ouvert, false = fermé
 *
 * @param  initial  (boolean) valeur initiale
 */
export function createOpenCloseStore(initial = false) {
	const { subscribe, set, update } = writable(!!initial);

	return {
		subscribe,
		toggle: () => { update(value => !value) },
		open:   () => { set(true) },
		close:  () => { set(false) }
	};
}


/**
 * Renvoie un store contenant les donnée de l'utilisateur.
 */
export const userData = (fileJson, initialValue = {}) => {

	const http = httpClient();

	/**
	 * Récupère les données.
	 * TODO adapter au client (ne pas appeler env.json)
	 *
	 * @return Promise contenant les données
	 */
	const fetchdataJson = () => http.fetchJson(`user/${fileJson}`);

	/**
	 * Met à jour la valeur du store avec les données.
	 * @param  set  fonction 'set' du store
	 */
	const refreshData = async (set) => fetchdataJson().then(data => set(data));

	const { subscribe, set } = writable(initialValue, (set) => {
		refreshData(set);
	});

	return {
		subscribe,
    set,
		refresh: () => refreshData(set)
	}
}
