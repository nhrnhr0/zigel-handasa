<script>
	let new_comment;
	export let comments;
</script>

<div class="row">
	<div class="col-8">
		<!-- comments -->
		<div class="row">
			<div class="form-group">
				<label for="comments">הערה חדשה</label>
				<textarea
					class="form-control"
					id="comments"
					name="comments"
					rows="3"
					placeholder="הערות נוספות"
					bind:value={new_comment}
				/>
			</div>
		</div>
		<br />
		<div class="row">
			<div class="form-group">
				<button
					class="btn btn-secondary add-comment-btn"
					disabled={!new_comment}
					on:click={(e) => {
						e.preventDefault();
						comments.unshift({
							comment: new_comment,
							created_at: new Date()
						});
						new_comment = '';
						comments = [...comments];
					}}
				>
					הוסף הערה
				</button>
			</div>
		</div>
		<br />
		<div class="comments">
			{#each comments as comment}
				<div class="card my-comment">
					<div class="card-body">
						<div class="row">
							<div class="col" style="white-space: pre-line;">
								{comment.comment}
							</div>
						</div>
						<div class="row">
							<div class="col">
								- {new Date(comment.created_at).toLocaleString('he-IL', {
									timeZone: 'Asia/Jerusalem'
								})}
								(לפני {Math.floor(
									(new Date().setHours(0, 0, 0, 0) -
										new Date(comment.created_at).setHours(0, 0, 0, 0)) /
										(1000 * 60 * 60 * 24)
								)} ימים)
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>

<style lang="scss">
	.my-comment {
		margin-bottom: 1rem;
	}
	.comments {
		max-height: 250px;
		overflow-y: auto;
		.my-comment {
			background-color: #f5f5f5;
		}
	}
</style>
