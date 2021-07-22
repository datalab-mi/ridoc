<script>
	import { quintOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { envJson, itemJson, searchJson } from '../../components/user-data.store';

	
	
	const [send, receive] = crossfade({
		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === 'none' ? '' : style.transform;

			return {
				duration: 600,
				easing: quintOut,
				css: t => `
					transform: ${transform} scale(${t});
					opacity: ${t}
				`
			};
		}
	});
	
	function getTags(tags){
	let selectedtags=tags.filter(tag=>tag.done==true)
	let activeTags=[]
	for (let i=0;i<selectedtags.length;i++){
		activeTags.push(selectedtags[i].description)
	}
	return activeTags;
	}

	function reset(){
		for(let i=0;i<tags.length;i++){
	 tags[i].done=false;
		}
	}
	function apply(){
	for (let pas=0;pas<$searchJson[1].length;pas++){
		if ($searchJson[1][pas].type=="search"){
			$searchJson[1][pas].value=auteur;
		}
		else if($searchJson[1][pas].innerHtml=="A partir de : "){
			$searchJson[1][pas].value=dateFrom;
		}
		else if($searchJson[1][pas].innerHtml=="Jusqu'à : "){
			$searchJson[1][pas].value=dateTo;
		}
	}
	$searchJson[2][0].value=getTags(tags);
	}
	function occurence(categorie){
	//renvoie l'occurence de  la cat�gorie dans la recherche
	}
	
	let tags = [
		{ id: 1, done: false, description: 'Comptable' },
		{ id: 2, done: false, description: 'Financier' },
		{ id: 3, done: false, description: 'Compte' },
		{ id: 4, done: false, description: 'OFFI' },
		{ id: 5, done: false, description: 'Innondations' },
		{ id: 6, done: false, description: 'Aidant' },
	];

	

	export let dateFrom="";
	export let dateTo="";
	export let auteur="";
	let searchTerm =""
	$: tagfilt= tags.filter(tag=>tag.description.toLowerCase().indexOf(searchTerm.toLowerCase()) !==-1)

</script>

<div class='board'>
	<div class='Factif mb-10 border-b-2'>
		<h1>Filtres actifs</h1>
		{#each tags.filter(t => t.done) as tag (tag.id)}
			<label
				in:receive="{{key: tag.id}}"
				out:send="{{key: tag.id}}"
				animate:flip
			>
				<input type=checkbox bind:checked={tag.done}>
				{tag.description} 
			</label>
		{/each}
	</div>
	

	<h1>Filtres disponibles</h1>
	<div class='date my-5'>
		<h2>Date de publication</h2>
		A partir:
		<input type=date bind:value={dateFrom} class="border-2 my-1">
		Jusqu'à:
		<input type=date bind:value={dateTo} class="border-2">
	</div>
	
	<div class='Auteur my-5'>
		<h2>Auteur</h2>
		<input class="border-2 " placeholder="Nom ou Prénom" bind:value={auteur} />
	</div>
	
	<div class='categories my-5'>
		<h2>Catégories</h2>
		<input bind:value={searchTerm} class="border-2 " placeholder="Rechercher..." />

		{#each tagfilt.filter(t => !t.done) as tag (tag.id)}
			<label
				in:receive="{{key: tag.id}}"
				out:send="{{key: tag.id}}"
				animate:flip
			>
				<input type=checkbox bind:checked={tag.done}>
				{tag.description} ({occurence(tag.description)}); 
			</label>
		{/each}
	</div>




<div class="validation flex justify-between">
	<button on:click={reset} class='resetbutton py-2 border-2 px-4 rounded'>
	Réinitialiser
</button>
	<button on:click={apply} class='applybutton py-2 px-4 rounded'>
	Appliquer
</button>
	
	
	</div>

</div>

<style>


	.board {
		@apply shadow;
		@apply h-full;
		width:15%;
		float:left;
		background-color: white;
		padding: 10pt;
		
	}

	.categories, .Factif {
		padding: 0 1em 0 0;
	}

	h2 {
		font-size: 1.2em;
		font-weight: bold;
		user-select: none;
		margin-bottom: 3px;

	}
	h1{
		font-size: 1.8em;
		font-weight: bold;
		user-select: none;
		padding-bottom: 10px;
		
	}

	label {
		top: 0;
		left: 0;
		display: block;
		font-size: 1em;
		line-height: 1;
		padding: 0.5em;
		margin: 0 auto 0.5em auto;
		border-radius: 10px;
		user-select: none;
	}
	.Factif label{
	background-color: var(--secondary);
		width:fit-content;
		margin-left:0;
		margin-right:1em;
	}
	
	input { 
			border-color: var(--primary)}
	

		select{
			border-color: var(--primary);
;
		}
	
	.resetbutton{
	color: var(--primary);
	border-color:var(--primary);
	}
	.applybutton{
		background-color:var(--primary);
		color:white;
	}

	
</style>