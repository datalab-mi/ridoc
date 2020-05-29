<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';

	import ResultItem from '../components/ResultItem.svelte';
	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';
	import UploadFiles from '../components/NewItem.svelte';

	import { searchInput, index_name } from '../components/stores.js';

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

<button on:click={handleSearch}>
	Rechercher
</button>

<UploadFiles />


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
