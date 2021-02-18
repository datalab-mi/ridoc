<script>
	import { onMount, onDestroy } from 'svelte';
	import { cssProps } from '../common/css-props.action';
	import { createOpenCloseStore } from '../common/store.utils';
	import { userTheme } from '../common/theme.store';
	import Logger from '../components/Logger.svelte';
	import LoginForm from '../components/login/LoginForm.svelte';
	import { displayLogin } from '../components/stores.js';
	import Footer from '../layouts/Footer.svelte';
	import Nav from '../layouts/Nav.svelte';

	export let segment;

	const login = createOpenCloseStore();

	let rootNode;
	let mainNode;

	onMount(() => {
		rootNode = document.documentElement;
	})

	$: rootNode && cssProps(rootNode, $userTheme.root);

</script>

<div>
	{#if $displayLogin || $login}
		<LoginForm state={login} />
	{/if}
	<Nav {segment} {login} />

	<main>
		<div class="max-w-7xl mx-auto py-4 sm:py-6 px-2 sm:px-6 lg:px-8">
			<slot />
			<Logger />
		</div>
	</main>
	<Footer />
</div>
