<script>
	async function stopSong() {
		for (let i = 0; i < 5; i++) {
			const res = await fetch('api/stop', {
				method: 'POST'
			});
			await new Promise((r) => setTimeout(r, 1000));
		}
	}
</script>

<h5 class="primary-text">Admin</h5>
<nav>
	<button on:click={stopSong} class="border error"><i>stop</i>Panic</button>
</nav>
