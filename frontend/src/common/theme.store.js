import { derived, writable } from 'svelte/store';
import { userPreferences } from './user-data.store';

/**
 * Renvoie un store contenant le thème de l'application
 * TODO alimenter
 */
export const appTheme = writable({ backgroundColor: 'white' }, () => {
	return () => console.debug('appTheme: no more subscribers');
});

/**
 * Renvoie un store correspondant au thème de l'application personnalisé pour l'utilisateur.
 */
export const userTheme = derived([appTheme, userPreferences], ([$appTheme, $userPreferences], set) => {
	const userTheme = $userPreferences && $userPreferences.theme ? $userPreferences.theme : {};
	set({ ...($appTheme || {}), ...userTheme });
	return () => console.debug('userTheme: no more subscribers');
});