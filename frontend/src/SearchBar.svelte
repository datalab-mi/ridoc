<script>
	import { searchInput } from './stores.js';
</script>

<div class='search-bar'>
<input bind:value={$searchInput.fullText.value} placeholder={$searchInput.fullText.placeholder}>
</div>

<style>
	.search-bar {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,255,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
</style>
