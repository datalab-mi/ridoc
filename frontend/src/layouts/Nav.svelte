<script>
	import { userData } from '../common/user-data.store';
	import { user } from '../components/stores';
	import { createOpenCloseStore } from '../common/store.utils';

	export let segment;
	
	/** store créé par createOpenCloseStore */
	export let login;

	const nav = createOpenCloseStore();
	
	const allLinks = [
		{ text: 'recherche',  href: 'search',     role: 'user'  },
		{ text: 'glossaire',  href: 'glossary',   role: 'admin' },
		{ text: 'expression', href: 'expression', role: 'admin' },
		{ text: 'admin',      href: 'admin',      role: 'admin' },
		{ text: 'tests',      href: 'tests',      role: 'admin' }
	];
	
	let logo;
	let links = [];

	$: {
		logo = $userData && $userData.logo
			? 'user/' + $userData.logo
			: undefined;
		links = allLinks.filter(link => $user.resources.includes(link.href) || link.role === $user.role);
	}
</script>

<style>
	[aria-current] {
		@apply relative;
	}

	[aria-current]::after {
		content: '';
		height: 3px;
		background-color: rgb(255,62,0);
		@apply block;
		@apply absolute;
		@apply bottom-0;
		@apply left-0;
		@apply w-full;
	}
	
	.navlink {
		@apply px-3;
		@apply py-2;
		@apply rounded-md;
		@apply text-base;
		@apply font-normal;
	}
</style>

<nav>
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex mt-2">
			<div class:hidden={!logo} class="flex-shrink-0">
				<a href="."><img class="block h-8 sm:h-20 w-8 sm:w-20" src={logo} alt="logo"></a>
			</div>
			<div class="flex-1">
				<div class="flex flex-col">
					<div class="hidden sm:flex ml-2 font-bold text-2xl">Recherche dans les rapports IGA</div>
					<div class="flex items-center justify-between h-10">
						<div class="flex items-center">
							{#if links.length}
								<div class="hidden md:block">
									<div class="ml-2 flex items-baseline space-x-1 content-center">
										{#each links as link}
											{#if link.href === segment}
												<a href={link.href} class="navlink hover:bg-gray-200" aria-current="page">{link.text}</a>
											{:else}
												<a href={link.href} class="navlink hover:bg-gray-200">{link.text}</a>
											{/if}
										{/each}
									</div>
								</div>
								<div class="ml-2 flex md:hidden">
									<!-- Mobile menu button -->
									<button on:click={nav.toggle} class="inline-flex items-center justify-center p-2 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-expanded={$nav || undefined}>
										<span class="sr-only">Open main menu</span>
										<!-- Icon when menu is closed. -->
										<svg class:block={!$nav} class:hidden={$nav} class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
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
						<div class="block">
							<div class="ml-2 flex items-center md:ml-6">
								<!-- Profile dropdown -->
								<div class="ml-3 relative">
									<div>
										<button on:click={login.toggle} class="max-w-xs rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" id="user-menu" aria-haspopup="true">
											<svg class="h-8 w-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5 5a5 5 0 0 1 10 0v2A5 5 0 0 1 5 7V5zM0 16.68A19.9 19.9 0 0 1 10 14c3.64 0 7.06.97 10 2.68V20H0v-3.32z"/></svg>
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
					<a href={link.href} class="block navlink hover:bg-gray-200">{link.text}</a>
				{/if}
			{/each}
			</div>
		</div>
	{/if}
</nav>

<!-- Hidden links to redirect Client side rendering app  -->
<div class="hidden">
	{#each links as link}
		<a href={link.href} hidden>{link.text}</a>
	{/each}
</div>
