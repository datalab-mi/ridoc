<script>
	import { quintOut } from "svelte/easing";
	import { crossfade } from "svelte/transition";
	import { flip } from "svelte/animate";
	import { onMount } from "svelte";
	import { USER_API, get } from "../../components/utils.js";

	import {
		envJson,
		itemJson,
		searchJson,
	} from "../../components/user-data.store";
	import { promiseSearch } from "./stores.js";
	import { list_logger } from "../../components/stores.js";
	import {
		flatten,
		format2ES,
		search,
		httpClient,
	} from "../../components/utils.js";
	import SearchInput from "./SearchInput.svelte";
	import SearchKeywordInput from "./SearchKeywordInput.svelte";
	import SearchSuggestInput from "./SearchSuggestInput.svelte";
	import Accordion from "../../components/accordion/Accordion.svelte";
	import AccordionItem from "../../components/accordion/AccordionItem.svelte";

	let tags = {};

	let keywordList = [];
	let styleInput = "border-2 w-full";
	let promiseListKeyword;
	let tagfilt;
	let searchTerm = {};

	function init() {
		// get keyword field in the aside
		$searchJson[1].forEach(function (part, index) {
			if (part.type === "keyword") {
				const field = this[index].fields;
				keywordList.push(field);
				tags[field] = [];
			}
		}, $searchJson[1]); // use arr as this

		keywordList.forEach((field) => {
			promiseListKeyword = get(
				`${USER_API}/keywords/${$envJson.index_name}/${field}`
			);
			promiseListKeyword
				.then((listKeyword) => {
					listKeyword.forEach((x, i) => {
						tags[field].push({
							id: i + 1,
							description: x,
							done: false,
							occ: 1,
						});
					});
				})
				.catch((err) => {
					list_logger.concat({
						level: "error",
						message: err,
						ressource: "keywords",
					});
				});
		});

		keywordList.forEach((x) => (searchTerm[x] = ""));
	}

	function waitindex() {
		//avoid undefined index issues
		if ($envJson["index_name"] !== undefined && $searchJson.length > 0) {
			init();
		} else {
			setTimeout(waitindex, 100);
		}
	}
	waitindex();

	$: {
		$promiseSearch
			.then((searchResults) => {
				keywordList.forEach((keyTag) => {
					let tagsbrut = [];
					if (searchResults.hits.length > 0) {
						searchResults.hits.forEach((hits) => {
							if (hits["_source"][keyTag] !== undefined) {
								tagsbrut.push(hits["_source"][keyTag]);
							}
						});
					}
					updateTags(tagsbrut, keyTag);
				});
			})
			.catch((err) => {
				console.log(err);
			});
	}
	function lowerandaccent(list) {
		return list.map((e) => e.toLowerCase().replace(/é|è|ê/g, "e"));
	}

	function updateTags(tagsbrut, keyTag) {
		//change les occurences selon la recherche
		//console.log(tagsbrut);
		if (tagsbrut.length > 0) {
			let dico = {};
			let tagsbrut2 = lowerandaccent(tagsbrut.flat());
			//console.log(tagsbrut2)
			tagsbrut2.forEach((element) => {
				if (element in dico) {
					dico[element]++;
				} else {
					dico[element] = 1;
				}
			});
			for (let k = 0; k < tags[keyTag].length; k++) {
				if (tags[keyTag][k]["description"] in dico) {
					tags[keyTag][k]["occ"] =
						dico[tags[keyTag][k]["description"]];
				} else {
					tags[keyTag][k]["occ"] = 0;
				}
			}
		} else {
			for (let k = 0; k < tags[keyTag].length; k++) {
				tags[keyTag][k]["occ"] = 0;
			}
		}
	}

	let body;
	function handleSearch() {
		//lance la recherche selon le fichier item.json
		body = format2ES(
			$itemJson,
			flatten($searchJson, 2).filter((x) => x.type !== "button"),
			$envJson.index_name
		);
		$promiseSearch = search(body);
	}

	const [send, receive] = crossfade({
		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === "none" ? "" : style.transform;

			return {
				duration: 10,
				easing: quintOut,
				css: (t) => `
					transform: ${transform} scale(${t});
					opacity: ${t}
				`,
			};
		},
	});

	function getKeywords(field) {
		//renvoie la liste des noms de tags selectionnés
		let selectedtags = tags[field].filter((tag) => tag.done); // === true)
		let activeTags = [];
		for (let i = 0; i < selectedtags.length; i++) {
			activeTags.push(selectedtags[i].description);
		}
		return activeTags;
	}

	function reset() {
		// Remove selected keywords
		keywordList.forEach((keyTag) => {
			for (let i = 0; i < tags[keyTag].length; i++) {
				tags[keyTag][i].done = false;
			}
		});
		// Remove values in $searchJson
		$searchJson[1].forEach(function (part, index) {
			this[index].value = "";
		}, $searchJson[1]); // use arr as this
		console.log($searchJson[1]);
		// Reset all inputs
		var inputs = document.querySelectorAll(
			"input[type=search],input[type=date],input[type=text]"
		);
		for (var i = 0; i < inputs.length; i++) {
			inputs[i].value = "";
		}
	}

	function update() {
		// update le fichier searchJson avec les champs keeyword selectionnés
		$searchJson[1].forEach(function (part, index) {
			if (part.type === "keyword") {
				const field = this[index].fields;
				this[index].value = getKeywords(field);
			}
		}, $searchJson[1]); // use arr as this
	}

	$: {
		keywordList.forEach((keyTag) => {
			if (keyTag in tags) {
				tagfilt = tags[keyTag].filter(
					(entry) =>
						entry["occ"] !== 0 &&
						entry.description
							.toLowerCase()
							.indexOf(searchTerm[keyTag].toLowerCase()) !== -1
				);
			}
		});
	}
