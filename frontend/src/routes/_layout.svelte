<script>
	import { onMount, onDestroy } from 'svelte';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';
	import { user } from '../components/stores';
	import Logger from '../components/Logger.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import { displayLogin } from '../components/stores.js';
	import { displaysurvey } from '../components/stores.js';
	import Footer from '../layouts/Footer.svelte';
	import Nav from '../layouts/Nav.svelte';
	import EmoRating from '../components/emoRating/starrating.svelte'
	import { clickOutside } from '../components/click-outside.action';

	export let segment;

	let rootNode;
	let mainNode;

	onMount(() => {
		rootNode = document.documentElement;
	})

	const handleClickOutside = (event) => {
		$displaysurvey = false;
	};

	$: rootNode && cssProps(rootNode, $userTheme.root);

	function emoSurvey() {
		$displaysurvey = !$displaysurvey
		console.log('test')
	}

</script>
<svelte:head>
	<script src="https://unpkg.com/jquery"></script>
	<script src="https://unpkg.com/knockout@3.5.1/build/output/knockout-latest.js" ></script>
	<script src="https://unpkg.com/survey-knockout@1.8.56/survey.ko.min.js"></script>

	<script src="https://unpkg.com/emotion-ratings@2.0.1/dist/emotion-ratings.js"></script>
	<script src="https://unpkg.com/surveyjs-widgets@1.8.56/surveyjs-widgets.min.js"></script>
</svelte:head>

{#if $displayLogin }
	<LoginForm />
{/if}



<!-- {#if $user.resources.includes("nav") }
	<Nav {segment} {login} />
{/if}
-->
<Nav {segment} />
<div class="fixed w-full mt-48 h-min" use:clickOutside on:clickoutside={handleClickOutside}>
	{#if $displaysurvey}
	<EmoRating />
	{:else}
	<div class=" button text-white rounded transform -rotate-90 origin-bottom-right p-2 px-4 " on:click={emoSurvey} >Votre avis nous intéresse</div>
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


</style>
