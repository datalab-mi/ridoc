<script>
	import { onMount } from 'svelte';
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

	const bgColorProp = '--bg-color';
	const styleProps = { 'background-color': `var(${bgColorProp})` };

	let rootNode;

	onMount(() => rootNode = document.documentElement);

	$: {
		if (rootNode) {
			styleProps[bgColorProp] = $userTheme.backgroundColor;
			cssProps(rootNode, styleProps);
		}
	}
</script>

<div>
	{#if $displayLogin || $login}
		<LoginForm state={login} />
	{/if}
	<Nav {segment} {login} />

	<!-- <header>
		<div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
			<h1 class="text-3xl font-bold leading-tight text-gray-900">
				Dashboard
			</h1>
		</div>
	</header> -->
	<main>
		<div class="max-w-7xl mx-auto py-4 sm:py-6 px-2 sm:px-6 lg:px-8">
			<slot></slot>
			<Logger/>
		</div>
	</main>
	<Footer />
</div>
