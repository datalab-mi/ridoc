
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div class="preview">
{@html indexHTML}
</div>
<div class="preview">{@html indexHTML}</div>

<style>
	h1 {font-size: 2rem;}
	div.preview ul {list-style-type: circle; padding: revert;}
	div.preview a {color: blue;}
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
	indexHTML='<h1 id="example-title">Example Title</h1> <ul> <li>this</li> <li>is</li> <li>a list</li> </ul>'
	console.log(indexHTML)
</script>
