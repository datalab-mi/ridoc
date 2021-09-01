<script>
  // import { stores } from '@sapper/app';
  import { httpClient, index, upload, createMeta, isEmpty, populateIframe  } from '../components/utils.js';
  import {envJson,itemJson} from '../components/user-data.store'
  import Ratesearch from '../components/ratesearch.svelte'

  import Entry from '../components/Entry.svelte';
  import { onMount } from 'svelte';
  let titre=true;
  let meta=undefined;
  let display;
  let readonly=true;
  let required=false;
  let inputs=[];
  let _source_includes='';
  let link;
  let filename;
  let split;
  let iframe


  onMount(() => {
    //const { page } = stores(); // sveltekit
    const urlParams = new URLSearchParams(window.location.search);
    const url = urlParams.get('url');
    link="/viewer/#.."+url
    console.log("link")
    console.log(link)
    populateIframe(iframe, link);
    split=url.split('/');
    filename=split[split.length -1];


    function getMeta(){
    // Filter entries in $itemJson with isDetailed at false
    inputs = $itemJson.inputs.filter(entry => ((entry.isDetailed !== undefined) && entry.isDetailed) || (entry.isDetailed == undefined))
    _source_includes = inputs.map(x=>x.key).join()
    httpClient().fetch('./api/user/'+$envJson['index_name']+'/_doc/'+filename+"?_source_includes="+_source_includes)
    .then(response => response.json())
    .then(data => {
      [meta, display] = createMeta(inputs, data, {})
    });
    }
    function waitindex(){ //eviter les problèmes de undefined
      if($envJson['index_name']!=undefined){
      getMeta()
    }
      else{
        setTimeout(waitindex,100)
      }
    }

    waitindex()
  });



</script>

<div class= "grid grid-cols justify-center">
<div class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto">
{#if meta !=undefined && $itemJson!=undefined && filename !=undefined}

  <div class="mb-6">
    <Ratesearch class="" {filename}/>

    {#each meta as { value, key, type, placeholder, innerHtml, highlight, metadata, rows, color} (key)}
        {#if !isEmpty(value) || (!readonly && metadata) }
          <Entry {readonly} {required} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {rows} {color} />
        {/if}
    {/each}

  </div>
  {/if}

<iframe class="place-self-center" bind:this={iframe} width='1025' height='578' allowfullscreen webkitallowfullscreen></iframe>
</div>
</div>
<style>
  .card{
    max-width: min-content !important;
  }
  .tag{
    max-width: min-content !important;
    background-color: #F0F0F0;
    border-radius: 40px;
  }
</style>
