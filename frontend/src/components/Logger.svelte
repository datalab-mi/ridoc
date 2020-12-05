<script>
	import { list_logger  } from './stores.js';
  import { fade, slide } from 'svelte/transition';

  $:{ console.log($list_logger)}

</script>

<div class="logger">
  {#each $list_logger as log}
    <div class={log.level} in:slide|local out:slide|local>
    {@html log.message}
    </div>
  {/each}
</div>
<style>

div {
  padding: 0.5em 0;
  border-top: 1px solid #eee;
}

.logger {
display: block;
position: fixed;
bottom: 5em;
left: 15px;
border: 3px solid #f1f1f1;
z-index: 9;
}

.error {
  background-color: red;
  color: white
}
.info {
  background-color: blue;
  color: white
}

</style>
