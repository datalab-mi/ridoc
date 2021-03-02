<svelte:head>
	<title>Tests</title>
</svelte:head>

<script>
	import { elasticInOut, expoInOut } from 'svelte/easing';
	import { writable } from 'svelte/store';
	import Accordion from '../components/accordion/Accordion.svelte';
	import AccordionItem from '../components/accordion/AccordionItem.svelte';

	export let selection1 = writable(null);
	export let selection2 = writable(null);

	/** preuve qu'on peut modifier un contenu "slot" mais ce n'est pas trivial */
	const toggleImage = (event) => {
		const expanded = event.detail.expanded;
		const node = event.detail.itemNode;
		const svgCollapsed = node.querySelector('svg.collapsed');
		const svgExpanded = node.querySelector('svg.expanded');

		const toShow = expanded ? svgExpanded : svgCollapsed;
		toShow.classList.add('inline-block');
		toShow.classList.remove('hidden');

		const toHide = expanded ? svgCollapsed : svgExpanded;
		toHide.classList.remove('inline-block');
		toHide.classList.add('hidden');
	};
</script>

<ul>
	<AccordionItem>
		<p slot="title" class="text-2xl font-bold">AccordionItem</p>
		<div slot="content" class="grid grid-cols-1">
			<div>
				<p>par défaut</p>
				<ul>
					<AccordionItem />
				</ul>
			</div>

			<div>
				<p>avec contenu simple</p>
				<ul>
					<AccordionItem title="exemple de titre" content="exemple de contenu" />
				</ul>
			</div>

			<div>
				<p>avec slots</p>
				<ul>
					<AccordionItem on:expand={e => toggleImage(e)}>
						<span slot="title">
							Encore<br />
							un <strong>exemple de titre</strong>
							<svg class="collapsed inline-block w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
							<svg class="expanded hidden w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
							</svg>
						</span>
						<div slot="content" style="height: 180px; position: relative">
							<p class="absolute bottom-0 right-0">
								<i>exemple de contenu</i> formaté
							</p>
						</div>
					</AccordionItem>
				</ul>
			</div>

			<div>
				<p>ouvert au départ</p>
				<ul>
					<AccordionItem selection={writable('peuImporte')} itemValue={'peuImporte'} />
				</ul>
			</div>

			<div>
				<p>avec transition personnalisée</p>
				<ul>
					<AccordionItem title="easing" itemValue={1} contentStyle="height: 100px" slideParams={{ easing: elasticInOut }} />
					<AccordionItem title="durée" itemValue={2} contentStyle="height: 200px" slideParams={{ duration: 5000 }} />
					<AccordionItem title="durée + easing" itemValue={3} contentStyle="height: 300px" slideParams={{ duration: 3000, easing: expoInOut }} />
				</ul>
			</div>

			<div>
				<p>avec styles</p>
				<ul>
					<AccordionItem
						itemClass="bg-green-500 p-2"
						itemStyle="cursor: wait"
						buttonClass="border-4 border-red-500"
						buttonStyle="cursor: not-allowed"
						contentClass="bg-gray-500"
						contentStyle="cursor: default"
					/>
				</ul>
			</div>

			<div>
				<p>groupe (tous liés)</p>
				<ul>
					<AccordionItem title="1" content="texte 1" selection={selection1} />
					<AccordionItem title="2" content="texte 2" selection={selection1} />
					<AccordionItem title="3" content="texte 3" selection={selection1} />
				</ul>
			</div>

			<div>
				<p>groupe (un seul ouvert)</p>
				<ul>
					<AccordionItem title="1" content="texte 1" selection={selection2} itemValue={1} />
					<AccordionItem title="2" content="texte 2" selection={selection2} itemValue={2} />
					<AccordionItem title="3" content="texte 3" selection={selection2} itemValue={3} />
				</ul>
			</div>
		</div>
	</AccordionItem>
</ul>

<ul>
	<AccordionItem>
		<p slot="title"  class="text-2xl font-bold">Accordion (plus simple qu'un groupe)</p>
		<div slot="content" class="grid grid-cols-1">
			<div>
				<p>par défaut</p>
				<Accordion />
			</div>

			<div>
				<p>avec contenu simple</p>
				<Accordion>
					<AccordionItem />
				</Accordion>
			</div>

			<div>
				<p>groupe (toujours un seul ouvert au max)</p>
				<Accordion>
					<AccordionItem title="1" content="texte 1" itemValue={1} />
					<AccordionItem title="2" content="texte 2" itemValue={2} />
					<AccordionItem title="3" content="texte 3" itemValue={3} />
				</Accordion>
			</div>

			<div>
				<p>groupe (deuxième élément ouvert au départ)</p>
				<Accordion selection={writable(2)}>
					<AccordionItem title="1" content="texte 1" itemValue={1} />
					<AccordionItem title="2" content="texte 2" itemValue={2} />
					<AccordionItem title="3" content="texte 3" itemValue={3} />
				</Accordion>
			</div>
		</div>
	</AccordionItem>
</ul>

<style>
	.grid > div {
		@apply p-4;
		@apply border-2;
		@apply border-black;
	}
</style>
