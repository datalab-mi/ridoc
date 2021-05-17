import { user as userStore } from './stores.js';

export const USER_API = '/api/user';

const currentUser = { token: undefined };
userStore.subscribe(value => currentUser.token = value.jwToken);

function buildHeaders() {
	return !!currentUser.token ?
		new Headers({ 'Authorization': `Bearer ${currentUser.token}` }) :
		new Headers();
}

async function upload(meta, file, method='PUT') {
  const filename = file.name
  const body = new FormData();

  if (method === "PUT") {
    body.append('file', file);
    meta.forEach(item => body.append(item.key,
      (item.value instanceof Array) ?  JSON.stringify(item.value) : item.value));
  }
  //for (var i = 0; i < files.length; i++) {
    //var file = files[i];

  const upload = await fetch(`/api/admin/${filename}`, {
      method: method,
      body: body,
      headers: buildHeaders()
      });

  if (upload.ok) {
    return upload.status
  } else if (upload.status===401)  {
    throw new Error('Rôle admin nécessaire');
  } else {
    throw new Error(`Status ${upload.status} inconnu`);
  }
}

async function index(index_name, filename, method) {
    let statusOK;
    // handle status of the http request
    if (method == 'PUT') {
      statusOK = (s) => s.ok
    } else if (method == 'DELETE') {
      statusOK = (s) => (s.ok || s.status == 404)
    }
    // Make the  http request
    const index = await fetch(`/api/admin/${index_name}/_doc/${filename}`,{
      method: method,
      headers: buildHeaders()
    });
		if (statusOK(index)) {
			return index.status
    } else if (index.status === 401)  {
      throw new Error('Rôle admin nécessaire pour indexer');
    } else {
			throw new Error('Oups');
		}
}

async function get(url) {
	const res = await fetch(url, {
      cache: 'no-cache',
      headers: buildHeaders()
    })
	if (!res.ok) {
		console.log(`L'appel à "${url}" a échoué`)
		throw new Error(`L'appel à "${url}" a échoué: ${res.status}`);
	}
	console.debug(`L'appel à "${url}" a réussi`)
	return await res.json();
}

