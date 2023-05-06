<script>
	import { onMount } from 'svelte';
	import NowPlaying from './NowPlaying.svelte';
	import Playlist from './Playlist.svelte';
	import Search from './Search.svelte';
	import Upload from './Upload.svelte';
	import Admin from './Admin.svelte';

	let context;
	let filteredSongs = [];

	async function getContext() {
		const res = await fetch('api/context');
		const data = await res.json();
		return data;
	}

	function updateContext() {
		setInterval(async function () {
			context = await getContext();
		}, 1000);
	}

	onMount(async () => {
		context = await getContext();
		filteredSongs = context.files;
		updateContext();
	});
</script>

<div class="padding" style="max-width: 500px; width:150%">
	<h3>Player Pyano</h3>
	<div class="small-divider" />
	{#if context}
		<NowPlaying {context} />
		<Playlist {context} />
		<Search {context} {filteredSongs} />
		<Upload />
		<Admin />
	{:else}
		<a class="loader large center" />
	{/if}
</div>
