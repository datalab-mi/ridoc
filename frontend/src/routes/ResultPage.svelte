<script>
  import { stores } from '@sapper/app';
  import { httpClient, index, upload } from '../components/utils.js';

  const { page } = stores();
  let link="/ViewerJS/#.."+$page.query.url;

  let split=$page.query.url.split('/');
  let filename=split[split.length -1].split('.')[0];
    
  let titre;
  let date;
  let auteurs;
  
  httpClient().fetch('./api/user/files/meta/'+filename+'.json')
  .then(response => response.json())
  .then(data => {
    return titre=data['title'], date=data['date'], auteurs=data['author']
  }); 


</script>
<div class="bg-white mx-32 p-10">
    <h1 class="text-4xl font-bold">{titre}</h1>
    <h3><bold class="font-bold">Publié le :</bold> {date}</h3>
    <h3><bold class="font-bold">Auteurs :</bold> {auteurs}</h3>

<iframe src = {link} width='1025' height='578' allowfullscreen webkitallowfullscreen></iframe> 
</div>