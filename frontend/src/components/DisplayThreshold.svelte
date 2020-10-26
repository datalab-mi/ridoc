
<script>
	import { config } from '../components/utils.js';
	let promiseT = get_old_threshold();
	let oldThresholds;
	let dThreshold;
	let rThreshold;


	
	async function get_old_threshold() {
			let thresholdJson = await config('threshold.json');
			dThreshold = JSON.stringify(thresholdJson.d_threshold)
			rThreshold = JSON.stringify(thresholdJson.r_threshold)
			oldThresholds = JSON.stringify(thresholdJson)
			return oldThresholds
		}



	async function handleClick(){
			const res = await fetch(`/api/admin/put_thresholds?d_threshold=${dThreshold}&r_threshold=${rThreshold}`, {
					method: 'PUT',
					body:  oldThresholds
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
	
	{#await promiseT}
		<p>...en attente des valeurs de seuil enregistrées</p>
	{:then old_result}
		<p>Le seuil d'affichage est fixé à {dThreshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={dThreshold} min="1" max="50" >
		</div>
		
		<p>Le seuil de pertinance est fixé à {rThreshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={rThreshold} min="1" max="5" >
		</div>
	
		
		<div>
		<button on:click={handleClick} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<span>Valider les seuils</span>
		</button>
		</div>
		
		
	

		
		
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}




	
	