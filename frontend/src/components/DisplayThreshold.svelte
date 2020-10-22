
<script>
	import { config } from '../components/utils.js';
	let promise_t = get_old_threshold();
	let old_thresholds;
	let d_threshold;
	let r_threshold;
	let result = null;


	
	async function get_old_threshold() {
			let threshold_json = await config('threshold.json');
			d_threshold = JSON.stringify(threshold_json.d_threshold)
			r_threshold = JSON.stringify(threshold_json.r_threshold)
			old_thresholds = JSON.stringify(threshold_json)
			return old_thresholds
		}



	async function handleClick(){
			const res = await fetch(`/api/admin/put_thresholds?d_threshold=${d_threshold}&r_threshold=${r_threshold}`, {
					method: 'PUT',
					body:  old_thresholds
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
	
	{#await promise_t}
		<p>...en attente des valeurs de seuil enregistrées</p>
	{:then old_result}

		<p>Le seuil d'affichage est fixé à {d_threshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={d_threshold} min="1" max="10" >
		</div>
		
		<p>Le seuil de pertinance est fixé à {r_threshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={r_threshold} min="1" max="10" >
		</div>
		
		
		<div>
		<button on:click={handleClick} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<span>Valider les seuils</span>
		</button>
		</div>
		
		<p>INFO status result {result}</p>
		<p>INFO old result {old_result}</p>
		<p>INFO d_threshold {d_threshold}</p>
		<p>INFO r_threshold {r_threshold}</p>
	

		
		
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
	
	