<script>
	export let context;
	async function playNow(file) {
		const res = fetch('api/play', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}

	async function removeFromPlaylist(file) {
		const res = fetch('api/playlist/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}
	async function duplicateInPlaylist(file) {
		const res = fetch('api/playlist/duplicate', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}
</script>

<div style="margin-top: 20px">
	{#if context.playlist.length > 0}
		<h5 class="primary-text">Playlist</h5>
		{#each context.playlist as file}
			<article class="border round padding small-margin">
				<div class="row">
					<i>audiotrack</i>
					<h7 style="font-size:1.2em">{file}</h7>
				</div>
				<div class="row">
					<button class="border margin" on:click={removeFromPlaylist(file)}>
						<i>remove</i>
					</button>
					<button class="border margin" on:click={duplicateInPlaylist(file)}>
						<i>file_copy</i>
						Duplicate
					</button>
					<button class="margin" on:click={playNow(file)}>
						<i>play_arrow</i>
						Play Now
					</button>
				</div>
			</article>
		{/each}
	{/if}
</div>
