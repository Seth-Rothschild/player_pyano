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

	function adjustVolume(value) {
		return async () => {
			const newVolume = context.velocity + value;
			if (newVolume < 0 || newVolume > 100) {
				return;
			}
			const res = await fetch('api/volume', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ volume: newVolume })
			});
		};
	}
</script>

<div style="max-width: 500px;">
	<h5 class="primary-text">Song Controls</h5>
	<nav>
		<button on:click={adjustVolume(-5)} class="circle transparent"><i>remove</i></button>
		<label class="slider">
			<input
				on:change={(e) => {
					adjustVolume(e.target.value - context.velocity)();
				}}
				type="range"
				value={context.velocity}
				min="0"
				max="100"
			/>
			<span style="width:{context.velocity}%" />
		</label>
		<button on:click={adjustVolume(5)} class="circle transparent"><i>add</i></button>
	</nav>

	{#if context.selected_file}
		<article class="border">
			<h6>Now Playing</h6>
			<span><b>{context.selected_file}</b></span><br />
			<div class="padding">
				{#if context.song_length}
					<div class="row">
						<span class="text-right" style="width:7%"
							>{((context.song_length * context.percent_done) / 100).toFixed(0)}s</span
						>
						<div
							class="secondary no-margin no-padding"
							style="width: {context.percent_done * 0.7}%"
						>
							<span>&nbsp;</span>
						</div>
						<div class="max no-margin no-padding" />
						<span class="no-margin no-padding" style="width: 13%"
							>| {context.song_length.toFixed(0)}s</span
						>
					</div>
				{/if}
			</div>

			<nav class="margin no-space">
				<div class="center">
					<button class="border left-round no-margin">
						<i>skip_previous</i>
						<span>Restart</span>
					</button>
					{#if context.paused}
						<button on:click={pauseSong} class="border no-round no-margin">
							<i>play_arrow</i>
							<span>Play</span>
						</button>
					{:else}
						<button on:click={pauseSong} class="border no-round no-margin">
							<i>pause</i>
							<span>Pause</span>
						</button>
					{/if}
					<button on:click={stopSong} class="border right-round no-margin">
						<i>stop</i>
						<span>Stop</span>
					</button>
				</div>
			</nav>
		</article>
	{:else}{/if}
</div>
