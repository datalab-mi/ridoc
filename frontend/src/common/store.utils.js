import { writable } from 'svelte/store';

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