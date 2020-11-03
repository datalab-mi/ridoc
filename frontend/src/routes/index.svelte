<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { itemConfig, searchList, index_name, promiseSearch } from '../components/stores.js';
	import { config, format2ES, search } from '../components/utils.js';

	import { onMount } from 'svelte';
	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';

	let body
	onMount(async () => {
		console.log('onmount')
		$itemConfig = await config('item.json')
		$searchList = await config('search.json')
		//initial search
		body =  format2ES($itemConfig, $searchList.flat(2), $index_name)
		$promiseSearch = await search(body)
	});

</script>

<SearchBar/>
<ResultList/>
