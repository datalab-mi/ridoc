<script>
	import { envJson } from '../components/user-data.store';
	import { user } from '../components/stores';
	import { createOpenCloseStore } from '../components/store.utils';
	import { cssProps } from '../components/css-props.action';
	import { userTheme } from '../components/theme.store';
	import { displayLogin } from '../components/stores.js';

	export let segment;

	const nav = createOpenCloseStore();

	function authClicked() {
		$displayLogin = !$displayLogin
	}
	const allLinks = [
		{ text: 'recherche',  href: 'search',     role: 'user'  },
		{ text: 'glossaire',  href: 'glossary',   role: 'admin' },
		{ text: 'expression', href: 'expression', role: 'admin' },
		{ text: 'admin',      href: 'admin',      role: 'admin' },
		//{ text: 'tests',      href: 'tests',      role: 'admin' }
	];

	let logo;
	let links = [];

	$: {
		logo = $envJson && $envJson.logo
			? 'user/' + $envJson.logo
			: undefined;
		links = allLinks.filter(link => $user.resources.includes(link.href) || link.role === $user.role);
	}
</script>

<style>
	[aria-current] {
		position: relative !important;
	}

	[aria-current]::after {
		content: '' !important;
		height: 3px !important;
		background-color:var(--primary) !important;
		display: block !important;
		position:  absolute !important;
		width: 100%;
		bottom: 0px;
		left: 0px;
		font-weight: 700 !important;
		
	}

	.navlink {
		padding-left: 0.75em;
		padding-right: 0.75em;
		padding-top: 0.5em;
		padding-bottom: 0.5em;
		border-radius: 0.25rem;
		font-weight: 400 !important;
		box-shadow: none;
	}

	.connect{
		background-color:var(--primary)
	}
	.artifact {
	display: none;
}
</style>

<nav use:cssProps={$userTheme.nav} class="bg-white border-2 border-gray">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex ">
			<div class:hidden={!logo} class="flex-shrink-0">
				<a href="."><img class="block h-8 sm:h-20 w-8 sm:w-20 m-1" src={logo} alt="logo"></a>
			</div>
			<div class="flex-1 align-center">
				<div class="flex flex-row my-6">
					<div class=" align-center mx-3 font-bold text-2xl ">{$envJson.navTitle}</div>
					<div class="flex items-center justify-between h-10 ">
						<div class="flex items-center">
							{#if links.length}
								<div class="hidden md:block ">
									<div class="ml-5 flex items-baseline space-x-1 content-center">
										{#each links as link}
											{#if link.href === segment}
												<a href={link.href} class="navlink hover:bg-gray-200" aria-current="page">{link.text}</a>
											{:else}
												<a href={link.href} class="navlink hover:bg-gray-200">{link.text}</a>
											{/if}
										{/each}
									</div>
								</div>
								<div class="ml-2 md:hidden ">
									<!-- Mobile menu button -->
									<button on:click={nav.toggle} class=" p-2 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-expanded={$nav || undefined}>
										<span class="sr-only">Open main menu</span>
										<!-- Icon when menu is closed. -->
										<svg class:block={!$nav} class:hidden={$nav} class="h-6 w-6 " xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
										</svg>
										<!-- Icon when menu is open. -->
										<svg class:block={$nav} class:hidden={!$nav} class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
										</svg>
									</button>
								</div>
							{/if}
						</div>
						<div class="absolute right-0">
							<div class="ml-2 ">
								<!-- Profile dropdown -->
								<div class="connect mr-4  p-2 rounded-lg">
									<div>
										<button on:click={authClicked} class="fr-button fr-fi-account-line text-white" id="user-menu" aria-haspopup="true">
										Se connecter
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	{#if links.length}
		<!--
			Mobile menu, toggle classes based on menu state.

			Menu open: "block", Menu closed: "hidden"
		-->
		<div class:block={$nav} class:hidden={!$nav} class="md:hidden">
			<div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
			{#each links as link}
				{#if link.href === segment}
					<a href={link.href} class="block navlink hover:bg-gray-200" aria-current="page">{link.text}</a>
				{:else}
					<a href={link.href} on:click={nav.close} class="block navlink hover:bg-gray-200">{link.text}</a>
				{/if}
			{/each}
			</div>
		</div>
	{/if}
</nav>

<!-- Hidden links to redirect Client side rendering app  -->
{#each allLinks as link}
	<a class="artifacts" href={link.href} hidden></a>
{/each}
<a class="artifacts" hidden href="ResultPage"></a>
<a class="artifacts" hidden href="ViewerJS"></a>
