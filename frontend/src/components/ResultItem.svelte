<script>
	import BaseItem from './BaseItem.svelte'
	import PutItem from './PutItem.svelte'

	import { index_name } from './stores.js';
	import { index, upload } from './utils.js'

	export let _id;
	export let _source;
	export let highlight = {'content':''};

	$: filename = _id.replace(/\+/g, " ")
	$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`

	let promiseDelete = new Promise(()=>{});
	let promiseDeleteIndex = new Promise(()=>{});

	let readonly = true;
	let send = false;
	let meta;

	let isResult = true;

	$: {
			meta = [
	        {
	          key: 'title',
	          type: 'text',
	          placeholder: 'NA',
	          value: _source.title,
	          innerHtml: ''
	        },
	        {
	          key: 'author',
	          type: 'text',
	          placeholder: 'NA',
	          value: _source.author,
	          innerHtml: 'Auteurs :'
	        },
	        {
	          key: 'date',
	          type: 'date',
	          value: _source.date,
	          innerHtml: 'Date :'
	        }
	            ]
	}
	const files = [{'name': _id.replace(/\+/g, " ")}]

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

	function handleSave() {
		send = !send
		readonly = !readonly
	}
</script>

<BaseItem meta={meta} bind:readonly={readonly} cssClass='result'>

	<div slot="highlight">
		{#if highlight.content != ''}
			<p> &laquo; {@html highlight.content} &raquo; </p>
		{/if}
	</div>

	<div slot="button">
		<button on:click="{window.open(url,'_blank')}">
			CONSULTER
		</button>

		<button on:click={handleDelete}>
			SUPPRIMER
		</button>

		{#if (readonly & send) }
			<button on:click={handleSave}>
				MODIFIER
			</button>
			<PutItem meta={meta} files={files} />
		{:else if (!readonly & !send) }
			<button on:click={handleSave}>
				SAUVER
			</button>
		{:else}
			<button on:click="{() => readonly = !readonly}">
				MODIFIER
			</button>
		{/if}

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

	</div>


</BaseItem>

<style>

</style>
