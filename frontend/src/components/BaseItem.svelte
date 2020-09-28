<script>

    import PutItem from './PutItem.svelte'
    import {upload, index } from  './utils.js'

    export let meta;
    export let cssClass = 'base';
    export let readonly = false;
    export let required = true;

    let rows = 4
</script>

<section class="{cssClass}-item">

  <div class="mb-4">
    {#each meta as {key, type, placeholder, value, innerHtml, highlight, metadata, isHighlight}, i }
      {#if (key == "title") || (key == "titre")}
        <h2>
          <textarea class='{cssClass}-title' type='text' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
        </h2>

      {:else if type == "date"}
        <label> {@html innerHtml}
          {#if required}
            <input type='date' bind:value={value} {placeholder} readonly="{readonly || !metadata}" required />
          {:else}
            <input type='date' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
          {/if}
        </label>
      {:else}

      <slot name="highlight">
      </slot>

      <div>
      <label> {@html innerHtml} </label>
        {#if value instanceof Array}
          <ul>
            {#each value as val}
                <li>
                  {#if highlight && isHighlight}
                      <p> &laquo; {@html val} &raquo; </p>
                  {:else}
                    {#if type == "text"}
                        <input type='text' bind:value={val} {placeholder} readonly="{readonly || !metadata}"/>
                    {:else if type == "textarea"}
                        <textarea bind:value={val} {placeholder} readonly="{readonly || !metadata}"/>
                    {:else if type == "link"}
                        <input class={(readonly || !metadata) ? "clickable":"no-clickable"} on:click={(readonly || !metadata) ? window.open(`/api/common/files/${val}`,'_blank'): ()=>{}} type='text' bind:value={val} {placeholder} readonly="{readonly || !metadata}"/>
                    {/if}

                  {/if}
                </li>
            {/each}

          {#if !readonly  && metadata}
            <button on:click={value=[...value, "newValue"] } class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
            <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M11 9h4v2h-4v4H9v-4H5V9h4V5h2v4zm-1 11a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/></svg>
            </button>
          {/if}

          </ul>
        {:else}
          {#if highlight && isHighlight}
              <p> &laquo; {@html value} &raquo; </p>
          {:else}
            {#if type == "text"}
              <input type='text' bind:value={value} {placeholder} readonly="{readonly || !metadata}"/>
            {:else if type == "textarea"}
              <textarea bind:value={value} {placeholder} {rows} readonly="{readonly || !metadata}"/>
            {/if}
          {/if}
        {/if}
      </div>
      {/if}

    {/each}

  </div>

  <div class="flex justify-between">

    <slot name="button">
    </slot>

    <slot name="score">
    </slot>

  </div>

</section>

<style>
  .result-item {
    border: 1px solid #aaa;
    border-radius: 2px;
    box-shadow: 2px 2px 8px rgba(0,0,255,1);
    padding: 1em;
    margin: 1em 1em 1em 1em;
  }
	.base-item {
		width: 100%;
		border: 1px solid #aaa;
		border-radius: 4px;
		box-shadow: 2px 2px 8px rgba(0,0,0,1);
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

  input, textarea{
    border:none;
    width: 90%;
    resize: none;
    vertical-align: top;
   }

   p {
     display: inline;
   }

   ul {
     list-style: disc inside;
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
</style>
