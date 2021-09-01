<script>
	import { quintOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { envJson, itemJson, searchJson } from '../../components/user-data.store';
	import { promiseSearch} from './stores.js';
	import { flatten, format2ES, search, httpClient} from '../../components/utils.js';
	
	let tags1
	let tags=[]
	let tag_name

	function init(){
		tags1 =initialTags()
		tags1.then(function(result){return tags=result});
		}
		
	function initialTags(){
	let inittag = httpClient().fetchJson('api/user/keywords/'+$envJson['index_name']+'/'+tag_name).then(response=>response).then(data=> data).then(tagslist=> {return tagsinit(tagslist)})
	return inittag;
}
	
	function tagsinit(tagslist){
		let tags=[]
		for (let i=0;i<tagslist.length;i++){
			tags.push({'id':i+1,'description':tagslist[i],'done':false,'occ':' '})
		}
		return tags
		
		
	}

	function waitindex(){ //avoid undefined index issues
		for (let element in $itemJson['inputs']){
			if ($itemJson['inputs'][element]['type']=="keyword"){
				tag_name=$itemJson['inputs'][element]['key']
			}
		}
		if ($envJson['index_name']!=undefined && tag_name!=undefined){
			init()
			console.log($itemJson['inputs'])
			
		}
		else{
			setTimeout(waitindex,100)
		}
	}
	waitindex()

	$: {
		$promiseSearch
			.then((searchResults) => {
				let tagsbrut=[];
				if (searchResults.hits.length>0){
					for(let i=0;i<searchResults.hits.length;i++){
						if(searchResults.hits[i]['_source'][tag_name]!==undefined)
						{console.log(searchResults.hits[i]['_source'][tag_name])
					tagsbrut.push(searchResults.hits[i]['_source'][tag_name])}

					}
				}
			
			updateTags(tagsbrut);
			})
			.catch((err) => {
				console.log('erreur')
			});
	}
	function lowerandaccent(list){
		let l=[]
		for (let i=0;i<list.length;i++){
			let el=list[i].toLowerCase();
			el = el.replace(/é|è|ê/g,"e");
			l.push(el)
		}
		return l
	}
	function updateTags(tagsbrut){ //change les occurences selon la recherche
		if(tagsbrut.length>0){
		let dico={};
		let tagsbrut2=lowerandaccent(tagsbrut.flat());
		console.log(tagsbrut2)
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
	}
		else{
			for (let k=0;k<tags.length;k++){
				tags[k]['occ']=0;
		}}
	}

	let body;
	function handleSearch() { //lance la recherche selon le fichier item.json
		body = format2ES($itemJson, flatten($searchJson, 2).filter(x => x.type !== "button"), $envJson.index_name)
		$promiseSearch = search(body)
	}
	
	
	const [send, receive] = crossfade({
		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === 'none' ? '' : style.transform;

			return {
				duration: 10,
				easing: quintOut,
				css: t => `
					transform: ${transform} scale(${t});
					opacity: ${t}
				`
			};
		}
	});
	
	function getTags(tags){ //renvoie la liste des noms de tags selectionnés
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
	update()
	}
	function update(){ // update le fichier searchJson avec les champs selectionnés
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
	
	let dateFrom="";
	let dateTo="";
	let auteur="";
	let searchTerm =""
	$: tagfilt= tags.filter(tag=>tag.description.toLowerCase().indexOf(searchTerm.toLowerCase()) !==-1 && tag["occ"] !==0)
</script>
<div class='board'>
	<div class='Factif border-b-2 mx-5 '>
		<h1>Filtres actifs</h1>
		{#if tags.filter(t => t.done).length>0}
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
		{:else}
		<div class="mb-10">Aucun filtre actif </div>
		{/if}

	</div>

	<h1 class="mx-5">Filtres disponibles</h1>
	<div class='date mb-5 mx-5'>
		<h2>Date de publication</h2>
		A partir:
		<input type=date bind:value={dateFrom} class="border-2 my-1" on:change={update}> <br>
		Jusqu'à : 
		<input type=date bind:value={dateTo} class="border-2" on:change={update}>
	</div>
	
	<div class='Auteur my-3 mx-5'>
		<h2>Auteur</h2>
		<input class="border-2 w-full" placeholder="Nom ou Prénom" bind:value={auteur} on:change={update} />
	</div>
	
	<div class='categories my-3 mx-5'>
		<h2>Catégories</h2>
		<input bind:value={searchTerm} class="border-2 w-full" placeholder="Rechercher..." />
		<div class="tags">
		{#each tagfilt.filter(t => !t.done) as tag (tag.id)}
			<label
				in:receive="{{key: tag.id}}"
				out:send="{{key: tag.id}}"
				animate:flip
			>
				<input type=checkbox bind:checked={tag.done} on:change={update}>
				{tag.description} <b class="occ gray-200 ">{tag.occ}</b> 
			</label>
		{/each}
		</div>
	</div>




<ul class="fr-btns-group fr-btns-group--inline">
	<li>
	<button on:click={reset} class="fr-btn fr-btn--secondary">
	Réinitialiser
	</button></li>

	<li>
	<button on:click={handleSearch} class='fr-btn'>
	Appliquer
	</button></li>
</ul>
	

</div>
<style>


	.board {
		@apply shadow;
		min-width:15%;
		float:left;
		background-color: white;
		padding: 10pt;
		border-color: #E1E1E1;
		border-width: 1px;
	}

	.categories, .Factif {
		padding: 0 0 0 0;
	}

	h2 {
		font-size: 16px;
		font-weight: bold;
		user-select: none;
		margin-bottom: 3px;

	}
	h1{
		font-size: 24px;
		font-weight: bold;
		user-select: none;
		
	}

	label {
		top: 0;
		left: 0;
		display: block;
		font-size: 16px;
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
			border-color: var(--primary); }
	
	
	.tags{
		height: 30vh;
		overflow-y: scroll;
	}
	.occ{
		color: rgb(185, 182, 182) !important;
	}

</style>