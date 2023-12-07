<script>
	import { onMount } from "svelte";
	import { envJson } from "../../components/user-data.store";
	import { promiseSearch } from "./stores.js";
	import { itemJson, searchJson } from "../../components/user-data.store";
	import { flatten, format2ES, search } from "../../components/utils.js";
	import SearchBar from "./SearchBar.svelte";
	import ResultList from "./ResultList.svelte";
	import Aside from "./aside.svelte";

	let body;
	onMount(async () => {
		//initial search
		if ($envJson.initialSearch) {
			body = format2ES(
				$itemJson,
				flatten($searchJson, 2),
				$envJson.index_name,
			);
			$promiseSearch = search(body);
		}
	});
</script>

<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<div class="wrapper">

	<div class="search">
		<SearchBar />
	</div>

	<div class="aside">
		<Aside />
	</div>

	<div class="result">
		<!-- <Aside/> -->
		<ResultList />
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
		/* font-weight: bold;
		text-align: center; */
	}

	.wrapper > * {
		/* padding: 10px; */
		flex: 1 100%;
	}
	/* .search  { flex: 3 0px; } */
	.aside {
		position: sticky; /* Make the sidebar immovable*/
		/* position: -webkit-sticky; */
		z-index: 1; /*Side bar stays at the top*/
		top: 0rem;
		/* border-style: solid;
		border: 1px;
		border-color: red;
		border-style: solid; */
		max-width: 15%;
		align-self: flex-start;
	}

	.result {
		/* flex: 1 1 auto; */
		/* border: 1px;
		border-color: blue;
		border-style: solid; */
		max-width: 85%;
	}
	.search { order: 0;  } 
	.aside { order: 1; } 
	.result { order: 2;  }
</style>
