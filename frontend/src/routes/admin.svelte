<svelte:head>
	<title>Admin</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';
	import Reindex from '../components/Reindex.svelte';
	import Threshold from '../components/Threshold.svelte';
	import NewItem from '../components/NewItem.svelte';
	import File from '../components/file-browser/File.svelte';
	import { userData } from '../common/user-data.store';
	import Accordion from '../common/accordion/Accordion.svelte';
	import AccordionItem from '../common/accordion/AccordionItem.svelte';
	import { writable } from 'svelte/store';

	let meta = [
						{
							key: 'name',
							type: 'text',
							placeholder: 'Recherchez un document...',
							value: '',
							innerHtml: '',
							size: '4/6'
						},
						{
							key: 'size',
							type: 'int',
							placeholder: 'Taille (kB)',
							value: '',
							innerHtml: '',
							size: '1/6'
						},
						{
							key: 'lastModified',
							type: 'int',
							placeholder: 'Modifié',
							value: '',
							innerHtml: '',
							size: '1/6'
						}
					]

</script>

<div class="preview text-justify">

<Accordion selection={writable(1)}>


<AccordionItem itemValue={1}>
<h1 slot="title">Ajout d'un nouveau document dans le moteur<hr></h1>
<div slot="content">
	<p>Renseignez des champs et selectionnez un fichier. Le document va être indexé
	automatiquement dans le moteur, il est inutile de reconstruire l'index Elasticsearch.</p>
	<br>
	<NewItem />
</div>
</AccordionItem>

<AccordionItem itemValue={2}>
<h1 slot="title">Reconstruction de l'index Elasticsearch<hr></h1>
<div slot="content">
<p>Cette action peut prendre du temps car tous les documents vont être réindexés.
Quand la liste des synonymes ou que la manière d'analyser les documents changent, il faut réindexer. </p>
<Reindex />
</div>
</AccordionItem>



<AccordionItem itemValue={3}>
<h1  slot="title">Gestion des seuils<hr></h1>
<div slot="content">
<p>Le seuil d'affichage fixe le nombre de documents que l'utilisateur peut visualiser après une recherche. </p>
<p>Le seuil de pertinence place un bandeau dans les résultats de recherche qui indique à l'utilisateur que les documents avec un score inférieur sont peu pertinents. </p>
<br>
<Threshold/>
</div>
</AccordionItem>


{#if ($userData.dstDir !== undefined)}
	<AccordionItem itemValue={4}>
	<h1 slot="title">Gestion des documents<hr></h1>
	<div slot="content">
	<File baseDir={$userData.dstDir} {meta} readonly={true}/>
	</div>
	</AccordionItem>

{/if}

{#if ($userData.pjDir !== undefined)}
	<AccordionItem itemValue={5}>
	<h1 slot="title">Gestion des pièces-jointes<hr></h1>
	<div slot="content">
	<p>Vous pouvez ajouter, modifier ou supprimer des pièces-jointes </p>
	<File baseDir={$userData.pjDir} {meta}/>
	</div>
	</AccordionItem>

{/if}

</Accordion>

</div>

<style>

	div.preview {
		margin: 0px auto 0px auto;
		max-width: 50rem;
	}
	h1 {
	    font-size: 2rem;
	}
	h2 {
	    font-size: 1.5rem;
	    padding-left: 20px;
	}
	hr {
	  display: block;
	  margin-top: 0.5em;
	  margin-bottom: 0.5em;
	  margin-left: auto;
	  margin-right: auto;
	  border-style: inset;
	  border-width: 1px;
	}
</style>
