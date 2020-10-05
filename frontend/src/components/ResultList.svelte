<script>
import { searchResults } from '../components/stores.js';
import { config } from '../components/utils.js';

import { onMount } from 'svelte';

import ResultItem from '../components/ResultItem.svelte';
import VirtualList from '../components/VirtualList.svelte';
let start;
let end;
let height = '90%';
let items = []
let threshold


let promise = config('item.json')

$: {
	let i = 0;
	items = [];
	threshold = true
	for (const hits of $searchResults.hits){
		let item = {}
		if (hits._score < $searchResults.threshold && threshold){
			threshold = false
			item = {'_id': "bar"}
		} else {
			item = hits
		}

	item['key'] =  Math.random() * 1e6  | 0 // Choose random key
	items.push(item)
	}
	//items.splice(i, 0, "bar")
}

</script>

{#await promise}
<p>... Récuperation de la configuration</p>
{:then meta}
{#if items.length > 0}
	<div class='result-list'>
	{#each items as item (item.key)}
		{#if  item._id === "bar"}
			<div class="bar">
				<p>Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande. Nous vous recommandons de contacter
					<a href="mailto://iga@interieur.gouv.fr?subject=Demande_de_consultation">l'administrateur</a>
				</p>
			</div>
		{:else}
			<ResultItem meta={JSON.parse(JSON.stringify(meta.inputs))} {...item}/>
		{/if}
	{/each}
	</div>
{/if}
{/await}

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
