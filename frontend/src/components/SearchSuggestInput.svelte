<script>
	import AutoComplete from 'simple-svelte-autocomplete';
	import { onMount, onDestroy } from 'svelte';
	import { userData } from './stores.js';
	import { httpClient, USER_API } from './utils.js';
	import { BehaviorSubject, of } from 'rxjs'
	import { debounceTime, distinctUntilChanged, filter, share, switchMap, take, tap } from 'rxjs/operators'

	export let innerHtml = '';
	export let style = '';
	export let placeholder = '';
	export let value = '';

	const http = httpClient();

	// constantes
	const inputId = "suggest-" + Math.floor(Math.random() * 1000);
	const minCharactersToSuggest = 4;
	const valueFieldName = 'text';
	const labelFieldName = 'text';
	const inputDelayMs = 250;

	// méthodes qui permettent de synchroniser le champ 'value' et le texte du champ <input />
	let onSuggestionInput;
	let onSuggestionSelected;

	onMount(() => {
		onSuggestionInput = (event) => (value = event.target.value);
		onSuggestionSelected = (selected) => (value = selected[valueFieldName]);

		const nestedInput = document.getElementById(inputId);
		nestedInput && nestedInput.addEventListener('input', onSuggestionInput);
	});
	
	onDestroy(() => {
		const nestedInput = document.getElementById(inputId);
		nestedInput && nestedInput.removeEventListener('input', onSuggestionInput);
	});
	
	/**
	 * fonction de mapping suggestion => keyword
	 * Le but initial du composant est de conserver uniquement les valeurs contenant le texte du champ <input />,
	 * ce qui est inadapté aux suggestions. C'est pourquoi on renvoie ici le texte du champ.
	 */
	const keywordsFunction = (/* suggestion */) => value || '';

	// RxJS ------------------------------------------------------------- START
	
	/** équivalent d'un store 'writable' (sans valeur initiale) */
	const searchTrigger = new BehaviorSubject();
	
	/**
	 * équivalent d'un store 'readable', fournit les suggestions.
	 * 
	 * besoin :
	 * éviter de mitrailler le serveur si l'utilisateur tape plusieurs caractères rapidement
	 * 
	 * Toute la 'magie' vient des opérateurs du pipe (doc conseillée) :
	 * - filter               : ne laisse pas passer null ou undefined
	 * - distinctUntilChanged : une seule émission pour 2 valeurs successives identiques
	 * - debounceTime         : garde une valeur s'il se passe un temps suffisant avant la prochaine
	 * - switchMap            : permet ici de se désinscrire de l'ancien observable avant de transformer le nouveau
	 *                          + couplé à un appel passant par 'fromFetch' pour pouvoir annuler les anciennes requêtes
	 * - share                : évite de lancer une requête par souscription
	 */
	const searchObservable = searchTrigger.asObservable().pipe(
		filter(v => v !== null && v !== undefined),
		distinctUntilChanged(),
        debounceTime(inputDelayMs),
        switchMap(v => searchSuggestions(v)),
		share()
	);
	
	/**
	 * fonction "asynchrone" (RxJS) de recherche des suggestions.
	 * Le serveur n'est appelé qu'à partir d'une certaine longueur de chaîne.
	 * 
	 * note : on n'utilise pas l'option 'minCharactersToSearch' car elle fonctionne mal avec la validation sur 'Enter',
	 * en effet la première valeur de la dernière liste de suggestions est utilisée, ce n'est pas ce qu'on veut.
	 * 
	 * @return observable contenant les suggestions
	 */
	const searchSuggestions = (inputText) => {
		console.debug('MAJ des suggestions');
		return !inputText || inputText.length < minCharactersToSuggest
			? of([])
			: http.rxjs.fetchJson(`${USER_API}/suggest`, {
					method: 'POST',
					body: JSON.stringify({
						index_name: $userData.index_name,
						content: inputText,
					})
			})
	};
	
	/**
	 * fonction asynchrone de recherche des suggestions.
	 * Crée une Promise contenant la prochaine valeur de l'observable, puis provoque la recherche.
	 */
	const searchFunction = async (inputText) => {
		const deferred = searchObservable.pipe(take(1)).toPromise();
		searchTrigger.next(inputText);
		return deferred;
	};

	// RxJS --------------------------------------------------------------- END
</script>

<div class={style}>
	<!-- svelte-ignore a11y-label-has-associated-control -->
	<label class="suggestion">
		{@html innerHtml}
		<AutoComplete
			{placeholder}
			{inputId}
			inputClassName="bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal"
			{searchFunction}
			{keywordsFunction}
			{labelFieldName}
			{valueFieldName}
			hideArrow={true}
			noResultsText=""
			onChange={onSuggestionSelected}
		/>
	</label>
</div>

<style>
	.suggestion :global(.autocomplete) { width: 100% }
</style>