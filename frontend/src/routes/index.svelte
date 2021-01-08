
<svelte:head>
	<title>Moteur de recherche • Dnum</title>

	<meta name="Description" content="Moteur de recherche">
</svelte:head>

<div>
{@html innerIndex}
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
    const res = await this.fetch('innerIndex.html');
    const innerIndex = await res.text();
		console.log('preload')
		console.log(innerIndex)
    if (res.status === 200) {
      return { innerIndex };
    } else {
      this.error(res.status, data.message);
    }
  }
</script>
<script>
  export let innerIndex;
	console.log(innerIndex)
</script>
