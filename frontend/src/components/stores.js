import { readable, writable } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const itemConfig = writable({})
export const searchList = writable([[]])
export const promiseSearch = writable(new Promise(()=>{}))

export const suggestEntry = writable([]);

export const isReindex = writable(false)

export const list_synonym = writable([])
export const list_files = writable([])

//index_name, dstDir, pjDir are replaced in rollup.config.js
export const index_name = writable('INDEX_NAME')
export const dstDir = "DST_DIR"
export const pjDir = "PJ_DIR"

// authentification
export const user = writable({display: false, role:"common", jwToken:null})

// logger
const inital_logger_list = [{level: "error",message: "erreur grave", ressource: "authentification", status:401},
        {level: "info",message: "document telechargé", ressource: "upload", status:200}]

// custom store for the logger, every 10 seconds lost first element (the oldest)
function createLogger() {
	const { subscribe, set, update } = writable([], () => {
	console.log('got a subscriber');
	const interval = setInterval(() => {
		update(n => n.slice(1, n.length))
	}, 10000);	return () => console.log('no more subscribers');
});

	return {
		subscribe,
		concat: (x) => update(n => n.concat(x)),
		filter: (msg, key) => update(n => n.filter(t => t[key] !== msg)),
    delete: () => n.slice(1, n.length),
		reset: () => set(inital_logger_list)
	};
}

export const list_logger = createLogger();
