<script>
	export let context;
	async function removeFromPlaylist(file) {
		const res = fetch('api/playlist/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file: file })
		});
	}
</script>

{#if context}
	<div style="max-width: 500px;">
		{#if context.playlist.length > 0}
			<h5 class="primary-text">Playlist</h5>
			{#each context.playlist as file}
				<article class="border round padding small-margin">
					<b>{file}</b>
					<div class="row">
						<button class="circle margin" on:click={removeFromPlaylist(file)}>
							<i>remove</i>
						</button>
					</div>
				</article>
			{/each}
		{/if}
	</div>
{/if}
