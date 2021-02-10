<script>
  import BaseItem from './BaseItem.svelte'
  import Entry from './Entry.svelte'
  import PutItem from './PutItem.svelte'

  import { get } from '../components/utils.js';

  let files ;
  let fileNameList = [];
  let send = false;
  const _id = -1
  const cssClass = "new"

  const required = false;

  async function filterItem() {
    let item = await get('user/item.json')
    item.inputs = item.inputs.filter(obj => obj.metadata)
    return item
  }
  let promise = filterItem()

</script>

{#await promise}
<p>... Récuperation de la configuration</p>
{:then item}

  <BaseItem {cssClass} {_id}>

    <div slot="fields">
      {#each item.inputs as {key, type, placeholder, value, innerHtml, highlight, metadata, isHighlight, rows, color}, i }
        <Entry  bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {isHighlight} {color} {required}/>
      {/each}
    </div>

    <div slot="button">
      <label for="docUpload" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
        Choisir un fichier
      </label>
      <input id="docUpload" class="fileUpload" type="file" bind:files multiple={item.multiple} accept={item.accept}>

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
          <PutItem meta={item.inputs} file={file} />
        {/each}
      {/if}
    </div>
</BaseItem>

{/await}

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

</style>
