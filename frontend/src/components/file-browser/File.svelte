<script>
	import { list_files, list_logger } from '../stores.js';
	import { files } from '../utils.js';
	import FileRow from './FileRow.svelte';
	import VirtualList from '../VirtualList.svelte';
  import { onDestroy } from 'svelte'

	export let baseDir
	export let meta

	let GetPromise = new Promise(()=>{})
	let PutPromise = new Promise(()=>{})

	let isAdd = false
	let readonly = true
	let send = false

	let start
	let end
	let key = "name"
	let file = {'name': ""}

	let list_files_filter;
	let filterRow = Object.assign({}, ...meta.map((x) => ({[x.key]: ''})));

	const keys_to_filter = meta.filter(item => item.type == 'text').map(item => item.key);
	GetPromise = handleFiles()

	async function handleFiles() {
		const res = await files('GET', baseDir)
		//const data = await res.json()
		$list_files = await res.json()//data.map(element => Object.assign({}, ...keys_to_filter.map(key => ({[key]: element[key]}))))
		return res.status
	}


	async function handleSubmit() {
		console.log(file[0])
		filterRow.name = file[0].name
		files('PUT', baseDir, file[0])
			.then(() => {
				list_logger.concat({level: "success", message: `Fichier  ajouté avec succès!`, ressource: "files"})
			})
			.catch(err => {
				list_logger.concat({level: "error", message: err, ressource: "files"})
			})

		GetPromise = handleFiles()
		// reset filter and file
		filterRow = Object.assign({}, ...meta.map((x) => ({[x.key]: ''})))
		file = {'name': ""}

	}

	function handleAdd() {
		isAdd = !isAdd;
	}

	$: { // filter $list_files with filterRow on its keys (expressionA, expressionB...)
		console.log($list_files)
		list_files_filter = $list_files.filter((item) => keys_to_filter.every((key) => item[key].toLowerCase().includes(filterRow[key].toLowerCase())))

	}

onDestroy(() => $list_files = [])


</script>


<div class='containerVL'>
	{#await GetPromise}
	<p>...Attente de la requête</p>
	{:then status}


		<div class="inline-flex bg-{(isAdd) ? 'white': 'gray'}-200 w-full">
			<div class="inline-flex w-5/6">
			{#each meta as {key, type, placeholder, value, innerHtml, size} }
				<div class="flex-grow w-{size} text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
					<input type="search" bind:value={filterRow[key]} placeholder={(isAdd) ? '': placeholder} >
				</div>
			{/each}
			</div>

			<div class="flex-initial w-1/6 px-4 py-2 m-2">
				{#if (isAdd)}
					{#if (file.name === "")}
					<label for="pjUplaod" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
					Choisir un fichier
					</label>
					<input id="pjUplaod" class="fileUpload" type="file" bind:files={file}>

					{:else}
						<button on:click={handleSubmit} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
							<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
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

		<VirtualList items={list_files_filter} {key} let:item>
			<FileRow {item} {meta} {baseDir} {key}/>
		</VirtualList>

	{:catch error}
		{#if error.satus === 404}
			<p style="color: red">Pas de pièces jointes</p>

		{:else}
			<p style="color: red">{error.message}</p>
		{/if}
	{/await}

</div>

<style>

	.container {
	width: 90%;
	}

	.containerVL {
	min-height: 200px;
	height: calc(60vh)
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

	.fileUpload {
	 display: none;
	}

</style>
