<script>
	import { get } from '../components/utils.js';
	import { list_logger  } from './stores.js';

	let promise = get_old_threshold();
	let thresholds = {};

	async function get_old_threshold() {
			thresholds = await get('/api/common/files/threshold.json');
			return 200
		}

	async function handleClick(){
			const res = await fetch(`/api/admin/threshold`, {
					method: 'PUT',
					body:  JSON.stringify(thresholds)
				});
			const text = await res.text();
			if (res.ok) {
				return text;
			} else {
				list_logger.concat({level: "error", message: "Non authorisé", ressource: "thresold"})
				throw new Error("Oups");
			}
		}
	</script>

	{#await promise}
		<p>...en attente des valeurs de seuil enregistrées</p>
	{:then status}
		<p>Le seuil d'affichage est fixé à {thresholds.d_threshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={thresholds.d_threshold} min="0" max="50" >
		</div>

		<p>Le seuil de pertinence est fixé à {thresholds.r_threshold}</p>
		<div class="slidecontainer">
		<input type="range" bind:value={thresholds.r_threshold} min="0" max="5" >
		</div>

		<div>
		<button on:click={handleClick} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 10v6H7v-6H2l8-8 8 8h-5zM0 18h20v2H0v-2z"/></svg>
			<span>SOUMETTRE</span>
		</button>
		</div>

	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
