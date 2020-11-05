<script>

  import Entry from './Entry.svelte'
  import PutItem from './PutItem.svelte'

  import { get } from '../components/utils.js';

  let files ;
  let fileNameList = [];
  let send = false;

  const required = false;

  async function filterItem() {
    let item = await get('/api/common/files/item.json')
    item.inputs = item.inputs.filter(obj => obj.metadata)
    return item
  }
  let promise = filterItem()

</script>

{#await promise}
<p>... Récuperation de la configuration</p>
{:then item}

<section class="new-item">

{#each item.inputs as {key, type, placeholder, value, innerHtml, highlight, metadata, isHighlight}, i }
  <Entry required={required} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {isHighlight}}/>
{/each}

<div>
  <label for="docUpload" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
  Choisir un fichier
  </label>

  <input id="docUpload" class="fileUpload" type="file" bind:files multiple={item.multiple} accept={item.accept}>

  {#if files}
    <button on:click="{() => send = !send}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
      <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
      <span>SOUMETTRE</span>
    </button>
    <br>
    {#each files as file}
      <li>{file.name}</li>
    {/each}
  {:else}
    <button disabled class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
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
</section>
{/await}

<style>

  .fileUpload {
    display: none;
  }

	.new-item {
		width: 90%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,0,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}

  input,textarea {
    border:none;
    width: 90%;
    resize: none;
   }

 .title {
	 font-weight: bold;
	 margin: 0;
	 padding: 0;
 }

</style>
