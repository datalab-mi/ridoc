<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';
	import { envJson } from '../../components/user-data.store';
	import { promiseSearch } from './stores.js';
	import { itemJson, searchJson } from '../../components/user-data.store';
	import { flatten, format2ES, search } from '../../components/utils.js';
	import SearchBar from './SearchBar.svelte';
	import ResultList from './ResultList.svelte';
	import Aside from './aside.svelte';

	let body
	onMount(async () => {
		//initial search
		if ($envJson.initialSearch) {
			body =  format2ES($itemJson, flatten($searchJson, 2), $envJson.index_name)
			$promiseSearch = search(body)
		}
	});

</script>

<div class="wrapper">
	<div class="search">
		<SearchBar/>
	</div>
	<div class="aside">
		<Aside/>
	</div>
	<div class="result">
		<!-- <Aside/> -->
		<ResultList/>
	</div>
</div>

<style>
/* 
.result {
  background: deepskyblue;
}

.aside {
  background: gold;
}

.search {
	background: green;
} */

.wrapper {
  display: flex;  
  flex-flow: row wrap;
  font-weight: bold;
  text-align: center; 
}

.wrapper > * {
  /* padding: 10px; */
  flex: 1 100%;
}
  /* .search  { flex: 3 0px; } */
  	.aside { flex: 1 1 auto; } 
   .result { flex: 1 1 auto; }
  /* .search { order: 0; } 
  .aside { order: 1; } 
  .result { order: 2; } */

</style>