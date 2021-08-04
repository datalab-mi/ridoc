<script>
  import { stores } from '@sapper/app';
  import { httpClient, index, upload } from '../components/utils.js';
  import {envJson,itemJson} from '../components/user-data.store'
  import Ratesearch from '../components/ratesearch.svelte'

  const { page } = stores();
  let link="/ViewerJS/#.."+$page.query.url;

  let split=$page.query.url.split('/');
  export let filename=split[split.length -1];
    
  let titre=true;
  let meta;
  
  function getMeta(){
  httpClient().fetch('./api/user/'+$envJson['index_name']+'/_doc/'+filename)
  .then(response => response.json())
  .then(data => {

   return meta=data
  }); 
  }
  setTimeout(getMeta,100)

</script>
{#if meta !=undefined && $itemJson!=undefined}

<div class= "grid grid-cols justify-center">
<div class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto">
  
  <div class="mb-6">
    <Ratesearch class="" {filename}/>
    {#each $itemJson['inputs'] as item}
      {#if item['rows']==undefined}
        {#if item["type"]=='keyword' && meta[item['key']]!=undefined}
          {#each meta[item['key']] as tag}
            <div class="tag mr-4 inline p-2">{tag}</div>
          {/each}
        {:else}
          {#if meta[item['key']]!=undefined}
            {#if item['key']=='title'||item['key']=='titre'}
              <div class='titre text-3xl font-bold my-2'>{meta[item['key']]}</div>
            {:else}
          <div class="value mb-1">{@html item['innerHtml']} {meta[item['key']]}</div>
            {/if}
          {/if}
        {/if}
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