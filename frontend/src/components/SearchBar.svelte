<script>
	import Accordion from '../common/accordion/Accordion.svelte';
	import AccordionItem from '../common/accordion/AccordionItem.svelte';
	import { cssProps } from '../common/css-props.action';
	import { userTheme } from '../common/theme.store';
	import { userData } from '../common/user-data.store';
	import SearchInput from '../components/SearchInput.svelte';
	import SearchKeywordInput from '../components/SearchKeywordInput.svelte';
	import SearchSuggestInput from '../components/SearchSuggestInput.svelte';
	import { itemConfig, promiseSearch, searchList } from '../components/stores.js';
	import { format2ES, search } from '../components/utils.js';

	const bgColorProp = '--search-criteria-bg-color';
	const styleProps = {};

	let body
	
	$: styleProps[bgColorProp] =
		$userTheme.search &&
		$userTheme.search.criteria &&
		$userTheme.search.criteria.backgroundColor
			? $userTheme.search.criteria.backgroundColor
			: undefined;

	function handleSearch() {
		body = format2ES($itemConfig, $searchList, $userData.index_name)
		$promiseSearch = search(body)
	}
</script>

<div class='search-bar' on:keyup={e => e.key === 'Enter' && handleSearch()}
	use:cssProps={styleProps} style="background-color: var({bgColorProp})">

{#if $searchList.length > 0}

	<!-- recherche basique -->
	{#each $searchList as row, i}
		{#each row as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
			{#if i === 0 && j === 0}
				<div class="flex flex-row-reverse">
					<div class="flex-none my-auto" >
						<button on:click={handleSearch} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded inline-flex items-center itemConfigs-center">
							<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"/></svg>
							<span>Rechercher</span>
						</button>
					</div>
					{#if type === 'keyword' }
						<SearchKeywordInput bind:value={value} {fields} {placeholder} {color} />
					{:else if type === 'search' && suggest }
						<SearchSuggestInput bind:value={value} {placeholder} {innerHtml} style="flex-1 my-auto {style}" />
					{:else }
						<SearchInput bind:value={value} {type} {placeholder} {innerHtml} style="flex-1 my-auto {style}" />
					{/if}
				</div>
			{/if}
		{/each}
	{/each}

	<!-- recherche avancée -->
	{#if $searchList[0].length > 1 || $searchList.length > 1}
		<Accordion containerClass="mt-4">
			<AccordionItem title="Recherche avancée">
				<div slot="content">
					{#each $searchList as row, i}
						{#if i !== 0 || row.length > 1}
							<div class="flex mb-4">
								{#each row as { fields, value, type, placeholder, innerHtml, style, color, suggest }, j}
									{#if i !== 0 || j !== 0}
										{#if type === 'keyword' }
											<SearchKeywordInput bind:value={value} {fields} {placeholder} {color} />
										{:else if type === 'search' && suggest }
											<SearchSuggestInput bind:value={value} {placeholder} {innerHtml} {style} />
										{:else }
											<SearchInput bind:value={value} {type} {placeholder} {innerHtml} {style} />
										{/if}
									{/if}
								{/each}
							</div>
						{/if}
					{/each}
				</div>
			</AccordionItem>
		</Accordion>
	{/if}

{:else}
	<p>...Attente de la config</p>
{/if}

</div>

<style>
	.search-bar {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		padding: 1em;
		margin: 0 0 1em 0;
		background-color: var(--bg-color);
	}
</style>
