<script>

    import BaseItem from './BaseItem.svelte'
    import PutItem from './PutItem.svelte'

    import { index_name } from './stores.js';
    import {upload, index } from  './utils.js'

    let files;
    let meta = [
              {
                key: 'title',
                type: 'text',
                placeholder: 'Renseigner le titre',
                value: '',
                innerHtml: ''
              },
              {
                key: 'author',
                type: 'text',
                placeholder: 'Séparez les par des virgules',
                value: '',
                innerHtml: 'Auteurs :'
              },
              {
                key: 'date',
                type: 'date',
                placeholder: 'Date',
                value: '',
                innerHtml: 'Date :'
              }
            ]

  let send = false;

</script>

<BaseItem meta={meta}>


  <div slot="button">
    <input id="fileUpload" type="file" bind:files>

    {#if files}
        <button on:click="{() => send = !send}">Soumettre</button>
    {:else}
        <button disabled>Soumettre</button>
    {/if}

    {#if send}
      <PutItem meta={meta} files={files} />
    {/if}
  </div>

</BaseItem>

<style>

  #fileUpload {

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
