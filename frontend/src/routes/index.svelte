<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';

	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';
	import { searchResults } from '../components/stores.js';

</script>

<SearchBar/>

<ResultList/>
