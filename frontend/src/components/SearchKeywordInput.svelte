<script>
	import Tags from "svelte-tags-input";
	import { userData } from '../common/user-data.store';
	import { USER_API, get } from "./utils.js";
	import { onMount } from "svelte";

	export let placeholder = "";
	export let fields = "";
	export let value = "";
	export let color = "#000";

	let promiseListKeyword;

	onMount(() => {
		promiseListKeyword = get(`${USER_API}/keywords/${$userData.index_name}/${fields}`);
	});

	function handleTags(event) {
		value = event.detail.tags;
	}
</script>

{#await promiseListKeyword then autoComplete}
	<div class="my-custom-class" style="--color: {color}">
		<Tags
			tags={value}
			on:tags={handleTags}
			{placeholder}
			allowDrop={true}
			allowPaste={true}
			onlyUnique={true}
			{autoComplete}
			minChars={0}
		/>
	</div>
{/await}

<style>
	/* override default Tag style */
	.my-custom-class :global(.svelte-tags-input-tag) {
		background: var(--color) !important;
		cursor: default !important;
	}
	.my-custom-class :global(.svelte-tags-input-layout) {
		background: #fff !important;
		border-style: none !important;
		cursor: default !important;
	}
	.my-custom-class :global(.svelte-tags-input) {
		background: #fff !important;
		cursor: default !important;
	}
</style>
