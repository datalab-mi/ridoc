<script>
	import { onMount, onDestroy } from 'svelte';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';
	import { user } from '../components/stores';
	import Logger from '../components/Logger.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import { displayLogin } from '../components/stores.js';
	import { displayRate } from '../components/stores.js';
	import Footer from '../layouts/Footer.svelte';
	import Nav from '../layouts/Nav.svelte';
	import EmoRating from '../components/emoRating/starrating.svelte'
	import { clickOutside } from '../components/click-outside.action';
	import "../../static/dsfr.css"

	export let segment;

	let rootNode;
	let mainNode;

	onMount(() => {
		rootNode = document.documentElement;
	})

	const handleClickOutside = (event) => {
		$displayRate = false;
	};

	$: rootNode && cssProps(rootNode, $userTheme.root);

	function emoSurvey() {
		$displayRate = !$displayRate
		console.log('test')
	}

</script>

{#if $displayLogin }
	<LoginForm />
{/if}



<!-- {#if $user.resources.includes("nav") }
	<Nav {segment} {login} />
{/if}
-->
<Nav {segment} />
<div class="rate fixed right-0 " use:clickOutside on:clickoutside={handleClickOutside}>
	{#if $displayRate}
	<EmoRating />
	{:else}
	<div class=" button text-white rounded transform -rotate-90 origin-bottom-right p-2 px-4 inline-flex" on:click={emoSurvey} ><svg class="mr-2" fill="white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 4.435c-1.989-5.399-12-4.597-12 3.568 0 4.068 3.06 9.481 12 14.997 8.94-5.516 12-10.929 12-14.997 0-8.118-10-8.999-12-3.568z"/></svg>Votre avis nous intéresse</div>
	{/if}
</div>

<main>
	<div class="">
		<slot />
		<Logger />
	</div>

</main>

<Footer />

<style>
	.button{
		background-color: var(--primary);
		float:right;

	}

	.rate{
		bottom:55%;
	}
</style>
