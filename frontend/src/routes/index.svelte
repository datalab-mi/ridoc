
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div>
{@html indexHTML}
</div>
<h1>Guacamole rapide à faire</h1>
<div>

<h2>Ingrédients</h2>
<ul>
  <li>2 avocats (pelés et avec les noyaux retirés)</li>
  <li>le jus d'un citron</li>
  <li>¼ de concombre, coupé grossièrement</li>
  <li>1 petite tomate, coupée</li>
</ul>

<h2>Instructions</h2>
<ol>
  <li>Écrasez délicatement les avocats avec une fourchette</li>
  <li>Placez la purée obtenue dans un plat et arrosez avec le jus de citron</li>
  <li>Mélangez pour que le jus de citron empêche la purée d'avocat de noircir</li>
  <li>Mélangez la tomate et le concombre coupés</li>
  <li>Gardez au frais et servir rapidement avec des tortillas</li>
</ol>
</div>

<style>
	:global(h1) {font-size: 2rem;}
	:global(ul) {list-style-type: circle; padding: revert;}
	:global(a) {color: blue;}

</style>

<script context="module">
  export async function preload() {
    // the `slug` parameter is available because
    // this file is called [slug].html
    const res = await this.fetch('indexHTML.html');
    const indexHTML = await res.text();
		console.log('preload')
    if (res.status === 200) {
      return { indexHTML };
    } else {
      this.error(res.status, indexHTML.message);
    }
  }
</script>
<script>
  export let indexHTML;
</script>
