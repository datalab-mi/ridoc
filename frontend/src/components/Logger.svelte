<script>
	import { list_logger  } from './stores.js';
  import { fade, slide } from 'svelte/transition';

  function remove(msg) {
    // remove all messages == msg
		list_logger.filter(msg, 'message');
	}

  /// for debug
  const handleAdd = (msg) => {

		list_logger.concat({level: "info",message: msg + "", ressource: "upload", status:200})
	}
	const handleDelete = () => {
		list_logger.delete()
	}

</script>

<div class="logger">
  {#each $list_logger as log}
    <div class={log.level} in:slide|local out:fade|local>
      {@html log.message}
      <button  on:click="{() => remove(log.message)}"></button>
    </div>
  {/each}
</div>
<!--
<input
  placeholder="what needs to be done?"
  on:keydown={e => e.key === 'Enter' && handleAdd(e.target.value)}
>
<button  on:click={handleDelete}>Delete</button>
 //-->
<style>


.logger {
  display: grid;
  grid-gap: 0.1rem;
  max-width: 60rem;
  margin: 0 auto;
  position: fixed;
  bottom: 2rem;
  left: 15px;
  z-index: 9;
}

.error {
  background-color: red;
  color: white;
  padding: 0.5em 0;
  border-top: 1px solid #eee;
  width:20rem;
  position: relative;
  line-height: 1.2;
  padding: 0.5em 2.5em 0.5em 2em;
  margin: 0 0 0.5em 0;
  border-radius: 5px;
}
.info {
  background-color: blue;
  color: white;
  padding: 0.5em 0;
  border-top: 1px solid #eee;
  width:20rem;
  position: relative;
  line-height: 1.2;
  padding: 0.5em 2.5em 0.5em 2em;
  margin: 0 0 0.5em 0;
  border-radius: 5px;
}
.success {
  background-color: green;
  color: white;
  padding: 0.5em 0;
  border-top: 1px solid #eee;
  width:20rem;
  position: relative;
  line-height: 1.2;
  padding: 0.5em 2.5em 0.5em 2em;
  margin: 0 0 0.5em 0;
  border-radius: 5px;
}
button {
  position:absolute;
  top: 0;
  right: 0.1em;
  width: 2em;
  height: 100%;
  background: no-repeat 50% 50% url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23676778' d='M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M17,7H14.5L13.5,6H10.5L9.5,7H7V9H17V7M9,18H15A1,1 0 0,0 16,17V10H8V17A1,1 0 0,0 9,18Z'%3E%3C/path%3E%3C/svg%3E");
  background-size: 1.4em 1.4em;
  border: none;
  opacity: 0;
  transition: opacity 0.2s;
  text-indent: -9999px;
  cursor: pointer;
}

div:hover button {
  opacity: 1;
}

</style>
