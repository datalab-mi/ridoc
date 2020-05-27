<script>
	import { index_name } from './stores.js';
	import { index, upload } from './utils.js'

	export let _id;
	export let _source;
	export let highlight = {'content':''};

	$: filename = _id.replace(/\+/g, " ")
	$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`

	let promiseDelete = new Promise(()=>{});
	let promiseDeleteIndex = new Promise(()=>{});

	let promiseUpload = new Promise(()=>{});
	let promiseIndex = new Promise(()=>{});

	let readonly = true

	async function remove() {
		const res = await fetch(`http://localhost/api/common/${filename}`,
				{method: 'DELETE'});
		if (res.ok || res.status == 404) {
			return res.status
		} else {
			console.log('error')
			throw new Error('Oups');
		}
	}

	function handleDelete() {
		console.log(`Delete ${_id.replace(/\+/g, " ")}`)
		promiseDelete = remove()
		promiseDeleteIndex = index( $index_name, filename, 'DELETE')
	}

	async function handleSave() {
		console.log(`Save ${_id.replace(/\+/g, " ")}`)
		readonly = !readonly
		const meta = [
			{'key': 'title' , 'value': _source.author},
			{'key': 'author' , 'value': _source.author},
			{'key': 'date' , 'value': _source.date},
			]
		const files = [{'name': _id}]

		promiseUpload = await upload(meta, files)
		promiseIndex = await index($index_name, files[0].name, 'PUT');
	}
</script>

<section class='result-item'>

	<h2>
		<textarea class='title' type='text' bind:value={_source.title} readonly={readonly}/>
	</h2>

	{#if highlight.content != ''}
		<p> &laquo; {@html highlight.content} &raquo; </p>
	{/if}

	<label>Auteurs :
	<input type='text' bind:value={_source.author} readonly={readonly}/>
	</label>
	<label>Date :
	<input type='text' bind:value={_source.date} readonly={readonly}/>
	</label>

	<button on:click={handleDelete}>
		SUPPRIMER
	</button>

	{#if readonly}
		<button on:click="{() => readonly = !readonly}">
			MODIFIER
		</button>
	{:else}
		<button on:click={handleSave}>
			SAUVER
		</button>
	{/if}

	<button on:click="{window.open(url,'_blank')}">
		CONSULTER
	</button>

	{#await promiseDelete}
	{:then status}
		{#if status == 204 }
			<p style="color: green"> Le fichier {filename} est supprimé</p>
		{:else if status == 404 }
			<p style="color: red" > {filename} n'existe pas</p>
		{:else}
			<p>Status {status} non connu</p>
		{/if}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

	{#await promiseDeleteIndex}
	{:then status}
		{#if status == 200 }
			<p style="color: green"> {filename} désindexé</p>
		{:else if status == 404 }
			<p style="color: red" > {filename} pas dans l'index</p>
		{:else}
			<p>Status {status} non connu</p>
		{/if}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}


	{#await promiseUpload}
  {:then status}
    {#if status == 201 }
      <p style="color: green">{filename} crée</p>
    {:else if status == 200 }
      <p style="color: blue" >{filename} modifié</p>
    {:else}
      <p>Status {status} non connu</p>
    {/if}
  {:catch error}
  	<p style="color: red">{error.message}</p>
  {/await}

  {#await promiseIndex}
  {:then status}
    {#if status == 201 }
      <p style="color: green">{filename} indexé</p>
    {:else if status == 200 }
      <p style="color: blue" >{filename} modifié dans l'index</p>
    {:else}
      <p>Status {status} non connu</p>
    {/if}
  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
</section>

<style>
	.result-item {
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0,0,255,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
	mark {
  background-color: blue;
  color: black;
	}

	a {
	display: block;
	margin: 0 0 1em 0;
	}

 input,textarea {
	 border:none;
	 width: 90%;
	 resize: none;
  }

 .title {
	 color: blue;
	 font-weight: bold;
	 margin: 0;
	 padding: 0;

 }
</style>
