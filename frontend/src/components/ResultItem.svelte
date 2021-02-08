<script>
	import PutItem from './PutItem.svelte'
	import Entry from './Entry.svelte'

	import { itemConfig, user, list_logger } from './stores.js';
	import { userData } from '../common/user-data.store';
	import { index, upload } from './utils.js'

	export let _id;
	export let _source;
	export let _score;
	export let highlight = {}

	let readonly = true
	let send = false
	let isResult = true
	let cssClass = 'result'
	let filename = _id.replace(/\+/g, " ")

	$: url = `/api/user/files/${$userData.dstDir}/${filename}`
	//$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`

	const file = {'name': _id.replace(/\+/g, " ")}
	const meta = JSON.parse(JSON.stringify($itemConfig.inputs))

	// replace value to the result value contained in _source or in highlight key
	// if present and if needed
	let display = true
	JSON.parse(JSON.stringify($itemConfig.inputs)).forEach((x, index) => {
		//console.log(highlight)
		if (x.highlight && highlight && (x.key in highlight)) {
			meta[index].value = highlight[x.key].join(' [...] ')
			meta[index].isHighlight = true
		} else {
			meta[index].value =  x.key in _source  ? _source[x.key] : x.value
			meta[index].isHighlight = false
		}
		// test if item should be displayed if empty
		if (!( meta[index].canBeEmpty === undefined) && (! meta[index].canBeEmpty) && (isEmpty(meta[index].value))) {
			display = false
		}
	})


	function handleDelete() {
		console.log(`Delete ${_id.replace(/\+/g, " ")}`)
		upload(meta, file, 'DELETE')
			.then(() => {
				list_logger.concat({level: "success", message: "Document supprimé avec succès! ", ressource: "upload"})
			})
			.catch(err => {
				list_logger.concat({level: "error", message: err, ressource: "upload"})
			})

		index( $userData.index_name, filename, 'DELETE')
			.then(() => {
				list_logger.concat({level: "success", message: "Document désindexé avec succès! ", ressource: "upload"})
			})
			.catch(err => {
				list_logger.concat({level: "error", message: err, ressource: "upload"})
			})
	}

	function handleSave() {
		send = !send
		readonly = !readonly
	}

	function handleCancel() {
		// reset values
		readonly = true;
		send = false;
	}

	function isEmpty(value){
	  return (value == null || value.length === 0);
	}

</script>

{#if (display) }
	<section class="result-item" id={_id}>

		{#if (readonly) }
				{#each meta as {key, type, placeholder, value, innerHtml, highlight, metadata, isHighlight, rows, color}, i }
					{#if (! isEmpty(value)) }
						<Entry  {readonly} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {isHighlight} {cssClass} {rows} {color}/>
					{/if}
				{/each}
		{:else}
			{#each meta as {key, type, placeholder, value, innerHtml, highlight, metadata, isHighlight, rows, color}, i }
				<Entry  {readonly} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {isHighlight} {cssClass} {rows} {color}/>
			{/each}
		{/if}

		<div class="flex justify-between">

		<div>
			<button on:click="{window.open(url,'_blank')}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M.2 10a11 11 0 0 1 19.6 0A11 11 0 0 1 .2 10zm9.8 4a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0-2a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg>
				<span>CONSULTER</span>
			</button>

			{#if ($user.role === "admin") }

				<button on:click={handleDelete} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
					<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
					<span>SUPPRIMER</span>
				</button>

				{#if (readonly && send) }
					<button on:click={handleSave} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
						<span>MODIFIER</span>
					</button>
					<PutItem meta={meta} file={file} />
				{:else if (!readonly && !send) }
					<button on:click={handleSave} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M0 2C0 .9.9 0 2 0h14l4 4v14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm5 0v6h10V2H5zm6 1h3v4h-3V3z"/></svg>
							<span>SAUVER</span>
					</button>
					<button on:click={handleCancel} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"/></svg>
						<span>ANNULER</span>
					</button>
				{:else}
					<button on:click="{() => readonly = !readonly}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
						<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
						<span>MODIFIER</span>
					</button>
				{/if}
			{/if}

		</div>

		<div>
			{#if (($user.resources.includes("admin")) && (_score != 0))}
					<p>Score : {Math.round((_score + Number.EPSILON) * 100) / 100}</p>
			{/if}
		</div>

		</div>

	</section>
{/if}

<style>
	.result-item {
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0, 0, 255, 1);
		padding: 1em;
		margin: 1em 1em 1em 1em;
	}
</style>
