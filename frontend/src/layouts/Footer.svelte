<script>
	import { envJson } from '../components/user-data.store';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';

	const appVersion = 'APP_VERSION';
	let logo;
	$: {
		logo = $envJson && $envJson.logo
			? 'user/' + $envJson.logo
			: undefined;
	}
</script>

<footer use:cssProps={$userTheme.footer}>

	<span class='float-left grid gap-0 grid-cols-2 max-w-sm '>
		<img src={logo} class=''>
		<div class="font-bold text-2xl text-left text-black">{$envJson.navTitle}</div>
		<a href={$envJson.repository} class=" my-1 text-left text-black ">Version : v{appVersion}</a>
		
	</span>
	
	
	<!---liens dans le footer, il faudra dans chaque fichier env.json renseigner les coordonnées des différents réseaux sociaux et sites-->
	<div class=" mx-0 my-0 p-0 grid grid-cols-3 float-right">

		<div class='text-left ml-10' >
			<div class='font-bold text-blue-400 mb-4' >Nous connaître</div>
			<a href={$envJson.plan} class='text-blue-700 font-bold underline'>Plan du site </a> <br>
			<a href={$envJson.contact} class='text-blue-700 font-bold underline'>Nous contacter</a><br>
			<a href={$envJson.horaires} class='text-blue-700 font-bold underline'>Horaires et plan d'accès</a><br>
		</div>

		<div class='text-left ml-10 ' >
			<div class='font-bold text-blue-400 mb-4' >Nos engagements</div>
			<a href={$envJson.engagement} class='text-blue-700 font-bold underline'>Engagement et qualité </a> <br>
			<a href={$envJson.accessibilité} class='text-blue-700 font-bold underline'>Accessibilité</a><br>
			<a href={$envJson.donnees} class='text-blue-700 font-bold underline'>Données personnelles et sécurité</a><br>
			<a href={$envJson.mentions} class='text-blue-700 font-bold underline'>Mentions légales</a><br>
		</div>

		<div class='text-left ml-10 ' >
			<div class='font-bold  text-blue-400 mb-4' >Sites connexes</div>
			<a href={$envJson.servicepublic} class='text-blue-700 font-bold underline'>service-public.fr </a> <br>
			<a href={$envJson.datagouv} class='text-blue-700 font-bold underline'>data.gouv.fr</a><br>
			<a href={$envJson.legifrance} class='text-blue-700 font-bold underline'>legifrance.gouv.fr</a><br>
			<a href={$envJson.gouvernement} class='text-blue-700 font-bold underline'>gouvernement.fr</a><br>
		</div>
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
