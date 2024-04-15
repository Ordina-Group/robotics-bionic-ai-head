<script>
	import Container1 from "./Container1.svelte"
	import Container2 from "./Container2.svelte"
	let advancedControlsVisible = false;
	
	
</script>
<main>
	<h1>YouBionic Robot Controls</h1>
	<div>
	<Container1 bind:advancedControlsVisible />
	{#if advancedControlsVisible}
	<Container2 />
	{/if}
	<div>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 440px;
		margin: 0 auto;
		background-color: #58595b;
		border: solid;
		border-radius: 10px;
		border-color: #f58220;
	}

	h1 {
		color: #f58220;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
		font-family: 'Roboto Condensed';
		margin: 0;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

</style>
