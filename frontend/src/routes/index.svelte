
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div class="preview">
{@html marked(indexMd)}
</div>

<style>

	div.preview {
		margin: 0px auto 0px auto;
		max-width: 50rem;
	}

	div.preview :global(h1) {
			font-size: 2rem;
			margin-bottom: 1rem;
			margin-top: 1rem;

	}
	div.preview :global(h2) {
			font-size: 1.5rem;
			margin-bottom: 0.5rem;
			margin-top: 0.5rem;

	}
	div.preview :global(ul) {list-style-type: disc; padding: revert;}
	div.preview :global(a) {color: inherit;font-weight: 800;}
	div.preview :global(hr) {
		display: block;
		margin-top: 1em;
		margin-bottom: 0.5em;
		margin-left: auto;
		margin-right: auto;
		border-style: inset;
		border-width: 1px;
	}
</style>

<script>
import { onMount } from 'svelte';
import marked from 'marked'
export let indexMd = "";

onMount(async () => {
	const res = await fetch('notice.md');
	indexMd = await res.text();
	});

</script>
