<script>
	import { index_name } from './stores.js';
	import { index } from './utils.js'

	export let _id;
	export let _source;
	export let highlight = {'content':''};

	$: filename = _id.replace(/\+/g, " ")
	$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`

	let promiseDelete = new Promise(()=>{});
	let promiseIndex = new Promise(()=>{});

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
		promiseIndex = index( $index_name, filename, 'DELETE')
	}

	function handleUpdate() {
		console.log(`Update ${_id.replace(/\+/g, " ")}`)
	}
</script>

<section class='result-item'>

	<a href="{url}" target="_blank">
	<h2>{_source.title}</h2>
	</a>

	<p>{@html highlight.content}</p>
	<p>Auteurs : {_source.author}</p>
	<p>Date : {_source.date}</p>

	<button on:click={handleDelete}>
		SUPPRIMER
	</button>

	<button on:click={handleUpdate}>
		MODIFIER
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

	{#await promiseIndex}
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

</style>
