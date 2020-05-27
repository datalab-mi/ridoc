<script>

    import { index_name } from './stores.js';
    import {upload, index } from  './utils.js'

    let files;
    let meta = [
              {
                key: 'title',
                type: 'text',
                placeholder: 'Titre',
                value: ''
              },
              {
                key: 'author',
                type: 'text',
                placeholder: 'Auteurs',
                value: ''
              },
              {
                key: 'date',
                type: 'date',
                placeholder: 'Date',
                value: ''
              }
            ]
  let promiseIndex = new Promise(()=>{});
  let promiseUpload = new Promise(()=>{});

  async function handleUpload() {
    promiseUpload = await upload(meta, files);
    promiseIndex = await index($index_name, files[0].name, 'PUT');
  }

</script>

<div class='upload-item'>

  <form >
    <input id="fileUpload" type="file" bind:files>
    {#each meta as {key, type, placeholder, value}, i }
      {#if type == "text"}
        <input type='text' bind:value={value} {placeholder} />
      {:else if type == "date"}
        <input type='date' bind:value={value} {placeholder} />
      {/if}
    {/each}

  </form>

  {#if files}
      <button on:click={handleUpload}>Submit</button>
  {:else}
      <button on:click={handleUpload} disabled>Submit</button>
  {/if}


  {#await promiseUpload}
  {:then status}
    {#if status == 201 }
      <p style="color: green">{files[0].name} crée</p>
    {:else if status == 200 }
      <p style="color: blue" >{files[0].name} modifié</p>
    {:else}
      <p>Status {status} non connu</p>
    {/if}
  {:catch error}
  	<p style="color: red">{error.message}</p>
  {/await}

  {#await promiseIndex}
  {:then status}
    {#if status == 201 }
      <p style="color: green">{files[0].name} indexé</p>
    {:else if status == 200 }
      <p style="color: blue" >{files[0].name} modifié dans l'index</p>
    {:else}
      <p>Status {status} non connu</p>
    {/if}
  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
</div>

<style>
	.upload-item {
		width: 90%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,0,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
</style>
