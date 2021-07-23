<script>
	import { quintOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { envJson, itemJson, searchJson } from '../../components/user-data.store';
	import { promiseSearch} from './stores.js';
	import { flatten, format2ES, search } from '../../components/utils.js';
	
	export let tags = [
		{'id':1,'description':"Calais",'done':false,'occ':23},
		{'id':2,'description':"Migrants",'done':false,'occ':3},
		{'id':3,'description':"migratoires",'done':false,'occ':2},
		{'id':4,'description':"interne",'done':false,'occ':13},
		{'id':5,'description':"OFII",'done':false,'occ':63},
		{'id':6,'description':"contrôle",'done':false,'occ':3},
	];

	$: {
		$promiseSearch
			.then((searchResults) => {
				let tagsbrut=[];
				if (searchResults.hits.length>0){
					for(let i=0;i<searchResults.hits.length;i++){
					tagsbrut.push(searchResults.hits[i]['_source']['tag'])
					}
				}
			updateTags(tagsbrut);
			
			})
			.catch((err) => {
				list_logger.concat({
					level: 'error',
					message: err,
					ressource: 'search',
				});
			});
	}

	function updateTags(tagsbrut){
		if(tagsbrut.length>0){
		let dico={};
		let tagsbrut2=tagsbrut.flat();
		tagsbrut2.forEach(element => {
			if (element in dico){
				dico[element]++;
			}
			else{
				dico[element]=1;
			}
		})
	for (let k=0;k<tags.length;k++){
			if(tags[k]['description'] in dico){
				tags[k]['occ']=dico[tags[k]['description']];
		}
			else{
				tags[k]['occ']=0;
			}
		}

		console.log(tags)
	}}

	let body;
	function handleSearch() {
		body = format2ES($itemJson, flatten($searchJson, 2).filter(x => x.type !== "button"), $envJson.index_name)
		$promiseSearch = search(body)
	}
	
	
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
	
	export function getTags(tags){
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
	auteur='';
	dateFrom='';
	dateTo='';
	}
	export function update(){
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
	
	export let dateFrom="";
	export let dateTo="";
	export let auteur="";
	let searchTerm =""
	$: tagfilt= tags.filter(tag=>tag.description.toLowerCase().indexOf(searchTerm.toLowerCase()) !==-1 && tag["occ"] !==0)

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
				<input type=checkbox bind:checked={tag.done} on:change={update}>
				{tag.description} 
			</label>
		{/each}
	</div>
	

	<h1>Filtres disponibles</h1>
	<div class='date my-5'>
		<h2>Date de publication</h2>
		A partir:
		<input type=date bind:value={dateFrom} class="border-2 my-1" on:change={update}>
		Jusqu'à:
		<input type=date bind:value={dateTo} class="border-2" on:change={update}>
	</div>
	
	<div class='Auteur my-5'>
		<h2>Auteur</h2>
		<input class="border-2 " placeholder="Nom ou Prénom" bind:value={auteur} on:change={update} />
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
				<input type=checkbox bind:checked={tag.done} on:change={update}>
				{tag.description} ({tag.occ}); 
			</label>
		{/each}
	</div>




<div class="validation flex justify-between">
	<button on:click={reset} class='resetbutton py-2 border-2 px-4 rounded'>
	Réinitialiser
</button>
	<button on:click={handleSearch} class='applybutton py-2 px-4 rounded'>
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