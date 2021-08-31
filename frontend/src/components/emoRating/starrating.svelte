<script>
    import Rate from "./Rate.svelte";
    import {searchRateJson} from "../user-data.store";

    const beforeRate = rate => {
      console.log(rate);
    };
    const afterRate = rate => {
      if ($searchRateJson.length<1){
      $searchRateJson.push(rate)
      console.log($searchRateJson) // TODO: insérer ici lien vers la BDD
      } else {
        window.alert("Vous avez déjà voté")
      }
    };
  </script>

  <div class="Rateblock float-right mt-12 bg-white p-4 max-w-xs shadow">
  <div class="titre text-xl"><b class="underline">Votre avis</b> nous intéresse</div>
  <p class="break-normal my-0">Comment décririez-vous votre expérience sur le site ?</p>
  <Rate
    {beforeRate}
    {afterRate}
    length={5}
    ratedesc={['Très mauvaise', 'Mauvaise', 'Normale', 'Bonne', 'Très bonne']}
    showCount={true} />

  </div>

  <style>
      .titre{
          color:var(--primary)
      }
  </style>
