<script>
	import { index_name } from './stores.js';
	import SynonymRow from './SynonymRow.svelte';

	let GetPromise;
	let PutPromise = new Promise(()=>{});

	let list_synonym;
	let filterKey = '';
	let filterValue = '';

	let isAdd = false;
	let readonly = true;
	let send = false;

	let meta = [
						{
							key: 'expresion1',
							type: 'text',
							placeholder: 'DNUM',
							value: '',
							innerHtml: 'Acronyme: '
						},
						{
							key: 'expresion2',
							type: 'text',
							placeholder: 'Direction du Numérique',
							value: '',
							innerHtml: 'Signification: '
						}
					]

	let key;

	async function synonym(method) {
		let res;
		if (method == 'GET') {
			res = await fetch(`http://localhost/api/common/synonym`,
					{method: 'GET'});
		} else if (method == 'PUT') {
			key = meta[0].value
			res = await fetch(`http://localhost/api/admin/synonym/${key}`, {
					method: 'PUT',
					body: JSON.stringify(meta)});
		}
		list_synonym = await res.json();
		console.log(list_synonym)

		if (res.ok)  {
			return res.status
		} else {
			console.log('error')
			throw new Error('Oups');
		}
	}

	GetPromise = synonym('GET')

function handleSubmit() {
	PutPromise = synonym('PUT')
}

function handleAdd() {
	isAdd = !isAdd;
}

function handleSave() {
	send = !send;
	readonly = !readonly;
}

</script>

<div class="container">

<div class='synonym-list'>
<div>
	{#await GetPromise}
	<p>...Attente de la requête</p>
	{:then status}
	<table>
	    <thead>
				<th class='key'><input type="search" bind:value={filterKey} placeholder='recherche' ></th>
				<th class='value'><input type="search" bind:value={filterValue} placeholder='recherche' ></th>
	    </thead>
	    <tbody>
				{#each list_synonym as item, i}
					{#if (filterKey == '') || (item.key.includes(filterKey)) }
						{#if (filterValue == '') || (item.value.includes(filterValue)) }

							<SynonymRow expression1={item.key} expression2={item.value} />

						{/if}
					{/if}

				{/each}
	    </tbody>
	</table>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

</div>
</div>

<div>

<div class='synonym-add'>

	<button on:click={handleAdd}>Ajouter</button>
	{#if (isAdd)}
		{#each meta as {key, type, placeholder, value, innerHtml}, i }
			<label> {@html innerHtml}
			<input type='text' bind:value={value} {placeholder}/>
			</label>
			<br>
		{/each}

		{#if meta.every((e) => e.value != '')}
			<button on:click={handleSubmit}>Soumettre</button>
			{:else}
			<button disabled>Soumettre</button>
		{/if}
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

<div class='synonym-add'>

		{#if (readonly & send) }
			<button on:click={handleSave}>
				MODIFIER
			</button>

		{:else if (!readonly & !send) }
			<p style="color: green">Vous pouvez modifier le tableau</p>
			<button on:click={handleSave}>
				SAUVER
			</button>
		{:else}
			<button on:click="{() => readonly = !readonly}">
				MODIFIER
			</button>
		{/if}
</div>
</div>
</div>


<style>
	.container {
		display: flex;
  	height: 80vh;
		justify-content: space-between
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
	td input {
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

tr:nth-child(even) {background-color: #f2f2f2;}


</style>
