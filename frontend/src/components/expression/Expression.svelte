<script>
	import { index_name, list_expression  } from '../stores.js';
	import SynonymRow from './ExpressionRow.svelte';
	import VirtualList from '../VirtualList.svelte';

	export let filename;

	let GetPromise;
	let PutPromise = new Promise(()=>{});

	let list_expression_filter;

	let filterValue = '';

	let isAdd = false;
	let readonly = true;
	let send = false;

	let start;
	let end;

	let key;


	async function expression(method) {
		let res;
		if (method == 'GET') {
			res = await fetch(`/api/common/expression`,
					{method: 'GET'});
		} else if (method == 'PUT') {
			key = '0';
			res = await fetch(`/api/admin/expression/${key}`, {
					method: 'PUT',
					body: JSON.stringify([{'value': key}, {'value': filterValue}])});
		}
		$list_expression = await res.json();
		if (res.ok)  {
			return res.status
		} else {
			console.log('error')
			throw new Error('Oups');
		}
	}

	GetPromise = expression('GET')

function handleSubmit() {
	PutPromise = expression('PUT')
	filterValue = ''
}

function handleAdd() {
	isAdd = !isAdd;
}


$: {list_expression_filter = $list_expression.filter(item =>  (item.value.includes(filterValue)))}

</script>


<div class='containerVL'>
	{#await GetPromise}
	<p>...Attente de la requête</p>
	{:then status}

		<div class="inline-flex bg-{(isAdd) ? 'white': 'gray'}-200 w-full">

			<div class="flex-initial w-4/5 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
				<input type="search" bind:value={filterValue} placeholder={(isAdd) ? 'Direction du numérique': 'recherche'} >
			</div>
			<div class="flex-initial w-1/5 px-4 py-2 m-2">
				{#if (isAdd)}
					{#if  (filterValue != '') }
						<button on:click={handleSubmit} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
							<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
							<span>SOUMETTRE</span>
						</button>
					{:else}
						<button disabled class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
							<svg class="fill-curr
							ent w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
							<span>SOUMETTRE</span>
						</button>
					{/if}
					<button on:click="{() => isAdd = !isAdd}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-2 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zM11.4 10l2.83-2.83-1.41-1.41L10 8.59 7.17 5.76 5.76 7.17 8.59 10l-2.83 2.83 1.41 1.41L10 11.41l2.83 2.83 1.41-1.41L11.41 10z"/></svg>
					</button>

				{:else}
				<button on:click={handleAdd} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
					<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M11 9h4v2h-4v4H9v-4H5V9h4V5h2v4zm-1 11a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>
					<span>AJOUTER</span>
				</button>
				{/if}
			</div>
		</div>

		<VirtualList items={list_expression_filter} let:item>
			<SynonymRow expressionA={item.key} expressionB={item.value} />
		</VirtualList>



	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

</div>

	<!--
	{#if (isAdd)}
		<div class='synonym-add'>

		{#each meta as {key, type, placeholder, value, innerHtml}, i }
			<label> {@html innerHtml}
			<input type='text' bind:value={value} {placeholder}/>
			</label>
			<br>
		{/each}

		{#if meta.every((e) => e.value != '')}

			<button on:click={handleSubmit} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
				<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
				<span>SOUMETTRE</span>
			</button>
		{:else}
			<button disabled class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
				<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
				<span>SOUMETTRE</span>
			</button>
		{/if}
	</div>
	{/if}


	{#await PutPromise}
	{:then status}
		{#if status == 201 }
			<p style="color: green">{key} crée</p>
		{:else if status == 200 }
			<p style="color: blue" >{key} modifié</p>
		{:else}
			<p>Status {status} non connu</p>
		{/if}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

</div>
//-->




<style>

.container {
	width: 90%;
}

.containerVL {
	min-height: 200px;
	height: calc(100vh - 15em);
}


	.synonym-list {
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,0,0,1);
		width: 60em;
		overflow: auto;
		margin: 10px
	}

	.synonym-add {
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,0,0,1);
		flex-grow: 1;
		height: 30vh;
		width: 30em;
		margin: 10px


	}

	.value {
		width: 80%
	}

	.key {
		width: 20%
	}
	th input
	{
    width: 100%;
	}
	input {
		border:none;
		width: 90%;
		resize: none;
		background-color: inherit;
	 }
	table {
  border-collapse: separate;
	table-layout: fixed;
  width: 100%;
	}

	th, td {
  text-align: left;
  padding: 8px;
	white-space:wrap;
}

	thead th {
		 position: sticky; top: 0;
	 }



</style>
