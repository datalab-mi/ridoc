<script>
	import { envJson } from '../components/user-data.store';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';

	const appVersion = 'APP_VERSION';
	let logo;
	$: {
		logo = $envJson && $envJson.logo_footer
			? 'user/' + $envJson.logo_footer
			: undefined;
	}
</script>

<footer use:cssProps={$userTheme.footer}>

	<span class=' float-left grid gap-0 grid-col '>
		<img src={logo} class='w-full'>
		<a href={$envJson.repository} class=" my-1 text-left text-black-400">Version <div class="text-black ">v{appVersion}</div> </a>
	</span>

	<!---liens dans le footer, il faudra dans chaque fichier env.json renseigner les coordonnées des différents réseaux sociaux et sites-->
	<div class=" mx-0 my-0 p-0 grid grid-cols-3 float-right">


		{#if $envJson.contacts}
		<div class='text-left ml-10 ' >
			<div class='font-bold  text-blue-400 mb-4' style='color:#5770BE'>Nous connaître</div>
			{#each $envJson.contacts as { href, name }}
				<a href={href} class='text-blue-800  underline'style='color:#000091'>{name}</a> <br>
			{/each}
			</div>
		{/if}

		{#if $envJson.commitments}
		<div class='text-left ml-10 ' >
			<div class='font-bold  text-blue-400 mb-4' style='color:#5770BE'>Nos engagements</div>
			{#each $envJson.commitments as { href, name }}
				<a href={href} class='text-blue-800  underline'style='color:#000091'>{name}</a> <br>
			{/each}
			</div>
		{/if}

		{#if $envJson.links}
		<div class='text-left ml-10 ' >
			<div class='font-bold  text-blue-400 mb-4' style='color:#5770BE'>Sites connexes</div>
			{#each $envJson.links as { href, name }}
				<a href={href} class='text-blue-800  underline'style='color:#000091'>{name}</a> <br>
			{/each}
			</div>
		{/if}

	</div>
</footer>

<style>
	footer {
		color: #aaa;
		font-family: Rubik, sans-serif;
		@apply text-base  py-4 pl-16 text-center w-full;
		background-color:white;

	}
</style>
