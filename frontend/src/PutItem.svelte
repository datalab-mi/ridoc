<script>

import { index_name } from './stores.js';
import { index, upload } from './utils.js'

export let meta;
export let files;

let filename;
$: {
  console.log(files)
  filename = files[0].name.replace(/\+/g, " ")
}

let promiseUpload = new Promise(()=>{});
let promiseIndex = new Promise(()=>{});


async function handleUpdate() {
  console.log(`Save ${filename}`)
  promiseUpload = await upload(meta, files)
  promiseIndex = await index($index_name, filename, 'PUT');
}

handleUpdate()

</script>


{#await promiseUpload}
{:then status}
  {#if status == 201 }
    <p style="color: green">{filename} crée</p>
  {:else if status == 200 }
    <p style="color: blue" >{filename} modifié</p>
  {:else}
    <p>Status {status} non connu</p>
  {/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}

{#await promiseIndex}
{:then status}
  {#if status == 201 }
    <p style="color: green">{filename} indexé</p>
  {:else if status == 200 }
    <p style="color: blue" >{filename} modifié dans l'index</p>
  {:else}
    <p>Status {status} non connu</p>
  {/if}
{:catch error}
  <p style="color: red">{error.message}</p>
{/await}
