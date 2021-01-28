<script>
import { promiseSearch, itemConfig, userData } from '../components/stores.js';
import { format2ES } from '../components/utils.js';

import { onMount } from 'svelte';

import ResultItem from '../components/ResultItem.svelte';
import VirtualList from '../components/VirtualList.svelte';

let start;
let end;
let height = '90%';
let items = [];
let threshold;

function add_bar(x) {
	let i = 0;
	items = [];
	threshold = true
	for (const hits of x.hits){
		let item = {}
		if (hits._score < x.r_threshold && threshold){
			threshold = false
			item = {'_id': "bar"}
		} else {
			item = hits
		}

	item['key'] =  Math.random() * 1e6  | 0 // Choose random key
	items.push(item)
	}
}

// reactive statement, add_bar function is called whenever the promise changes
$: $promiseSearch.then((searchResults) => {add_bar(searchResults)})

</script>

	{#if Object.keys($itemConfig).length > 0}
		{#if items.length > 0}
			<div class='result-list'>
			{#each items as item (item.key)}
				{#if  item._id === "bar"}
					<div class="bar">
						<p>Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande. Veuillez contacter l'<b><a href="mailto:{$userData.contact}?subject=Demande de consultation">administrateur</a></b>.
						</p>
					</div>
				{:else}
					<ResultItem  {...item}/>

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
		box-shadow: 2px 2px 8px rgba(255,0,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
		min-height: 200px;
	}
.bar {
	border: 1px solid #aaa;
	border-radius: 2px;
	box-shadow: 2px 2px 8px rgba(0,255,0,1);
	padding: 1em;
	margin: 1em 1em 1em 1em;
}
</style>
