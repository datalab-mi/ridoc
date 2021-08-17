<script>
    import Rate from "./Rate.svelte";
    import {rateJson} from "../user-data.store";

    const beforeRate = rate => {
      console.log(rate);
    };
    const afterRate = rate => {
      if ($rateJson.length<1){
      $rateJson.push(rate)
      console.log($rateJson) // TODO: insérer ici lien vers la BDD
      } else {
        window.alert("Vous avez déjà voté")
      }
    };
  </script>

  <div class="Rateblock float-right mt-12 bg-white p-4 max-w-xs">
  <div class="titre text-xl"><b class="underline">Votre avis</b> nous intéresse</div>
  <p class="break-normal">Comment décririez-vous votre expèrience sur le site ?</p>
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
