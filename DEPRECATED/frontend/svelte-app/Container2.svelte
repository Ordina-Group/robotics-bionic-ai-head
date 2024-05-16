<script>
	import Button from "./Button.svelte"
	let configNumber = null
	let manualNumberServo = 0
	let manualNumberAngle = 90
	let manualNameAngle = 90
	let selectedServoName = 'mouth'
	let servoNameOptions = [
	    'eyeRight',
    	'eyeLeft',
    	'eyeRightOpen',
    	'eyeLeftOpen',
    	'eyesUpDown',
    	'mouth',
    	'headTilt',
    	'headSwivel',
    	'headPivot'
	 ]
	let passiveColor = '#007f92';
	let textColor = '#3da4bf';
	
	
	function doConfig () {
	    fetch('http://localhost:8080/configure/{$configNumber}')
	}
	
	function doManualNumber () {
	    fetch('http://localhost:8080/manualnumber/{$manualNumberServo}/{$manualNumberAngle}')
	}
	
	function doManualName () {
	    fetch('http://localhost:8080/manualname/{$selectedServoName}/{$manualNameAngle}')
	}
	
		function doReset () {
		fetch('http://localhost:8080/reset')
	}
	
</script>

<main>
	<h2>Advanced Robot Controls</h2>
	<div class=grid>
	<div class="resetButton">
	<Button class="primary reset" on:click={doReset}> Reset </Button>
	</div>
	<div class="configButton">
	<label>Servomotor Number (0-15)</label>
	<input type='number' bind:value={configNumber} min=0 max=15/>
	<br>
	<Button class="primary medium" on:click={doConfig}> Config </Button>
	<br>
	</div>
	<div class="byNumber">
	<label>Servomotor Number</label>
	<input type='number' bind:value={manualNumberServo} min=0 max=15 />
	<br>
	<label>Desired Angle</label>
	<input type='number' bind:value={manualNumberAngle} min=0 max=180/>
	<br>
	<Button class="primary semiLarge" on:click={doManualNumber}> Manual Input By Number </Button>
	</div>
	<div class="byName">
		<label>Servomotor</label>
	<select bind:value={selectedServoName}>
	    {#each servoNameOptions as value}<option {value}>{value}</option>{/each}
    </select>
	<br>
	<label>Desired Angle</label>
    <input type='number' bind:value={manualNameAngle} min=0 max=180 />
    <br>
    <Button class="primary semiLarge" on:click={doManualName}> Manual Input by Name </Button>
	</div>
	</div>
	

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 440px;
		margin: 0 auto;
		background-color: #58595b;
	}

	h1 {
		color: #f58220;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
		font-family: 'Roboto Condensed';
	}
	
	h2 {
		color: #f58220;
		text-transform: uppercase;
		font-size: 2em;
		font-weight: 100;
		font-family: 'Roboto Condensed';
		margin: 0;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	
	.grid{ 
			background-color: #686a6e;
			display: grid;
			grid-template-columns: repeat(2, minmax(0,1fr));
			grid-template-rows: 5em 20em;
			width:30em;
			height: 21.6em;
			gap:0rem;
			padding: 0;
			margin: 0 auto;
			align: center;
			border: solid;
			border-width: 5px;
			border-radius: 8px;
			border-color: #f58220;
	}
	
	.resetButton{
	 align: center;
	 grid-row: 1 / 2;
	 margin: auto;
	}
	
	.configButton{
	 grid-row: 0;
	 margin: auto;
	}
	
	.byNumber{
		margin: auto;
	}
	
	.byName{
		margin: auto;
	}
</style>
