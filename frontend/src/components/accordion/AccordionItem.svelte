<script>
	import { createEventDispatcher,getContext } from 'svelte';
	import { sineInOut } from 'svelte/easing';
	import { writable } from 'svelte/store';
	import { slide } from 'svelte/transition';
	import { contextKey } from './accordion';

	/** store pour la valeur de sélection */
	export let selection = getContext(contextKey) || writable(null);

	/** valeur correspondant à la sélection de cette section */
	export let itemValue = 1;

	/** classe(s) CSS de la section d'accordéon */
	export let itemClass = undefined;

	/** styles CSS de la section d'accordéon */
	export let itemStyle = undefined;

	/** classe(s) CSS du bouton */
	export let buttonClass = undefined;

	/** styles CSS du bouton */
	export let buttonStyle = undefined;

	/** classe(s) CSS du contenu */
	export let contentClass = undefined;

	/** styles CSS du contenu */
	export let contentStyle = undefined;

	/** paramètres de transition */
	export let slideParams = {};

	/**
	 * texte pour le titre
	 * alternative : passer un slot 'title'
	*/
	export let title = 'titre';

	/**
	 * texte pour le contenu
	 * alternative : passer un slot 'content'
	*/
	export let content = 'contenu';

	const dispatch = createEventDispatcher();

	/** élément DOM externe (élément de liste) */
	let itemNode;

	let derivedSlideParams;
	$: derivedSlideParams = { duration: 700, easing: sineInOut, ...slideParams };

	let expanded;

	$: {
		const oldValue = expanded;
		expanded = $selection === itemValue;
		if (oldValue != expanded) {
			dispatch('expand', { itemNode, expanded });
		}
	}

	const toggleSelection = () => selection.update(v => v !== itemValue ? itemValue : null);
</script>

<li bind:this={itemNode} class="relative {itemClass || ''}" style={itemStyle}>
	<button type="button" on:click={toggleSelection} class={buttonClass} style={buttonStyle}>
		<slot name="title">
			<div class="flex items-center">
				<span class="pr-2">{title}</span>
				<svg class:hidden={!expanded} class:inline-block={expanded}
						class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
				</svg>
				<svg class:hidden={expanded} class:inline-block={!expanded}
						class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
				</svg>
			</div>
		</slot>
	</button>
	{#if expanded}
		<div transition:slide|local={derivedSlideParams} class={contentClass} style={contentStyle}>
			<slot name="content">
				<div class="p-6">
					<p>{content}</p>
				</div>
			</slot>
		</div>
	{/if}
</li>

<style>
	button {
		@apply w-full;
		@apply px-2;
		@apply py-2;
		/* @apply border-b; */
		@apply outline-none;
		@apply text-left;
	}
	/** ignore this warning (unused) */
	/*
	li + li {
		@apply border-t;
	}
	li:last-child {
		@apply border-b;
	}
	*/
	li {
    list-style-type: none;
	}
</style>
