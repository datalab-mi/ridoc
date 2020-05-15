<script>
	import ResultItem from './ResultItem.svelte';
	import ResultList from './ResultList.svelte';
	import SearchBar from './SearchBar.svelte';

</script>

<SearchBar/>

<ResultList>

<ResultItem title={'Title A'} body={'Some text'} authors={'Author 1'}/>
<ResultItem title={'Title B'} body={'Some text'} authors={'Author 2'}/>
<ResultItem title={'Title C'} body={'Some text'} authors={'Author 3'}/>

</ResultList>
