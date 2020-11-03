<script>
	import { searchResults, suggestEntry,  index_name, itemConfig, searchList, promiseSearch } from '../components/stores.js';
	import { config, format2ES, search } from '../components/utils.js';

	import SearchInput from  '../components/SearchInput.svelte';

	let promiseSuggest =  new Promise(()=>{})
	let getInit =  new Promise(()=>{})
	//let promiseSearch =  new Promise(()=>{})
	console.log("*Searchbar*")
	console.log($promiseSearch)

	let body

	async function suggest() {
		const res = await fetch("/api/common/suggest",{
												method: "POST",
												body: JSON.stringify({
															 index_name: $index_name,
															 content: $searchList.content.value,
														 })
													 });

		const result = await res.json();
		//console.log(itemConfigs)
		if (res.ok) {
			$suggestEntry = result
			return "ok";
		} else {
			throw new Error('Oups');
		}
	}

	function handleSearch() {
		console.log("handleSearch")
		body =  format2ES($itemConfig, $searchList, $index_name)
		$promiseSearch = search(body)
	}

	function handleSuggest() {
		console.log('handleSuggest')
		promiseSuggest = suggest()
	}

	function handleSuggestChosen(v) {
		console.log('handleSuggestChosen')

		//searchList.content.value = e.target.innerHTML
		$searchList.content.value = v
		$suggestEntry = []
	}


</script>
<div class='search-bar' on:keyup={e=>e.key==="Enter" && handleSearch()}>

{#if $searchList.length > 0}

	{#each $searchList as row, i }
	<div class="flex mb-4">

		{#each row as {bool, query, value, type, placeholder, innerHtml, style}, j}
			{#if (i === 0) && (j === 0) }
				<div class="w-1/6 p-2" >
					<button on:click={handleSearch} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded inline-flex itemConfigs-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
						<span>Rechercher</span>
					</button>
				</div>
			{/if}

			<SearchInput bind:value={value} {type} {placeholder} {innerHtml} {style} />
		{/each}
		</div>

	{/each}

{#await $promiseSearch}
	<p>...Attente de la requête</p>

{:then result}
	{#if ("hits" in result) }
		<p>{result.hits.length} documents retournés</p>
	{/if}

{/await}

{:else}
<p>...Attente de la config</p>

{/if}

</div>

<style>
	.search-bar {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,255,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}

	#suggest {
			z-index: 2;
			position: absolute;
			background-color: rgba(255,255,255,1);
		}
	</style>
