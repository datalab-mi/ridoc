<script>

import { index_name } from './stores.js';
import { index, upload } from './utils.js'

export let meta;
export let file;


const filename = file.name.replace(/\+/g, " ")

console.log(`Save ${filename}`)
let promiseUpload = upload(meta, file)
let promiseIndex = index($index_name, filename, 'PUT');


</script>


{#await promiseUpload}
{:then status}
  {#if status == 201 }
    <p style="color: green">{filename} crée</p>
  {:else if (status == 200) }
    <p style="color: blue" >{filename} modifié</p>
  {:else if (status == 203) }
    <p style="color: red" >{filename} au mauvais format!</p>
  {:else if (status == 202) }
    <p></p>
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
