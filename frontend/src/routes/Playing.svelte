<script>
	export let context;

	async function stopSong() {
		const res = await fetch('api/stop', {
			method: 'POST'
		});
	}

	async function pauseSong() {
		const res = await fetch('api/pause', {
			method: 'POST'
		});
	}

	async function adjustVolume(e) {
		const res = await fetch('api/volume', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ volume: e.target.value })
		});
	}
</script>

{#if context}
	<div style="max-width: 500px;">
		<h5 class="primary-text">Song Controls</h5>
		{#if context.selected_file}
			<div class="padding">
				<h6>Now Playing</h6>

				<span><b>{context.selected_file}</b></span><br />
				<span>Length: {context.song_length.toFixed(0)} seconds</span><br />
				{#if context.song_length}
					<div class="row">
						<div
							class="secondary no-margin no-padding"
							style="width: {context.percent_done * 0.8}%"
						>
							Progress
						</div>
						<div class="max no-margin no-padding" />
						<span class="no-margin no-padding" style="width: 13%"
							>| {context.percent_done.toFixed(2)}%</span
						>
					</div>
				{/if}
			</div>
			<nav class="margin no-space">
				<button class="border left-round">
					<i>skip_previous</i>
					<span>Restart</span>
				</button>
				{#if context.paused}
					<button on:click={pauseSong} class="border no-round">
						<i>play_arrow</i>
						<span>Play</span>
					</button>
				{:else}
					<button on:click={pauseSong} class="border no-round">
						<i>pause</i>
						<span>Pause</span>
					</button>
				{/if}
				<button on:click={stopSong} class="border right-round">
					<i>stop</i>
					<span>Stop</span>
				</button>
			</nav>
			<div class="row margin">
				<span>Volume</span>
				<label class="slider">
					<input on:change={adjustVolume} type="range" value={context.velocity} min="0" max="100" />
					<span />
				</label>
				<span>{context.velocity.toFixed(0)}%</span>
			</div>
		{:else}
			<h6>No Song Selected</h6>
		{/if}
	</div>
{/if}
