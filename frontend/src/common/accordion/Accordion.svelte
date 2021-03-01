<script>
	import { setContext } from 'svelte';
	import { writable } from 'svelte/store';
	import { contextKey } from './accordion.js';

	export let selection = writable(null);

	/** classe(s) CSS du conteneur externe */
	export let containerClass = undefined;

	/** styles CSS du conteneur externe */
	export let containerStyle = undefined;

	/** classe(s) CSS de la liste */
	export let listClass = undefined;

	/** styles CSS de la liste */
	export let listStyle = undefined;

	setContext(contextKey, selection);
</script>

<div class="accordion {containerClass || ''}" style={containerStyle}>
	<ul class={listClass} style={listStyle}>
		<slot>
			<li>il manque le contenu</li>
		</slot>
	</ul>
</div>

<style>
	.accordion {
		@apply mx-auto;
	}
	/*
	ul {
		@apply border-t;
		@apply border-l;
		@apply border-r;
	}
	ul:empty {
		@apply border-b;
	}
	*/
</style>
