<script>
	export let _id;
	export let _source;
	export let highlight = {'content':''};

	$: filename = _id.replace(/\+/g, " ")
	$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`

	let promiseDelete = new Promise(()=>{});

	async function remove() {
		//for (var i = 0; i < files.length; i++) {
			//var file = files[i];
		const res = await fetch(`http://localhost/api/common/${filename}`, {
				method: 'DELETE'
				});

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

	{#await promiseDelete}
	{:then status}
		{#if status == 204 }
			<p style="color: green"> {filename} supprimé</p>
		{:else if status == 404 }
			<p style="color: red" > {filename} pas trouvé</p>
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
