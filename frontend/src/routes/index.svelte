<svelte:head>
	<title>Accueil</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>
<div class="background">

<div class="preview" use:cssProps={$userTheme.index}>
<div>
{#if ($user.resources.includes("description") && description.length > 0)}
	{@html marked(description)}
{/if}
</div>
<div>
{#if ($user.resources.includes("notice") && notice.length > 0)}
	<hr>
	{@html marked(notice)}
{/if}
</div>
<hr>
<div class="flex flex-wrap justify-evenly">
{#if ($user.resources.includes("search"))}
	<button  onclick="location.href='search'" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded  inline-flex items-center itemJsons-center">
		<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
		<span>Rechercher</span>
	</button>
{/if}
</div>
</div>
</div>

<style>

	div.preview {
		margin: 0px auto 0px auto;
		max-width: 50rem;
	}
	div.preview :global(p) {
		text-align: justify;
	}
	/* a paragraph proceeded by another paragraph will have a top margin */
	div.preview :global(p + p) {
	    margin-top: 12px;
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
import { onMount, onDestroy } from 'svelte';
import { user } from '../components/stores.js';
import { cssProps } from '../components/css-props.action';
import { userTheme } from '../components/theme.store';
import marked from 'marked'
let description = "";
let notice = "";
let mainNode;

onMount(async () => {
	mainNode = document.getElementsByTagName("main")[0]

	const res1 = await fetch('user/notice.md');
	if (res1.ok) {
		notice = await res1.text();
	}
	const res2 = await fetch('user/description.md');
	if (res2.ok) {
		description = await res2.text();
	}
})

$: {
	mainNode && mainNode.style.setProperty("background-image", 'url("/user/background.jpg")')
	mainNode && mainNode.style.setProperty("background-size", "auto 100%")
}

onDestroy(() => {
	mainNode && mainNode.style.removeProperty("background-image")
	mainNode && mainNode.style.removeProperty("background-size")
});

</script>
