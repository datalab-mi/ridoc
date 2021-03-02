<script>
	import { userTheme } from '../../components/theme.store';
	import { itemJson } from '../../components/user-data.store';
	import BaseItem from '../../components/BaseItem.svelte';
	import Entry from '../../components/Entry.svelte';
	import PutItem from '../../components/PutItem.svelte';

  let files;
  let send = false;
	let itemNew = {};
	$: itemNew = $itemJson
	$: console.log(itemNew)
  const _id = -1
  const required = false
	const readonly = false


</script>

{#if Object.keys(itemNew).length === 0 }
	<p>... Récuperation de la configuration</p>
{:else}

	<BaseItem id={_id} componentCssProps={$userTheme.search && $userTheme.search.results}>

	    <div slot="fields" class="flex-col space-y-1">
	      {#each itemNew.inputs as { value, key, type, placeholder, innerHtml, highlight, metadata, isHighlight, color} (key)}
					{#if metadata}
						<Entry {readonly} {required} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {isHighlight} {color} />
					{/if}
				{/each}
	    </div>

	    <div slot="buttons">
	      <label for="docUpload" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
	        Choisir un fichier
	      </label>
	      <input id="docUpload" class="fileUpload" type="file" bind:files multiple={itemNew.multiple} accept={itemNew.accept}>

	      {#if files}
	        <button on:click="{() => send = !send}" class="hover:bg-gray-400">
	          <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
	          <span>SOUMETTRE</span>
	        </button>
	        <br>
	        {#each files as file}
	          <li>{file.name}</li>
	        {/each}
	      {:else}
	        <button disabled>
	          <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
	          <span>SOUMETTRE</span>
	        </button>
	      {/if}

	      {#if send}
	        {#each files as file}
	          <PutItem meta={itemNew.inputs} file={file} />
	        {/each}
	      {/if}
	    </div>
	</BaseItem>
{/if}

<style>
	.fileUpload {
		display: none;
	}
	button {
		@apply mt-1;
		@apply px-4;
		@apply py-2;
		@apply bg-gray-300;
		@apply text-gray-800;
		@apply font-bold;
		@apply rounded;
		@apply inline-flex;
		@apply items-center;
	}
	div[slot='fields'] :global(.entry-title) {
		color: blue;
	}
</style>
