<script>
	import { userData } from '../components/user-data.store';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';

	const appVersion = 'APP_VERSION';
</script>

<footer use:cssProps={$userTheme.footer}>
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
		@apply text-base  py-8 px-16 text-center w-full;
	}
</style>
