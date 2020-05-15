<script>
	export let title;
	export let body;
	export let authors;
</script>

<section class='result-item'>

<h2>{title}</h2>
<p>{body}</p>
<p>Auteurs : {authors}</p>

</section>


<style>
	.result-item {
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0,0,255,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
</style>
