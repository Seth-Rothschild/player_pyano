<script>
	let files;
	let outcome = '';
	async function uploadFile() {
		let body = new FormData();
		if (files.length) {
			for (let i = 0; i < files.length; i++) {
				body.append('files', files[i]);
			}
		}
		const res = await fetch('api/files/upload', {
			method: 'POST',

			body: body
		});
		if (res.status == 200) {
			outcome = 'Success';
		} else {
			outcome = 'Failed';
		}
	}
</script>

<div style="margin-top: 20px;">
	<h5 class="primary-text">Upload</h5>
	<div class="row">
		<button class="secondary">
			Choose Files
			<input accept=".mid" multiple bind:files type="file" id="file" name="file" />
		</button>
		<button disabled={files ? '' : 'disabled'} on:click={uploadFile}> Upload </button>
	</div>
</div>

<div
	on:click={() => {
		outcome = '';
	}}
	on:keydown={() => {
		outcome = '';
	}}
>
	<div class="toast pink white-text {outcome == 'Failed' ? 'active' : ''}">
		<i>error</i>
		<span>Failed to upload files</span>
	</div>
	<div class="toast green white-text {outcome == 'Success' ? 'active' : ''}">
		<i>done</i>
		<span>File upload success</span>
	</div>
</div>
