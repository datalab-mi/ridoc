<script>
	import { userData } from '../common/user-data.store';

	const appVersion = 'APP_VERSION';
</script>

<footer>
	<span>
		&copy; {new Date().getFullYear()} DNUM - {($userData.index_name || '').toUpperCase()}.
		Powered by <a href="https://sapper.svelte.dev" target="_blank">Sapper</a>.
		Nous écrire <a href="mailto://{$userData.contact || ''}">✉️</a>.
		<a href={$userData.repository}>Dépot : v{appVersion}</a>
	</span>
</footer>

<style>
	footer {
		color: #aaa;
		font-family: Rubik, sans-serif;
		@apply text-base my-4 mx-auto py-4 px-8 text-center w-full;
	}
</style>