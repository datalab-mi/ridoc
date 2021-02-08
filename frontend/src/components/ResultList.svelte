<script>
	import { cssProps } from '../common/css-props.action';
	import { userTheme } from '../common/theme.store';
	import ResultItem from '../components/ResultItem.svelte';
	import { itemConfig, list_logger, promiseSearch } from '../components/stores.js';
	import { userData } from '../common/user-data.store';

	const bgColorProp = '--search-results-bg-color';
	const styleProps = {};

	let items = [];
	let threshold;
	let resultMessage;

	function add_bar(x) {
		items = [];
		threshold = true;
		for (const hits of x.hits) {
			hits['key'] = (Math.random() * 1e6) | 0; // Choose random key
			if (hits._score < x.r_threshold && threshold) {
				threshold = false;
				items.push({ _id: 'bar', key: -1 });
			}
			items.push(hits);
		}
	}

	function getResultMessage(results) {
		if ('hits' in results) {
			const nb = results.hits.length;
			switch (nb) {
				case 0: return 'Aucun résultat ne correspond à votre recherche';
				case 1: return '1 résultat correspond à votre recherche';
				default: return nb + ' résultats correspondent à votre recherche';
			}
		}
		return undefined;
	}

	// reactive statement, add_bar function is called whenever the promise changes
	$: {
		styleProps[bgColorProp] =
			$userTheme.search &&
			$userTheme.search.results &&
			$userTheme.search.results.backgroundColor
				? $userTheme.search.results.backgroundColor
				: undefined;
		
		$promiseSearch
			.then((searchResults) => {
				add_bar(searchResults);
				resultMessage = getResultMessage(searchResults);
			})
			.catch((err) => {
				list_logger.concat({
					level: 'error',
					message: err,
					ressource: 'search',
				});
			});
	}
</script>

{#await $promiseSearch}
	<p>...Attente de la requête</p>
{:then result}
	{#if resultMessage}<p class="mb-4">{resultMessage}</p>{/if}
{/await}

{#if Object.keys($itemConfig).length > 0}
	{#if items.length > 0}
		<div class="result-list" use:cssProps={styleProps} style="background-color: var({bgColorProp})">
		{#each items as item (item.key)}
			{#if  item._id === "bar"}
				<div class="bar">
					<p>Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande. Veuillez contacter l'<b><a href="mailto:{$userData.contact}?subject=Demande de consultation"> administrateur ✉️ </a></b>.
					</p>
				</div>
			{:else}
				<ResultItem  {... ( ({ _id, _source, _score, highlight }) => ({ _id, _source, _score, highlight }) )(item) } />
			{/if}
		{/each}
		</div>
	{/if}
{:else}
	<p>... Récuperation de la configuration</p>
{/if}


<style>
	.result-list {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		padding: 1em;
		margin: 0 0 1em 0;
		min-height: 200px;
	}
	.bar {
		border: 1px solid #aaa;
		border-radius: 2px;
		padding: 1em;
		margin: 1em 1em 1em 1em;
	}
</style>