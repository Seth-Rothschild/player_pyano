<script>
	import { onMount } from 'svelte';
	import Playing from './Playing.svelte';
	import Playlist from './Playlist.svelte';
	import Search from './Search.svelte';

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

<div class="padding">
	<h3>Player Pyano</h3>
	<div class="small-divider" />
	{#if context}
		<Playing {context} />
		<Playlist {context} />
		<Search {context} {filteredSongs} />
	{:else}
		<a class="loader large center" />
	{/if}
</div>
