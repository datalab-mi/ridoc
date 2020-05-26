async function upload(files, meta) {
  //for (var i = 0; i < files.length; i++) {
    //var file = files[i];
  const formData = new FormData();
  const filename = files[0].name

  formData.append('file', files[0]);
  meta.forEach(item => formData.append(item.key, item.value));

  const upload = await fetch(`http://localhost/api/common/${filename}`, {
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
    if (method == 'PUT') {
      statusOK = (s) => s.status
    } else if (method == 'DELETE') {
      statusOK = (s) => (s.ok || s.status == 404)
    }
    const index = await fetch(`http://localhost/api/common/${index_name}/_doc/${filename}`,
      {method: method});
		if (statusOK(index)) {
			return index.status
		} else {
      console.log('error')
			throw new Error('Oups');
		}
}

export { index, upload };
