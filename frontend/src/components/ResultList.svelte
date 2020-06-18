<script>
import { searchInput, searchResults, index_name } from '../components/stores.js';
import ResultItem from '../components/ResultItem.svelte';

</script>


{#if searchResults}
	<div class='result-list'>

	{#each $searchResults as item, i}
		<ResultItem {...item}/>
	{/each}

	</div>

{/if}

<style>
	.result-list {
		width: 90%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(255,0,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
</style>
