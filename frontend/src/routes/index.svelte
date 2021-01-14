
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div class="preview">
<h1>Liens rapides</h1>

<div class="flex flex-wrap justify-evenly">
	<button  onclick="location.href='search'" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded  inline-flex items-center itemConfigs-center">
		<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
		<span>Rechercher</span>
	</button>

	<button  on:click={authClicked}  class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded  inline-flex  items-center itemConfigs-center">
		<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5 5a5 5 0 0 1 10 0v2A5 5 0 0 1 5 7V5zM0 16.68A19.9 19.9 0 0 1 10 14c3.64 0 7.06.97 10 2.68V20H0v-3.32z"/></svg>
		<span>Se connecter</span>
	</button>
</div>
<hr>
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


<script context="module">
  export async function preload() {
    // the `slug` parameter is available because
    // this file is called [slug].html
    const res = await this.fetch('notice.md');
    const indexMd = await res.text();
		console.log('preload')
    if (res.status === 200) {
      return { indexMd };
    } else {
      this.error(res.status, indexHTML.message);
    }
  }
</script>
<script>
	import { user, displayLogin } from '../components/stores.js';

	import marked from 'marked'
	function authClicked() {
		$displayLogin =! $displayLogin
	}
  export let indexMd;
</script>
