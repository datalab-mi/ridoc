<script>
	import Nav from '../components/Nav.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import Logger from '../components/Logger.svelte';

	import { user, displayLogin, list_logger  } from '../components/stores.js';

	export let segment;



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

	<slot></slot>

	{#if $displayLogin}
		<LoginForm/>
	{/if}

	<Logger/>

</main>
