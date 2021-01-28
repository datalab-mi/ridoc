<script>
  import Tags from "svelte-tags-input"
  import { userData } from '../components/stores.js';
  import { get } from '../components/utils.js';

  export let innerHtml = ""
  export let style = ""
  export let placeholder = ""
  export let fields = ""
  export let value = ""
  export let type = "text"
  export let color = "#000"

  let promiseListKeyword = new Promise(()=>{})

  if  (type === "keyword") {
    promiseListKeyword = get(`api/user/keywords/${$userData.index_name}/${fields}`)
  }
  const handleInput = e => {
    // in here, you can switch on type and implement
    // whatever behaviour you need
    value = type.match(/^(number|range)$/)
      ? +e.target.value
      : e.target.value
  };

  function handleTags(event) {
      value = event.detail.tags;
  }

</script>

{#if type === "keyword"}
  {#await promiseListKeyword}
  {:then autoComplete}
    <div class="my-custom-class" style= "--color: {color}">
      <Tags
        tags={value}
        on:tags={handleTags}
        placeholder={placeholder}
        allowDrop={true}
        allowPaste={true}
        onlyUnique={true}
        autoComplete={autoComplete}
        minChars={0}
        />
    </div>
  {/await}

{:else}
  <div class={style}>
    <label> {@html innerHtml}
      <input {type} {value} {placeholder} on:input={handleInput}
        class="bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal">
    </label>
  </div>
{/if}



<style>
  /* override default Tag style */
  .my-custom-class :global(.svelte-tags-input-tag) {
      background: var(--color) !important;
      cursor: default !important;;
  }
  .my-custom-class :global(.svelte-tags-input-layout) {
      background:#FFF !important;
      border-style: none !important;
      cursor: default !important;;
  }
  .my-custom-class :global(.svelte-tags-input) {
      background:#FFF !important;
      cursor: default !important;;
  }
  </style>
