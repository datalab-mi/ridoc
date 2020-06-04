<script>
	import { searchInput, searchResults, index_name } from '../components/stores.js';

	let promise =  new Promise(()=>{});

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
		console.log(items)
		if (res.ok) {
			$searchResults = items[0]
			return items[0].length;
		} else {
			throw new Error('Oups');
		}
	}


	function handleSearch() {
		promise = search();
	}

</script>

<div class='search-bar'>

	<input type="search" bind:value={$searchInput.fullText.value}
	       placeholder={$searchInput.fullText.placeholder}>

	<button on:click={handleSearch}>
		Rechercher
	</button>

	{#if $searchInput.fullText.value!=''}
		<h1>La recherche est : {$searchInput.fullText.value}</h1>
	{/if}

	{#await promise}
		<p>...Attente de la requête</p>

	{:then length}
		<p>{length} documents trouvés</p>

	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

</div>

<style>
	.search-bar {
		width: 90%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,255,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}

</style>
