<script>
export let cssClass; // specify type of baseitem, result or new, not used yet
export let _id;

</script>

<section class="item" id={_id}>

  <slot name="fields">
  </slot>

  <div class="flex justify-between">

    <slot name="button">
    </slot>

    <slot name="score">
    </slot>

  </div>

</section>

<style>
	.item {
		border: 1px solid #aaa;
		@apply rounded-sm;
		@apply p-2;
	}
	@screen sm {
		.item {
			@apply p-4;
		}
	}

</style>
