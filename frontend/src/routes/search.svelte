<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { itemConfig, searchList, userData, promiseSearch } from '../components/stores.js';
	import { get, format2ES, search } from '../components/utils.js';

	import { onMount } from 'svelte';
	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';

	let body
	onMount(async () => {
		$itemConfig = await get('user/item.json')
		console.log($itemConfig )
		$searchList = await get('user/search.json')
		//initial search
		body =  format2ES($itemConfig, $searchList.flat(2), $userData.index_name)
		$promiseSearch = search(body)

	});

</script>

<SearchBar/>
<ResultList/>
