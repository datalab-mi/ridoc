<script>
	import { onMount } from 'svelte';

	import ResultItem from './ResultItem.svelte';
	import ResultList from './ResultList.svelte';
	import SearchBar from './SearchBar.svelte';

	import { searchInput } from './stores.js';

	export let index_name
	let promise = search();

	async function search() {
		let value = $searchInput.fullText.value

		const res = await fetch("http://localhost/api/common/search",{
                        method: "POST",
                        body: JSON.stringify({
                               index_name: index_name,
                               value: value
                             })
													 });


		const items = await res.json();

		if (res.ok) {
			return items;
		} else {
			throw new Error('Oups');
		}
	}

	function handleClick() {
		promise = search();
	}
</script>

<div>
<SearchBar/>

<button on:click={handleClick}>
	Rechercher
</button>

{#await promise}
	<p>...Traitement de la requête</p>

{:then items}
<ResultList>
{#each items[0] as item, i}
	<ResultItem {...item}/>
{/each}
</ResultList>

{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
</div>
