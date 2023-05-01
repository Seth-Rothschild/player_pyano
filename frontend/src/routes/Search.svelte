<script>
	export let context;
	export let filteredSongs;

	function filterSongs(e) {
		filteredSongs = context.files.filter((file) => {
			return file.toLowerCase().includes(e.target.value.toLowerCase());
		});
	}

	async function selectSong(file) {
		const res = fetch('api/play', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}
	async function addToPlaylist(file) {
		const res = fetch('api/playlist/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}

	async function tryPlay() {
		if (filteredSongs.length == 1) {
			const res = fetch('api/play', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ file: filteredSongs[0] })
			});
		}
	}
</script>

{#if context}
	<div style="max-width: 500px;">
		<h5 class="primary-text">Select a Song</h5>
		<div class="field border prefix">
			<i>search</i><input
				on:input={filterSongs}
				on:change={tryPlay}
				type="text"
				placeholder="Select a song"
			/>
		</div>
		{#each filteredSongs as file}
			<article class="border round padding small-margin">
				<b>{file}</b>
				<div class="row">
					<button class="circle margin" on:click={addToPlaylist(file)}>
						<i>add</i>
					</button>
					<button class="circle margin" on:click={selectSong(file)}>
						<i>play_arrow</i>
					</button>
				</div>
			</article>
		{/each}
	</div>
{/if}
