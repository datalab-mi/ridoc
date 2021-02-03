import { user as userStore } from './stores.js';
import { fromFetch } from 'rxjs/fetch'
import { from, of } from 'rxjs'
import { catchError, flatMap, switchMap } from 'rxjs/operators'

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
  console.log('upload :')
  console.log(file)
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
      console.log('error')
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
	
	const fetchRawRxjs = (url, requestInit = defaultInit) =>
		fromFetch(url, { headers: buildHeaders(), ...requestInit })
		.pipe(
			switchMap(res => {
				if (!res.ok) {
					console.log(`L'appel à "${url}" a échoué`)
					return of({ error: true, message: `L'appel à "${url}" a échoué: ${res.status}` });
				}
				console.debug(`L'appel à "${url}" a réussi`);
				return of(res);
			}),
			catchError(err => of({ error: true, message: err.message })),
		);
	
	const fetchJsonRxjs = (url, requestInit = defaultInit) =>
		fetchRawRxjs(url, requestInit).pipe(flatMap(res => from(res.json())));
	
	return {
		fetch: fetchRaw,
		fetchJson,
		rxjs: {
			fetch: fetchRawRxjs,
			fetchJson: fetchJsonRxjs
		}
	};
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

const format2ES = (item, query_list, index_name) => {
    query_list = query_list.flat(2)
		let query_dic = {index_name: index_name};
		let obj;
		let highlight_fields = item.inputs.filter(obj => obj.highlight).map(x => x.key)
		for (obj of query_list) {
			let clause = {}
			if (obj.value != "") {
				//highlight_fields.push(obj.fields)
				if (!(obj.bool in query_dic)) {
					query_dic[obj.bool] = []
				}
        console.log('***')
        console.log(JSON.stringify(obj.query))
        console.log(JSON.stringify(obj.query).replace('"\$value"', JSON.stringify(obj.value)))
				clause = JSON.parse(JSON.stringify(obj.query).replace('"\$value"', JSON.stringify(obj.value)))
				query_dic[obj.bool].push(clause)
			}
		}
		if (highlight_fields.length >0){
			query_dic["highlight"] = highlight_fields.flat()
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
  console.log(target)

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

export { index, upload, get, httpClient, synonym, files, format2ES, search, text_area_resize, reIndex };
