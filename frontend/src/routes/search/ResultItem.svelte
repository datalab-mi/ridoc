<script>
	import { userTheme } from '../../components/theme.store';
	import { envJson } from '../../components/user-data.store';
	import BaseItem from '../../components/BaseItem.svelte';
	import Entry from '../../components/Entry.svelte';
	import PutItem from '../../components/PutItem.svelte';
	import { itemJson } from '../../components/user-data.store';
	import { list_logger, user } from '../../components/stores.js';
	import { httpClient, index, upload, createMeta, isEmpty } from '../../components/utils.js';

	export let _id;
	export let _source;
	export let _score;
	export let highlight = {}
	export let canBeChange = true;

	const http = httpClient();
	const required = true;

	let send = false;
	let readonly = true;

	let filename;
	$: filename = _id.replace(/\+/g, ' ')

	let file;
	$: file = { name: filename }

	let url;
	$: url = `/api/user/files/${$envJson.dstDir}/${filename}`

	let meta;
	let display;
	//$: url = `/web/viewer.html?file=%2Fuser%2Fpdf%2F${filename}`
	//$: meta = readonly ? createMeta(inputs, _source, highlight) : createMeta(inputs, _source)
	// !!! doesn't work, need to do this ugly workaround
	[meta, display] = createMeta($itemJson.inputs, _source, highlight)
	//const meta2 = createMeta($itemJson.inputs, _source)
	//$: meta = readonly ? meta1 : meta2

	function handleDelete() {
		console.log(`Delete ${filename}`)
		upload(meta, file, 'DELETE')
			.then(()   => list_logger.concat({ level: "success", message: "Document supprimé avec succès! ", ressource: "upload" }))
			.catch(err => list_logger.concat({ level: "error",   message: err, ressource: "upload" }));
		index($envJson.index_name, filename, 'DELETE')
			.then(()   => list_logger.concat({ level: "success", message: "Document désindexé avec succès! ", ressource: "upload" }))
			.catch(err => list_logger.concat({ level: "error",   message: err, ressource: "upload" }));
		display = false
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



	const btnAttrs = {
		class: 'hover:bg-gray-400'
	};
	const svgAttrs = {
		class: 'fill-current w-4 h-4 mr-2',
		xmlns: 'http://www.w3.org/2000/svg',
		viewBox: '0 0 20 20',
	};
</script>

{#if display}
	<BaseItem id={_id} >

		<div slot="fields" class="flex-col space-y-0">
		{#each meta as { value, key, type, placeholder, innerHtml, highlight, metadata, rows, color} (key)}
				{#if !isEmpty(value) || (!readonly && metadata) }
					<Entry {readonly} {required} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {rows} {color} />
				{/if}
		{/each}
		</div>

		<div slot="buttons" class="pt-4">

			<button on:click={http.fetchAuth(url,filename)} {...btnAttrs} style={$envJson.primary} class="fr-btn">
				<svg {...svgAttrs}><path d="M.2 10a11 11 0 0 1 19.6 0A11 11 0 0 1 .2 10zm9.8 4a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0-2a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg>
				<span>CONSULTER</span>
			</button>

			{#if $user.role === 'admin'}
			<button on:click={handleDelete} {...btnAttrs} style={$envJson.primary} class="fr-btn">
				<svg {...svgAttrs}><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
				<span>SUPPRIMER</span>
			</button>
			{#if canBeChange }
					{#if readonly && send}
						<button on:click={handleSave} {...btnAttrs} class="fr-btn">
							<svg {...svgAttrs}><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
							<span>MODIFIER</span>
						</button>
						<PutItem meta={meta} file={file} />
					{:else if readonly || send}
						<button on:click={() => readonly = !readonly} {...btnAttrs} class="fr-btn">
							<svg {...svgAttrs}><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
							<span>MODIFIER</span>
						</button>
					{:else}
						<button on:click={handleSave} {...btnAttrs} class="fr-btn">
							<svg {...svgAttrs}><path d="M0 2C0 .9.9 0 2 0h14l4 4v14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm5 0v6h10V2H5zm6 1h3v4h-3V3z"/></svg>
							<span>SAUVER</span>
						</button>
						<button on:click={handleCancel} {...btnAttrs} class="fr-btn">
							<svg {...svgAttrs}><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"/></svg>
							<span>ANNULER</span>
						</button>
					{/if}
				{/if}
			{/if}

		</div>

		<div slot="score" class="my-auto">
			{#if _score && $user.resources.includes('admin')}
				<p class="whitespace-no-wrap">Score : {Math.round((_score + Number.EPSILON) * 100) / 100}</p>
			{/if}
		</div>

	</BaseItem>
{/if}

<style>

</style>
