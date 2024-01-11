<script>
  import { onMount } from "svelte";
  import {
    httpClient,
    index,
    upload,
    createMeta,
    isEmpty,
  } from "../components/utils.js";
  import { envJson, itemJson } from "../components/user-data.store";
  import Ratesearch from "../components/ratesearch.svelte";
  import Entry from "../components/Entry.svelte";
  import { headers } from "../components/stores.js";
  let titre = true;
  let readonly = true;
  let required = false;
  let inputs = [];
  let _source_includes = "";
  let filename;
  let link;

  let iframe;

  let promiseIndex = new Promise(() => {});

  onMount(async () => {
    async function getMeta() {
      // Filter entries in $itemJson with isDetailed at false
      inputs = $itemJson.inputs.filter(
        (entry) =>
          (entry.isDetailed !== undefined && entry.isDetailed) ||
          entry.isDetailed == undefined,
      );
      _source_includes = inputs.map((x) => x.key).join();
      const response = await httpClient().fetch(
        "./backend/user/" +
          $envJson["index_name"] +
          "/_doc/" +
          filename +
          "?_source_includes=" +
          _source_includes,
      );

      const data = await response.json();
      return createMeta(inputs, data, {});
    }

    async function waitindex() {
      //eviter les problèmes de undefined
      if ($envJson["index_name"] != undefined) {
        //const { page } = stores(); // sveltekit
        const urlParams = new URLSearchParams(window.location.search);
        filename = urlParams.get("filename");
        link = `/ViewerJS/?zoom=page-width#../backend/user/files/${$envJson.dstDir}/${filename}`;
        
        const res = await fetch(link, {
          method: "GET",
          headers: $headers
        });
        const blob = await res.blob();
        const urlObject = URL.createObjectURL(blob);
        iframe.setAttribute("src", urlObject);
        const [meta, display] = await getMeta();
        console.log(meta);
        return meta;
      } else {
        console.log("wait 100ms")
        await new Promise((resolve) => setTimeout(resolve, 100));
        return await waitindex();
      }
    }

    promiseIndex = await waitindex();
  });
</script>

<svelte:head>
  <title>{filename}</title>
</svelte:head>

<div class="grid grid-cols justify-center">
  <div
    class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto"
  >
    <div class="mb-6">
      <Ratesearch class="" {filename} />

      {#await promiseIndex}
      Attente des meta données
      {:then meta}
        {#each meta as { value, key, type, placeholder, innerHtml, highlight, metadata, rows, color } (key)}
          {#if !isEmpty(value) || (!readonly && metadata)}
            <Entry
              {readonly}
              {required}
              bind:value
              {key}
              {type}
              {placeholder}
              {innerHtml}
              {highlight}
              {metadata}
              {rows}
              {color}
            />
          {/if}
        {/each}
      {/await}
    </div>

    <iframe
      title="iframe"
      bind:this={iframe}
      class="place-self-center"
      width="1025"
      height="578"
      allowfullscreen
      webkitallowfullscreen
    ></iframe>
  </div>
</div>

<style>
  .card {
    max-width: min-content !important;
  }
  .tag {
    max-width: min-content !important;
    background-color: #f0f0f0;
    border-radius: 40px;
  }
</style>
