<script>
	import { envJson } from '../../components/user-data.store';
	import ResultItem from './ResultItem.svelte';
	import { list_logger } from '../../components/stores.js';
	import { promiseSearch } from './stores.js';
	import { itemJson } from '../../components/user-data.store';
	import {paginate, LightPaginationNav} from "svelte-paginate";


	let tris =["Trier par","Date","Titre","Score"];
	let triselect;
	let currentPage=1;
	let pageSize=3;
	let items = [];
	let threshold;
	let resultMessage;
	let message;
	let canBeChange;
	$: paginatedItems=paginate({items,pageSize,currentPage})
	$: canBeChange =  $itemJson.inputs.some((entry) => entry.metadata)

	$: message = $envJson.message ||  "Le document que vous recherchez a peu de chance de se trouver en dessous de cette bande. Veuillez contacter l'<b><a href='mailto:{$envJson.contact}?subject=Demande de consultation'> administrateur ✉️</a></b>."
	//let message = ($envJson.message === undefined) ? dafaultMessage : $envJson.message
	function add_bar(x) {
		items = [];
		threshold = ! (x.hits.some((x) => x._score !== 1)) //test if the request is ranked
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

	function trier(){
		console.log(items)
		if(triselect=='Date'){
			items.sort(function(a,b){
				if (a['_source']['date']==undefined){
					return 1
				}
				else if (b['_source']['date']==undefined){
					return -1
				}
				else{
				return (Date.parse(a['_source']['date'])-Date.parse(b['_source']['date']))}
			})

		}
		else if(triselect=="Titre"){
			items.sort(function(a,b){
				if (a['_source']['title']==undefined){
					return 1
				}
				else if(b['_source']['title']==undefined){
					return -1
				}
				else{
				return a['_source']['title'].localeCompare(b['_source']['title']);}
			})
		}
		else if (triselect=="Score"){
			items.sort(function(a,b){
				return b['_score']-a['_score']
			})
		}
		$: paginatedItems=paginate({items,pageSize,currentPage}) //on refait le découpage en page
		currentPage=1; //retour à la page initiale
	}
</script>
<div class="px-48 " >
	<select bind:value={triselect} class= "float-right px-6 py-2 " on:change="{trier}">
		{#each tris as tri }
			<option value={tri} class="bg-gray">{tri}</option>
		{/each}
	</select>
{#await $promiseSearch}
	<p>...Attente de la requête</p>
{:then result}
	{#if resultMessage}<p class="mb-4">{resultMessage}</p>{/if}
{/await}


{#if Object.keys($itemJson).length > 0}
	{#if items.length > 0}
		<div class="result-list">
		{#each paginatedItems as item (item.key)}
			
			{#if  item._id === "bar"}
				<section class="bar">
					<p>{@html message}</p>
				</section>
			{:else}
				<ResultItem  {... ( ({ _id, _source, _score, highlight }) => ({ _id, _source, _score, highlight, canBeChange }) )(item) }/>
			{/if}
		{/each}
		</div>
	{:else}
		<div class='bg-white p-4 pb-48 shadow mt-12'>
			
			<img src='./user/noresult.PNG' class="float-right">
			<h2 class="text-3xl font-bold my-4">Aucun résultat</h2>
			<p class="float-left text-xl ">Malheureusement aucun résultat n'est associé à votre recherche. Essayer de changer les mots-clés que vous avez utilisé.</p>
			
			
		</div>
	{/if}
{:else}
	<p>... Récuperation de la configuration</p>
{/if}

</div>
<div class="nav">
<LightPaginationNav totalItems="{items.length}" pageSize="{pageSize}" currentPage="{currentPage}" limit="{1}" showStepOptions="{true}" on:setPage="{(e)=> currentPage=e.detail.page}"/>
</div>
<style>
img{
	max-width: 20%;
	margin-top: 0;
	
	
}
select{
	background-color: #F0F0F0 ;
	border-bottom:solid black;
	margin-bottom: 4px;
}
.nav :global(.pagination-nav){
	background-color:transparent !important;
	box-shadow: none !important;
}

</style>
