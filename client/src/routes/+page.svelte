<script>
	import { page } from '$app/stores';
	console.log($page.data.nav_data);
</script>

<!-- display boxes with the navigation links -->
<!-- $page.data.nav_data like in navbar -->
<!-- {"id":1,"name":"ממתינים לאישור","url":"/waiting-approval","order":0}{"id":2,"name":"פרויקטים רצים","url":"/running-projects","order":1}{"id":3,"name":"פרויקטים גמורים","url":"/done-projects","order":2}{"id":4,"name":"פרויקטים שלא אושרו","url":"/not-approved","order":3}{"id":5,"name":"ניהול תזרימי","url":"/cash-flow","order":4}{"id":6,"name":"יצירת סטטוסים","url":"/create-statuses","order":5} -->
<div class="boxes">
	{#each $page.data.nav_data as item}
		<div class="box">
			<a href={item.url}>
				<div class="box-content">
					<div class="box-title">{item.name}</div>
				</div>
			</a>
		</div>
	{/each}
</div>

<style lang="scss">
	.boxes {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		align-items: center;
		margin: 0 1.5rem;
		.box {
			width: 300px;
			height: 300px;
			margin: 1rem;
			background-color: #f5f5f5;
			.box-content {
				display: flex;
				justify-content: center;
				align-items: center;
				height: 100%;
				width: 100%;
				.box-title {
					font-size: 1.5rem;
					font-weight: bold;
				}
			}
		}
	}
</style>
