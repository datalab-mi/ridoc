<script>
  import { stores } from '@sapper/app';
  import { httpClient, index, upload, createMeta, isEmpty  } from '../components/utils.js';
  import {envJson,itemJson} from '../components/user-data.store'
  import Ratesearch from '../components/ratesearch.svelte'

  import Entry from '../components/Entry.svelte';

  const { page } = stores();
  let link="/ViewerJS/?zoom=page-width#.."+$page.query.url;

  let split=$page.query.url.split('/');
  export let filename=split[split.length -1];

  let titre=true;
  let meta;
  let display;
  let readonly=true;
  let required=false;
  let inputs=[];
  let _source_includes='';

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

</script>
{#if meta !=undefined && $itemJson!=undefined}

<div class= "grid grid-cols justify-center">
<div class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto">

  <div class="mb-6">
    <Ratesearch class="" {filename}/>

    {#each meta as { value, key, type, placeholder, innerHtml, highlight, metadata, rows, color} (key)}
        {#if !isEmpty(value) || (!readonly && metadata) }
          <Entry {readonly} {required} bind:value {key} {type} {placeholder} {innerHtml} {highlight} {metadata} {rows} {color} />
        {/if}
    {/each}

  </div>
<iframe class="place-self-center" src = {link} width='1025' height='578' allowfullscreen webkitallowfullscreen></iframe>
</div>
</div>
{/if}
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
