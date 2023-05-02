<script>
	export let context;
	export let filteredSongs;
    let editmode = ""
    $: newfilename = editmode
    let query = ""
    $: filterSongs(context.files, query)

	function filterSongs(files, query) {
		filteredSongs = files.filter((file) => {
			return file.toLowerCase().includes(query.toLowerCase());
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

    async function updateFileName(file) {
        const res = fetch('api/files/rename', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ file: file, newname: newfilename })
        });
        editmode = ""

        filteredSongs = filteredSongs.map((song)=>{
            if (song == file) {
                return newfilename
            } else {
                return song
            }
        })
    }

    async function deleteFile(file) {
        const res = fetch('api/files/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ file: file })
        });
        editmode = ""
    }
</script>

	<div style="max-width: 500px; margin-top: 20px;">
		<h5 class="primary-text">Select a Song</h5>
		<div class="field border prefix round">
			<i>search</i><input
				on:input={(e)=>{query = e.target.value}}
				on:change={tryPlay}
				type="text"
				placeholder="Select a song"
			/>
		</div>
		{#each filteredSongs as file}
			<article class="border round padding small-margin">
                <div class="row">
                    {#if editmode == file}
                        <input type="text" bind:value={newfilename} />
                    {:else}

                    <i>audiotrack</i>
                    <h7 style="font-size:1.2em">{file}</h7>
                    {/if}
                </div>
				<div class="row">
                    {#if editmode == file}
                        <button class="margin tertiary" on:click={()=>{editmode = ""}}>
                            <i>close</i>
                            Edit Mode Off
                        </button>
                        <button class="margin secondary" on:click={updateFileName(file)}>
                            <i>save</i>
                            Save
                        </button>
                        <button class="margin error" on:click={()=>{deleteFile(file)}}>
                            <i>delete</i>
                            Delete File!
                        </button>
                    {:else}
                    <button on:click={()=>{editmode = file}} class="margin tertiary border">
                        <i>edit</i>
                        Edit File
                    </button>
					<button class="margin secondary border" on:click={addToPlaylist(file)}>
						<i>add</i>
                        Add to Playlist
					</button>
					<button class="margin" on:click={selectSong(file)}>
						<i>play_arrow</i>
                        Play
					</button>
                    {/if}
				</div>
			</article>
		{/each}
	</div>
