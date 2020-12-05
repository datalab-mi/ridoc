<script>
	import Nav from '../components/Nav.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import Logger from '../components/Logger.svelte';

	import { displayLogin, list_logger  } from '../components/stores.js';

	export let segment;

	const handleAdd = (msg) => {
		$list_logger = $list_logger.concat({level: "info",message: msg + "", ressource: "upload", status:200})
	}
	const handleDelete = () => {
		$list_logger = $list_logger.slice(1, $list_logger.length)
	}


</script>

<style>
	main {
		position: relative;
		max-width: 120em;
		background-color: white;
		padding: 2em;
		margin: 0;
		box-sizing: border-box;
	}
</style>

<Nav {segment}/>

<main >
	<input
		placeholder="what needs to be done?"
		on:keydown={e => e.key === 'Enter' && handleAdd(e.target.value)}
	>
	<button  on:click={handleDelete}>Delete</button>

	<slot></slot>

	{#if $displayLogin}
		<LoginForm/>
	{/if}

	<Logger/>
</main>
