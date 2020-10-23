<script>
	export let segment;
	let logo = "/api/common/logo"
</script>

<style>
	nav {
		border-bottom: 1px solid rgba(255,62,0,0.1);
		font-weight: 300;
		padding: 0 1em;
		display: flex;
		justify-content: space-between;
	}

	ul {
		margin: 0;
		padding: 0;
	}

	/* clearfix */
	ul::after {
		content: '';
		display: block;
		clear: both;
	}

	li {
		display: block;
		float: left;
	}

	[aria-current] {
		position: relative;
		display: inline-block;
	}

	[aria-current]::after {
		position: absolute;
		content: '';
		width: calc(100% - 1em);
		height: 2px;
		background-color: rgb(255,62,0);
		display: block;
		bottom: -1px;
	}

	a {
		text-decoration: none;
		padding: 1em 0.5em;
		display: block;
	}

	.logo {
		position: relative;
		top: .1rem;
		left: -1rem;
		width: 4.2rem;
		background: 0 50% no-repeat;
		background-size: auto 100%;
		text-indent: -9999px;
		/* z-index: 11; */
	}

</style>

<nav>
	<ul>
		<li><a aria-current='{segment === undefined ? "page" : undefined}' href='.'>recherche</a></li>
		<li><a aria-current='{segment === "glossary" ? "page" : undefined}' href='glossary'>glossaire</a></li>
		<li><a aria-current='{segment === "expression" ? "page" : undefined}' href='expression'>expression</a></li>
		<li><a aria-current='{segment === "admin" ? "page" : undefined}' href='admin'>admin</a></li>
	</ul>
	<a rel="prefetch" href="." class="logo" style="background-image: url({logo})"></a>

</nav>
