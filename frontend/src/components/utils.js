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
		} else {
      console.log('error')
			throw new Error('Oups');
		}
}

async function config(filename) {
	const res = await fetch(`/api/common/files/${filename}`);
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
		if (res.ok)  {
			return res
    } else if (res.status===404)  {
      throw new Error('Ressource introuvable');
		} else {
			throw new Error('Erreur inconnue');
		}
	}

export { index, upload, config, files };
