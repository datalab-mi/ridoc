<script>
	import { cssProps } from '../common/css-props.action';

	export let id;
	export let componentCssProps = undefined
</script>

<section {id} use:cssProps={componentCssProps} class="base-item rounded-sm p-2 sm:p-4">
	<slot name="fields" />

	<div class="flex justify-between">
		<slot name="buttons" />
		<slot name="score" />
	</div>
</section>

<style>
	.base-item {
		border: 1px solid #aaa;
	}
</style>
