<svelte:head>
	<title>Rechercher</title>
</svelte:head>

<script>
	import { onMount } from 'svelte';

	import Synonym from '../components/synonym/Synonym.svelte';

	let meta = [
						{
							key: 'expressionA',
							type: 'text',
							placeholder: 'INNOVATION',
							value: '',
							innerHtml: 'expression: ',
							size: '5/5'
						}
					]


</script>

<Synonym {meta} filename='raw_expression'/>
