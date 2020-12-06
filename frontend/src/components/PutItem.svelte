<script>

import { index_name, list_logger } from './stores.js';
import { index, upload } from './utils.js'

export let meta;
export let file;

let msg
const filename = file.name.replace(/\+/g, " ")

console.log(`Save ${filename}`)

upload(meta, file)
  .then(status => {
    if (status == 201) {
      msg = `${filename} crée`
    } else if (status == 200){
      msg = `${filename} modifié`
    } else if (status == 203){
      msg = `${filename} au mauvais format`
    } else {
      msg = `status ${status} inconnu`
    }
    list_logger.concat({level: "success", message: msg, ressource: filename, status: status, ressource: "putItem"})
  })
  .catch(err => {
    list_logger.concat({level: "error", message: err, ressource: "putItem"})
  })

index($index_name, filename, 'PUT')
  .then(status => {
    if (status == 201) {
      msg = `${filename} indexé`
    } else if (status == 200){
      msg = `${filename} modifié dans l'index`
    } else {
      msg = `status ${status} inconnu`
    }
    list_logger.concat({level: "success", message: msg, ressource: filename, status: status, ressource: "putItem"})
    })
  .catch(err => {
    list_logger.concat({level: "error", message: err, ressource: "putItem"})
  })

</script>
