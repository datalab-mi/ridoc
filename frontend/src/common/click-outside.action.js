/**
 * Envoie un événement 'clickoutside' en cas de clic à l'extérieur de l'élément.
 * detail: { originalEvent: <événement de clic> }
*/
export function clickOutside(node) {

	const handleClick = event => {
		if (node && !node.contains(event.target) && !event.defaultPrevented) {
			node.dispatchEvent(new CustomEvent('clickoutside', { detail: { originalEvent: event } }));
		}
	}

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	}

}