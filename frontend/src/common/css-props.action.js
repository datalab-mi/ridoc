/**
 * Ajoute des propriétés CSS à l'élément ou retire des propriétés CSS de l'élément.
 * Pour retirer une propriété, l'objet en paramètre doit contenir le nom de cette propriété
 * mais sans valeur associée.
 * 
 * @param node   élément
 * @param props  propriétés CSS
 */
export function cssProps(node, props) {

	const updateProperties = (_props) => {
		if (_props) {
			for (const prop of Object.keys(_props)) {
				const value = _props[prop];
				if (value) {
					node.style.setProperty(prop, value);
				} else {
					node.style.removeProperty(prop);
				}
			}
		}
	}

	updateProperties(props);

	return {
		update: (newProps) => updateProperties(newProps)
	}

}