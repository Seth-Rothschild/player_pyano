<script>
	export let context;
	async function stopSong() {
		for (let i = 0; i < 5; i++) {
			const res = await fetch('api/stop', {
				method: 'POST'
			});
			await new Promise((r) => setTimeout(r, 1000));
		}
		const res = await fetch('api/panic', {
			method: 'POST'
		});
	}
	async function toggleDebug() {
		const res = await fetch('api/debug', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ debug: !context.debug })
		});
	}
	async function updateEQ(index, newValue) {
		let newEQ = context.EQ;
		newEQ[index] = newValue;
		const res = await fetch('api/eq', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ eq: newEQ })
		});
	}
</script>

{#if context}
	<h5 class="primary-text">Admin</h5>
	<div class="field border row" style="max-width:100px">
		<input
			type="number"
			min="-20"
			max="20"
			step="1"
			value={context.EQ[0]}
			on:input={(e) => updateEQ(0, e.target.value)}
		/>
		<input
			type="number"
			min="-20"
			max="20"
			step="1"
			value={context.EQ[1]}
			on:input={(e) => updateEQ(1, e.target.value)}
		/>
		<input
			type="number"
			min="-20"
			max="20"
			step="1"
			value={context.EQ[2]}
			on:input={(e) => updateEQ(2, e.target.value)}
		/>
		<input
			type="number"
			min="-20"
			max="20"
			step="1"
			value={context.EQ[3]}
			on:input={(e) => updateEQ(3, e.target.value)}
		/>
		<input
			type="number"
			min="-20"
			max="20"
			step="1"
			value={context.EQ[4]}
			on:input={(e) => updateEQ(4, e.target.value)}
		/>
	</div>
	<nav>
		<button on:click={stopSong} class="border error"><i>stop</i>Panic</button>
		<button on:click={toggleDebug} class="border tertiary"><i>bug_report</i>Debug</button>
	</nav>
{/if}
