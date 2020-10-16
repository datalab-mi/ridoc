<script>
	let d_threshold = 3;
	let promise;
	let result = null;

	async function handleClick(){
		const res = await fetch("/api/admin/put_d_threshold", {
				method: 'PUT',
				body: d_threshold
			});
		const text = await res.text();
		result = text;

		if (res.ok) {
			return text;
		} else {
			throw new Error(text);
		}
	}
		
	
</script>


<p>The display threshold is fixed at {d_threshold}</p>

<div class="slidecontainer">
  <input type="range" bind:value={d_threshold} min="1" max="5" >
</div>

<div>
  <button on:click={handleClick} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
    <span>Valider le seuil d'affichage</span>
  </button>
</div>
<p>INFO RESULT {result}</p>

<!-- svelte-ignore empty-block -->
{#await promise}
{:catch error}
	<p style="color: red">{error.message}</p>
  
{/await}