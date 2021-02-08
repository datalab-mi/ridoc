<script>
    import { userData } from '../common/user-data.store';
    import { USER_API, get, text_area_resize } from '../components/utils.js';
    import Tags from "svelte-tags-input";

    export let key
    export let type
    export let placeholder
    export let value
    export let innerHtml
    export let highlight
    export let metadata
    export let isHighlight

    export let readonly = false;
    export let required = true

    export let cssClass = 'base'

    export let rows = 4
    export let color = "#000066"
    let newValue = ""
    let keywordList = []
    let promiseListKeyword = new Promise(()=>{})


    if  (type === "keyword") {
      if (!readonly && metadata) {
        promiseListKeyword = get(`${USER_API}/keywords/${$userData.index_name}/${key}`)
      } else {
        promiseListKeyword = [] // no need of promiseListKeyword
      }
    }


    function onDelete(val){
      value = value.filter(item => item !== val)
    }

    function onAdd(){
      value = [...value, newValue]
      newValue = ""
    }

    function handleTags(event) {
        value = event.detail.tags;
    }

    function handleClick(val) {
      if  (readonly || !metadata) {
        let found = val.match(/(http.*)/g)
        if ( found != null) {
          window.open(found,'_blank')
        } else {
          window.open(`/api/user/files/${$userData.pjDir}/${val}`,'_blank')
        }

    }
  }
</script>

<div class="entry">
{#if (key == "title") || (key == "titre")}
  <h2 class="mb-2">
    <textarea class="{cssClass}-title" type='text' bind:value={value} {placeholder} readonly="{readonly || !metadata}" />
  </h2>

{:else if type == "date"}
  <label> {@html innerHtml} </label>
  {#if required}
    <input type='date' bind:value={value} {placeholder} readonly="{readonly || !metadata}" required />
  {:else}
    <input type='date' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
  {/if}

{:else}
  <label> {@html innerHtml} </label>
  {#if value instanceof Array}
    {#if type === "keyword"}
      {#await promiseListKeyword}
      {:then autoComplete}
        <div class="my-custom-class" style= "--color: {color}">
          <Tags
        		tags={value}
            on:tags={handleTags}
            disable={(readonly || !metadata)}
            placeholder={(readonly || !metadata) ? false:placeholder}
            allowDrop={true}
            allowPaste={true}
            onlyUnique={true}
            autoComplete={autoComplete}
            minChars={1}
            />
        </div>
        {/await}

  {:else}
      <ul>
        {#each value as val}
            <li>
              {#if highlight && isHighlight}
                  <p> &laquo; {@html val} &raquo; </p>
              {:else}
                {#if type == "text"}
                    <input type='text' bind:value={val} {placeholder} readonly="{readonly || !metadata}"/>
                {:else if type == "textarea"}
                    <textarea bind:value={val} {placeholder} readonly="{readonly || !metadata}"   />
                {:else if type == "link"}
                    <input class={(readonly || !metadata) ? "clickable":"no-clickable"} on:click={handleClick(val)} type='text' bind:value={val} {placeholder} readonly="{readonly || !metadata}"/>
                {/if}
                {#if !readonly  && metadata}
                <button on:click={() => onDelete(val)}>
                  <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
                  </button>
                {/if}
              {/if}
            </li>
        {/each}
      {#if !readonly && metadata}
        <li>
          <input type='text' bind:value={newValue} placeholder="Nouvelle entrée"/>
          <button on:click={onAdd}>
          <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M11 9h4v2h-4v4H9v-4H5V9h4V5h2v4zm-1 11a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>
          </button>
        </li>
      {/if}
      </ul>
    {/if}

  {:else}
    {#if highlight && isHighlight}
        <p> &laquo; {@html value} &raquo; </p>
    {:else}
      {#if type == "text"}
        <input type='text' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
      {:else if type == "textarea"}
        <textarea bind:value={value} {placeholder} readonly="{readonly || !metadata}" {rows} />
      {:else if type == "link"}
          <input class={(readonly || !metadata) ? "clickable":"no-clickable"} on:click={handleClick(value)} type='text' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
      {/if}
    {/if}
  {/if}
{/if}
</div>


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

	.result-item {
		border: 1px solid #aaa;
		border-radius: 2px;
		padding: 1em;
		margin: 1em 1em 1em 1em;
	}
	.base-item {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0, 0, 0, 1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
	.clickable {
		color: blue;
		font-weight: normal;
		cursor: pointer;
	}

	.no-clickable {
		color: blue;
		font-weight: normal;
	}

	.base-title {
		font-weight: bold;
		margin: 0;
		padding: 0;
	}

	.result-title {
		color: blue;
		font-weight: bold;
		margin: 0;
		padding: 0;
	}

	input,
	textarea {
		border: none;
		@apply w-full;
		resize: none;
		vertical-align: top;
		@apply bg-transparent;
	}

	p {
		display: inline;
	}

	ul {
		list-style: disc inside;
	}
</style>
