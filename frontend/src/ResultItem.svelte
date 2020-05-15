<script>
	export let _id;
	export let _source;
	export let highlight;
	$: url = `/pdfjs-2.3.200-dist/web/viewer.html?file=/user/pdf/${_id.replace(/\+/g, " ")}`
</script>

<section class='result-item'>


<a href="{url}">
<h2>{_source.title}</h2>
</a>

<p>{@html highlight.content}</p>
<p>Auteurs : {_source.author}</p>
<p>Date : {_source.date}</p>
</section>


<style>
	.result-item {
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0,0,255,1);
		padding: 1em;
		margin: 0 0 1em 0;
	}
	mark {
  background-color: blue;
  color: black;
}

a {
display: block;
margin: 0 0 1em 0;
}

</style>
