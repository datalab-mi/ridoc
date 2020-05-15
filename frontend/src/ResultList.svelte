<script>
	import { searchInput } from './stores.js';
</script>

<h1>La recherche est : {$searchInput.fullText.value}</h1>

<div class='result-list'>
<slot></slot>
</div>

<style>
	.result-list {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(255,0,0,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
</style>
