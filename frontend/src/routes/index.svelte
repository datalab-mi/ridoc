<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';

	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';
	import UploadFiles from '../components/NewItem.svelte';


</script>

<SearchBar/>

<UploadFiles />

<ResultList/>
