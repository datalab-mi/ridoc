
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div>
  <h1>Moteur de recherche</h1><br>

  <p>
    Cet outil est un moteur de recherche documentaire fondé sur Elasticsearch,
    python et Svelte.
  </p>
</div>

<style>
	h1 {
	    font-size: 2rem;
	}

</style>


<script context="module">
  export async function preload() {
    // the `slug` parameter is available because
    // this file is called [slug].html
    const res = await this.fetch('data.json');
    const data = await res.json();
		console.log('preload')
		console.log(data)
    if (res.status === 200) {
      return { indexData: data };
    } else {
      this.error(res.status, data.message);
    }
  }
</script>
<script>
  export let indexData;
</script>
