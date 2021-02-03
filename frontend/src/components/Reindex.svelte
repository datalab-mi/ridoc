<script>
import { userData, isReindex, list_logger } from './stores.js';
import {reIndex} from './utils.js'
import VirtualList from './VirtualList.svelte';

let promise = new Promise(() => {});

	function handleIndex() {
    $isReindex = true
		promise = reIndex($userData.index_name)
		promise
		.then(res => {
			$isReindex = false
			list_logger.concat({level: "success", message: "Réindexation terminée", status: res.status, ressource: "Reindex"})
		})
		.catch(err => {
			list_logger.concat({level: "error", message: err, ressource: "Reindex"})
	  })
	}
</script>



	<div>
    <button on:click={handleIndex} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">

    {#if $isReindex}
      <svg id="spinner" class="fill-current w-4 h-4 mr-2"  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M14.66 15.66A8 8 0 1 1 17 10h-2a6 6 0 1 0-1.76 4.24l1.42 1.42zM12 10h8l-4 4-4-4z"/></svg>
    {:else}
      <svg class="fill-current w-4 h-4 mr-2"  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M14.66 15.66A8 8 0 1 1 17 10h-2a6 6 0 1 0-1.76 4.24l1.42 1.42zM12 10h8l-4 4-4-4z"/></svg>
    {/if}

      <span>Réindexation</span>
    </button>
  </div>

	{#await promise then result}
		{#if (result.log.length > 0)}
		<p style="color: red">{result.log.length} documents non indexés</p>
		<ul>
			{#each result.log as item}
				<li><b>{item.filename}</b></li>
				<p>{item.msg}</p>

			{/each}
		</ul>
		{/if}
	{/await}

	<!-- <div class='containerVL'> -->
	<!-- 	<VirtualList key={'filename'} items={result.log} let:item> -->
	<!-- 		<p>{item.filename} : {item.msg}</p> -->
	<!-- 	</VirtualList> -->
	<!-- </div> -->
<!-- svelte-ignore empty-block -->
<!--{#await promise} -->
<!--{:catch error} -->
<!--<p style="color:red">Error</p>-->
<!-- <iframe srcdoc={error.message} height="300">  -->
<!--</iframe> -->
<!--{/await}  -->
<style>

#spinner {
  transition-property: transform;
  animation-name: svelte-spinner_infinite-spin;
  animation-duration: 750ms;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}
@keyframes svelte-spinner_infinite-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.containerVL {
max-height: 50rem;
height: calc(20vh)
}

ul {
	list-style: disc inside;
}
</style>
