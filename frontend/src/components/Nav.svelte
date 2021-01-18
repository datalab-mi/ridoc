<script>
	import { user, displayLogin, userData } from './stores.js';
	import { onDestroy } from 'svelte';

	export let segment;
	let logo = ''
  const unsubscribe = userData.subscribe(value => {
    logo = "user/" + value.logo;
  });

	function authClicked() {
		$displayLogin =! $displayLogin
	}

</script>

<style>
	nav {
		border-bottom: 1px solid rgba(255,62,0,0.1);
		font-weight: 300;
		padding: 0 1em;
		display: flex;
		justify-content: space-between;
	}

	ul {
		margin: 0;
		padding: 0;
	}

	/* clearfix */
	ul::after {
		content: '';
		display: block;
		clear: both;
	}

	li {
		display: block;
		float: left;
	}

	[aria-current] {
		position: relative;
		display: inline-block;
	}

	[aria-current]::after {
		position: absolute;
		content: '';
		width: calc(100% - 1em);
		height: 2px;
		background-color: rgb(255,62,0);
		display: block;
		bottom: -1px;
	}

	a {
		text-decoration: none;
		padding: 1em 0.5em;
		display: block;
	}

	.logo {
		margin: auto;
		width:100%;
		height:100%;
		viewBox: "0 0 100 100"
	}

	.login {
		cursor: pointer;
	}

</style>

<nav>

	<ul>
		<li><a class="w-12 h-12" href='.'><img src={logo}></a></li>
		<li><a aria-current='{segment === "search" ? "page" : undefined}' href='search'>recherche</a></li>
		<li><a aria-current='{segment === "glossary" ? "page" : undefined}' href='glossary'>glossaire</a></li>
		<li><a aria-current='{segment === "expression" ? "page" : undefined}' href='expression'>expression</a></li>

		{#if ($user.role === "admin")}
			<li><a aria-current='{segment === "admin" ? "page" : undefined}' href='admin'>admin</a></li>
		{/if}

	</ul>

	<svg on:click={authClicked} class="login inline-block object-center fill-current w-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5 5a5 5 0 0 1 10 0v2A5 5 0 0 1 5 7V5zM0 16.68A19.9 19.9 0 0 1 10 14c3.64 0 7.06.97 10 2.68V20H0v-3.32z"/></svg>

</nav>
