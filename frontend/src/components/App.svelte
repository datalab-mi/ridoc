<script>
	import { onMount } from 'svelte';

	import ResultItem from './ResultItem.svelte';
	import ResultList from './ResultList.svelte';
	import SearchBar from './SearchBar.svelte';
	import NewItem from './NewItem.svelte';

	import { searchInput, index_name } from './stores.js';

	let promise = search();

	async function search() {
		let value = $searchInput.fullText.value

		const res = await fetch("http://localhost/api/common/search",{
                        method: "POST",
                        body: JSON.stringify({
                               index_name: $index_name,
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

	function handleSearch() {
		promise = search();
	}

	function handleUpload() {

	}
</script>

<div>
<SearchBar/>

<button on:click={handleSearch} class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow">
  Rechercher
</button>

<NewItem />


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
