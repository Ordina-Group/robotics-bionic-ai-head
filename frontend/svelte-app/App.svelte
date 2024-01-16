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
	
	function doConfig () {
	    fetch('http://localhost:8080/configure/{$configNumber}')
	}
	
	function doManualNumber () {
	    fetch('http://localhost:8080/manualnumber/{$manualNumberServo}/{$manualNumberAngle}')
	}
	
	function doManualName () {
	    fetch('http://localhost:8080/manualname/{$selectedServoName}/{$manualNameAngle}')
	}
	
	function doCloseEyes () {
		fetch('http://localhost:8080/closeeyes')
	}
	
	function doOpenEyes () {
		fetch('http://localhost:8080/openeyes')
	}
	
	function doNodYes () {
		fetch('http://localhost:8080/yes')
	}
	
	function doShakeNo () {
		fetch('http://localhost:8080/no')
	}
	
	function doRest () {
		fetch('http://localhost:8080/rest')
	}
	
	function doBlink () {
		fetch('http://localhost:8080/blink')
	}
	
	function doLaugh () {
		fetch('http://localhost:8080/laugh')
	}
	
	function doReset () {
		fetch('http://localhost:8080/reset')
	}
	
	function doPlaySound () {
		fetch('http://localhost:8080/sound')
	}
</script>

<main>
	<h1>YouBionic Robot Controls</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	<Button class="primary lg" on:click={doCloseEyes}> Close Eyes </Button>
	<Button class="primary lg" on:click={doOpenEyes}> Open Eyes </Button>
	<br>
	<Button class="primary lg" on:click={doNodYes}> Nod Yes </Button>
	<Button class="primary lg" on:click={doShakeNo}> Shake No </Button>
	<br>
	<Button class="primary lg" on:click={doRest}> Rest </Button>
	<Button class="primary lg" on:click={doBlink}> Blink </Button>
	<br>
	<Button class="primary lg" on:click={doLaugh}> Laugh </Button>
	<Button class="primary lg" on:click={doReset}> Reset </Button>
	<br>
	<Button class="primary lg" on:click={doPlaySound}> Play Sound </Button>
	<br>
	<input type='number' bind:value={configNumber} min=0 max=15/>
	<br>
	<Button class="primary lg" on:click={doConfig}> Config </Button>
	<br>
	<input type='number' bind:value={manualNumberServo} min=0 max=15 />
	<input type='number' bind:value={manualNumberAngle} min=0 max=180/>
	<br>
	<Button class="primary lg" on:click={doManualNumber}> Manual Input By Number </Button>
	<br>
	<select bind:value={selectedServoName}>
	    {#each servoNameOptions as value}<option {value}>{value}</option>{/each}
    </select>
    <input type='number' bind:value={manualNameAngle} min=0 max=180 />
    <br>
    <Button class="primary lg" on:click={doManualName}> Manual Input by Name </Button>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