function httpClient() {
	const defaultInit = { cache: 'no-cache' };

	const fetchRaw = async (url, requestInit = defaultInit) => {
		const res = await fetch(url, { headers: buildHeaders(), ...requestInit })
		if (!res.ok) {
			console.log(`L'appel à "${url}" a échoué`)
			throw new Error(`L'appel à "${url}" a échoué: ${res.status}`);
		}
		console.debug(`L'appel à "${url}" a réussi`);
		return res;
	}

	const fetchJson = async (url, requestInit = defaultInit) => {
		const res = await fetchRaw(url, requestInit);
		return await res.json();
	}

	/**
	 * Extrait le nom de fichier des entêtes de la réponse
	 * @param  response  Response obtenue par fetch
	 * @return nom de fichier ou null
	 */
	const extractFilename = response => {
		let filename = null;
		const disposition = response.headers.get('Content-Disposition');
		if (disposition && disposition.indexOf('attachment') !== -1) {
			const matches = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
			if (matches && matches[1]) {
			  filename = matches[1].replace(/['"]/g, '');
			}
		}
		return filename;
	}

	/**
	 * Provoque le téléchargement d'un fichier déjà récupéré.
	 * @param  blob      blob déjà récupéré
	 * @param  filename  nom du fichier à télécharger
	 */
	const downloadFile = (blob, filename) => {

		// indiquer le type MIME explicitement pour éviter les surprises avec certains navigateurs
		const newBlob = new Blob([blob], { type: blob.type || 'application/octet-stream' })

		// IE : il faut utiliser msSaveOrOpenBlob, on ne peut pas utiliser un objet blob comme cible de lien
		if (window.navigator && window.navigator.msSaveOrOpenBlob) {
			window.navigator.msSaveOrOpenBlob(newBlob);
			return;
		}

		// ajout d'un lien qui pointe vers un ObjectURL contenant le blob
		const data = window.URL.createObjectURL(newBlob);
		const link = document.createElement('a');
		link.href = data;
		link.download = filename || 'file_' + Date.now();
		link.click();

		// délai car Firefox en a besoin
		setTimeout(() => window.URL.revokeObjectURL(data), 100);
	}

	/**
	 * Récupère un blob, puis provoque le téléchargement par le navigateur.
	 * @see API fetch
	 * @see Response.blob()
	 */
	const fetchBlob = async (url, requestInit = defaultInit) => {
		const res = await fetchRaw(url, requestInit);
		const blob = await res.blob();
		downloadFile(blob, extractFilename(res));
	}

	return { fetch: fetchRaw, fetchJson, fetchBlob };
}

	async function files(method, baseDir,file = {'name': ""}) {
		let res;
    const filename = file.name//file !== "undefined" ? file.name : ""
    const url = filename === "" ? baseDir :  `${baseDir}/${filename}`

		if (method == 'GET') {
			res = await fetch(`${USER_API}/files/${url}`, {
        method: 'GET',
        headers: buildHeaders()
      })
		} else if (method == 'PUT') {
      const formData = new FormData()
      formData.append('file', file)
			res = await fetch(`/api/admin/files/${url}`, {
					method: 'PUT',
          body: formData,
          headers: buildHeaders()
      })
		} else if (method == 'DELETE') {
			res = await fetch(`/api/admin/files/${url}`, {
					method: 'DELETE',
          headers: buildHeaders()
      })
	}
		if (res.ok) {
			return res
    } else if (res.status===404)  {
      throw new Error('Ressource introuvable');
    } else if (res.status===401)  {
      throw new Error('Rôle admin nécessaire pour sauver');
		} else {
			throw new Error('Erreur inconnue');
		}
	}

  async function reIndex(index_name) {
  		const res = await fetch(`/api/admin/${index_name}/reindex`,{
        headers: buildHeaders()
      });
  		if (res.ok) {
        const result = await res.json();
  			return result;
  		} else if (res.status == 401) {
  			throw new Error("Rôle admin nécessaire");
  		} else {
        const text = await res.text();
  			throw new Error(text);
  		}
  	}

const flatten = (array, depth) => {
  // If no depth is specified, default to 1
  if (depth === undefined) {
    depth = 1;
  }
  // Recursively reduce sub-arrays to the specified depth
  const flat = (arr, depth) => {
    // If depth is 0, return the array as-is
    if (depth < 1) {
      return arr.slice();
    }
    // Otherwise, concatenate into the parent array
    return arr.reduce(function (acc, val) {
      return acc.concat(Array.isArray(val) ? flat(val, depth - 1) : val);
    }, []);
  };
  return flat(array, depth);
}

const format2ES = (item, query_list, index_name) => {
    //query_list = query_list.flat(2)
		let query_dic = {index_name: index_name};
		let obj;
		let highlight_fields = item && item.inputs
			? item.inputs.filter(obj => obj.highlight).map(x => x.key)
			: [];
		for (obj of query_list) {
			let clause = {}
			if (obj.value != "") {
				//highlight_fields.push(obj.fields)
				if (!(obj.bool in query_dic)) {
					query_dic[obj.bool] = []
				}
				clause = JSON.parse(JSON.stringify(obj.query).replace('"\$value"', JSON.stringify(obj.value)))
				query_dic[obj.bool].push(clause)
			}
		}
		if (highlight_fields.length >0){
			query_dic["highlight"] = flatten(highlight_fields, 1)
		}
		return query_dic
  }

async function search(body) {
	const res = await fetch(`${USER_API}/search`, {
											method: "POST",
											body: JSON.stringify(body),
                      headers: buildHeaders(),
                      cache: 'no-cache'
												 });

	if (res.ok) {
    const result = await res.json();
		return result
  } else if (res.status===401)  {
    throw new Error('Rôle insuffisant pour rechercher');
	} else {
		throw new Error('Oups');
	}
}


function resize({ target }) {
  target.style.height = "1px";
	target.style.height = (+target.scrollHeight)+"px";
}

function text_area_resize(el) {
	resize({ target: el });
	el.style.overflow = 'auto';
	el.addEventListener('input', resize);

	return {
		destroy: () => el.removeEventListener('input', resize)
	}
}

async function synonym(method, row, filename,key=0) {
  let res;
  if (method === 'GET') {
    res = await fetch(`${USER_API}/synonym?filename=${filename}`,
        {method: 'GET', headers: buildHeaders()});
  } else if (method === 'PUT' || method === 'DELETE') {
    res = await fetch(`/api/admin/synonym/${key}?filename=${filename}`, {
        method: method,
        body: JSON.stringify(row),
        headers: buildHeaders()
    })
  }
  let data = await res.json();
  if (res.ok)  {
    return data
  } else if (res.status===401)  {
    //displayLogin.set(true)
    throw new Error('Rôle admin nécessaire')
  } else {
    throw new Error('Oups');
  }
}

export { index, upload, get, httpClient, synonym, files, flatten, format2ES, search, text_area_resize, reIndex };
