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

promise = search();

</script>

<div class='search-bar'>

	<div class="flex mb-4">
		<div class="w-2/3 px-2" >
			<input type="search" bind:value={$searchInput.fullText.value}
			       placeholder={$searchInput.fullText.placeholder}
						  class="bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal">
			</div>
			<div class="w-1/3 px-2" >
				<button on:click={handleSearch} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
					<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
					<span>Rechercher</span>
				</button>
			</div>

	</div>

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
