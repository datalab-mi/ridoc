<script>
  import { stores } from '@sapper/app';
  import { httpClient, index, upload } from '../components/utils.js';
  import {envJson} from '../components/user-data.store'

  const { page } = stores();
  let link="/ViewerJS/#.."+$page.query.url;

  let split=$page.query.url.split('/');
  let filename=split[split.length -1];
    
  let titre;
  let date;
  let auteurs;
  let tags=[''];
  
  function getMeta(){
  httpClient().fetch('./api/user/'+$envJson['index_name']+'/_doc/'+filename)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    try{
      data['tag'].length;
     return titre=data['title'], date=data['date'], auteurs=data['author'],tags=data['tag'];}
     catch {
      return titre=data['title'], date=data['date'], auteurs=data['author']
     }
  }); 
  }
  setTimeout(getMeta,100)

</script>
<div class= "grid grid-cols justify-center">
<div class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto">
  <div class="mb-6">
    {#if tags.length>1}
    <div class="tags mb-6">
      {#each tags as tag }
    <div class="tag inline px-2 py-1 mr-4 ">{tag}</div>
    {/each}
    </div>
    {/if}
    <h1 class="text-4xl font-bold">{titre}</h1>
    <h3 class="mt-2"><bold class="font-bold">Publié le :</bold> {date}</h3>
    <h3><bold class="font-bold">Auteurs :</bold> {auteurs}</h3>
  </div>
<iframe class="place-self-center" src = {link} width='1025' height='578' allowfullscreen webkitallowfullscreen></iframe> 
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