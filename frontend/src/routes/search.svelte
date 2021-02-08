<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';
	import { userData } from '../common/user-data.store';
	import ResultList from '../components/ResultList.svelte';
	import SearchBar from '../components/SearchBar.svelte';
	import { itemConfig, promiseSearch, searchList } from '../components/stores.js';
	import { format2ES, get, search } from '../components/utils.js';

	let body
	onMount(async () => {
		$itemConfig = await get('user/item.json')
		console.log($itemConfig )
		$searchList = await get('user/search.json')
		//initial search
		if ($userData.initialSearch) {
			body =  format2ES($itemConfig, $searchList.flat(2), $userData.index_name)
			$promiseSearch = search(body)
		}
	});

</script>

<SearchBar/>
<ResultList/>
