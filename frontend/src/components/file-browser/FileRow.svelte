<script>

	import { list_logger  } from '../stores.js';
	import { createEventDispatcher } from 'svelte';

	export let item
	export let meta
	export let key
	export let readonly = true

	const name = item[key]
	const dispatch = createEventDispatcher();

</script>

<div class="inline-flex w-full">
	<div class="inline-flex" style="flex-grow: 1">
	{#each meta as {key, type, placeholder, value, innerHtml, size} }
		<div class="flex-grow w-{size} text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
			<input type="search" bind:value={item[key]} readonly={readonly} >
		</div>
	{/each}
	</div>
	{#if (! readonly) }
	<div class="flex-initial w-1/6 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
		<button on:click="{() => dispatch('delete', name)}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<svg class="fill-current w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
		</button>
	</div>
	{/if}

</div>

<style>

	td input {
		border:none;
		width: 90%;
		resize: none;
		background-color: inherit;
	 }

	th, td {
  text-align: left;
  padding: 8px;
	white-space:wrap;
}

input {
	border:none;
	width: 90%;
	resize: none;
	background-color: inherit;
 }

</style>
