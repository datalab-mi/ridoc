<script>
import "../../static/dsfr.min.css"
</script>

<div class="fr-search-bar" id="header-search" role="search">
    <label class="fr-label" for="search-784-input">
        Recherche
    </label>
    <input class="fr-input" placeholder="Rechercher" type="search" id= "search-784-input" name="search-784-input">
    <button class= "fr-btn" title=Rechercher> Rechercher</button>
</div>

<div class="fr-toggle">
    <input type="checkbox" class="fr-toggle__input" aria-describedby="toggle-698-hint-text" id="toggle-698">
    <label class="fr-toggle__label" for="toggle-698" data-fr-checked-label="Activé" data-fr-unchecked-label="Désactivé">Label action interrupteur</label>
    <p class="fr-hint-text" id="toggle-698-hint-text">Texte d’aide pour clarifier l’action</p>
</div>

<div class="fr-select-group fr-select-group--error">
    <label class="fr-label" for="select-error">
      Label pour liste déroulante
    </label>
    <select class="fr-select fr-select--error" aria-describedby="select-error-desc-error" id="select-error" name="select-error">
      <option value="" selected disabled hidden>Selectionnez une option</option>
      <option value="1">Option 1</option>
      <option value="2">Option 2</option>
      <option value="3">Option 3</option>
      <option value="4">Option 4</option>
    </select>
    <p id="select-error-desc-error" class="fr-error-text">
      Texte d’erreur obligatoire
    </p>
  </div>

<button class="fr-btn fr-fi-checkbox-circle-line fr-btn--icon-left">
    Label bouton
</button>

