import { displayLogin } from './stores.js';

async function upload(meta, file) {
  //for (var i = 0; i < files.length; i++) {
    //var file = files[i];
  const formData = new FormData();
  console.log('upload :')
  console.log(file)
  const filename = file.name
  formData.append('file', file);

  meta.forEach(item => formData.append(item.key,
    (item.value instanceof Array) ?  JSON.stringify(item.value) : item.value));

  const upload = await fetch(`/api/admin/${filename}`, {
      method: 'PUT',
      body: formData
      });

  if (upload.ok) {
    return upload.status
  } else if (upload.status===401)  {
    displayLogin.set(true)
    throw new Error('Rôle admin nécessaire');
  } else {
    console.log('error')
    throw new Error('Oups');
  }
}

async function index(index_name, filename, method) {
    let statusOK;
    // handle status of the http request
    if (method == 'PUT') {
      statusOK = (s) => s.status
    } else if (method == 'DELETE') {
      statusOK = (s) => (s.ok || s.status == 404)
    }
    // Make the  http request
    const index = await fetch(`/api/admin/${index_name}/_doc/${filename}`,
      {method: method});
		if (statusOK(index)) {
			return index.status
    } else if (res.status===401)  {
      displayLogin.set(true)
      throw new Error('Rôle admin nécessaire');
    } else {
      console.log('error')
			throw new Error('Oups');
		}
}

async function get(url) {
	const res = await fetch(url, {cache: 'no-cache'})
	const data = await res.json();
	if (res.ok)  {
		return data
	} else {
		console.log('error')
		throw new Error('Oups');
	}
}


	async function files(method, baseDir,file = {'name': ""}) {
		let res;
    const filename = file.name//file !== "undefined" ? file.name : ""
    const url = filename === "" ? baseDir :  `${baseDir}/${filename}`

		if (method == 'GET') {
			res = await fetch(`/api/common/files/${url}`,
					{method: 'GET'})
		} else if (method == 'PUT') {
      const formData = new FormData()
      formData.append('file', file)
			res = await fetch(`/api/admin/files/${url}`, {
					method: 'PUT', body: formData})
		} else if (method == 'DELETE') {
			res = await fetch(`/api/admin/files/${url}`, {
					method: 'DELETE'})
	}
		if (res.ok) {
			return res
    } else if (res.status===404)  {
      throw new Error('Ressource introuvable');
    } else if (res.status===401)  {
      displayLogin.set(true)
      throw new Error('Rôle admin nécessaire');
		} else {
			throw new Error('Erreur inconnue');
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
	const res = await fetch("/api/common/search",{
											method: "POST",
											body: JSON.stringify(body)
												 });

	const result = await res.json();
	if (res.ok) {
		return result
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
    res = await fetch(`/api/common/synonym?filename=${filename}`,
        {method: 'GET'});
  } else if (method === 'PUT' || method === 'DELETE') {
    res = await fetch(`/api/admin/synonym/${key}?filename=${filename}`, {
        method: method,
        body: JSON.stringify(row)});
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

export { index, upload, get, synonym, files, format2ES, search, text_area_resize };
