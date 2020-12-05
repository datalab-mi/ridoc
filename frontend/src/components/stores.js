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
export const displayLogin = writable(false)
export const jwToken = writable(null)

// logger
export const list_logger = writable([{level: "error",message: "erreur grave", ressource: "authentification", status:401},
        {level: "info",message: "document telechargé", ressource: "upload", status:200}])