</script>

<div class="board">
	<div class="Factif border-b-2 mx-5">
		<h1>Filtres actifs</h1>
		{#if !Object.values(tags).some((tag) => tag.some((t) => t.done))}
			<div class="mb-10">Aucun filtre actif</div>
		{/if}
		{#each keywordList as keyTag}
			{#if keyTag in tags}
				{#if tags[keyTag].some((t) => t.done)}
					{#each tags[keyTag].filter((t) => t.done) as tag (tag.id)}
						<label
							in:receive={{ key: tag.id + keyTag }}
							out:send={{ key: tag.id + keyTag }}
							animate:flip
						>
							<input
								type="checkbox"
								bind:checked={tag.done}
								on:change={update}
							/>
							{tag.description}
						</label>
					{/each}
				{/if}
			{/if}
		{/each}
	</div>

	<h1 class="mx-5">Filtres disponibles</h1>

	<!-- recherche avancée dans le 2eme element de la liste de searchJson  -->
	{#if $searchJson !== "undefined" && $searchJson.length > 1}
		<Accordion containerClass={"mt-4 mx-5"}>
			{#each $searchJson[1] as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
				<AccordionItem>
					<div slot="title">
						<h2>{innerHtml}</h2>
					</div>
					<div slot="content" class="flex-col">
						<div class="flex flex-col">
							{#if type === "keyword"}
								<div>
									<input
										type="search"
										bind:value={searchTerm[fields]}
										class="border-2 w-full"
										{placeholder}
									/>
									<div class="tags">
										{#if fields in tags}
											{#each tags[fields].filter((entry) => !entry.done && entry["occ"] !== 0 && entry.description
														.toLowerCase()
														.indexOf(searchTerm[fields].toLowerCase()) !== -1) as tag (tag.id)}
												<label
													in:receive={{
														key: tag.id + fields,
													}}
													out:send={{
														key: tag.id + fields,
													}}
													animate:flip
												>
													<input
														type="checkbox"
														bind:checked={tag.done}
														on:change={update}
													/>
													{tag.description}
													<b class="occ gray-200"
														>{tag.occ}</b
													>
												</label>
											{/each}
										{/if}
									</div>
								</div>
							{:else if type === "search" && suggest}
								<SearchSuggestInput
									bind:value
									{placeholder}
									{style}
									{styleInput}
								/>
							{:else}
								<SearchInput
									bind:value
									{type}
									{placeholder}
									{style}
									{styleInput}
								/>
							{/if}
						</div>
					</div>
				</AccordionItem>
			{/each}
		</Accordion>
	{/if}

	<ul class="fr-btns-group fr-btns-group--inline">
		<li>
			<button on:click={reset} class="fr-btn fr-btn--secondary">
				Réinitialiser
			</button>
		</li>

		<li>
			<button on:click={handleSearch} class="fr-btn"> Appliquer </button>
		</li>
	</ul>
</div>

<style>
	.board {
		@apply shadow;
		/* width:20%; */
		max-width: 18rem;

		/* float:left; */
		background-color: white;
		padding: 10pt;
		border-color: #e1e1e1;
		border-width: 1px;
	}

	.categories,
	.Factif {
		padding: 0 0 0 0;
	}

	h2 {
		font-size: 16px;
		font-weight: bold;
		user-select: none;
		margin-bottom: 3px;
	}
	h1 {
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
	.Factif label {
		background-color: var(--secondary);
		width: fit-content;
		margin-left: 0;
		margin-right: 1em;
	}

	input {
		border-color: var(--primary);
		max-width: 10rem;

	}

	.tags {
		max-height: 30vh;
		overflow-y: scroll;
	}
	.occ {
		color: rgb(185, 182, 182) !important;
	}
</style>
