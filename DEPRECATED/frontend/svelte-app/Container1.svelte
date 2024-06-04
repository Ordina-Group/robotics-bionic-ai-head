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
	export let advancedControlsVisible = false;
	
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
	
	function doPlaySound () {
		fetch('http://localhost:8080/sound')
	}
	
	function doSleep () {
		fetch('http://localhost:8080/sleep')
	}
	
	function doThink () {
		fetch('http://localhost:8080/sus')
	}
</script>

<main>
	<Button class="primary small" on:click={doOpenEyes}> Open Eyes </Button>
	<Button class="primary small" on:click={doCloseEyes}> Close Eyes </Button>
	<Button class="primary small" on:click={doNodYes}> Nod Yes </Button>
	<Button class="primary small" on:click={doShakeNo}> Shake No </Button>
	<br>
	<Button class="primary medium" on:click={doRest}> Rest </Button>
	<Button class="primary medium" on:click={doBlink}> Blink </Button>
	<Button class="primary medium" on:click={doLaugh}> Laugh </Button>
	<br>
	<Button class="primary large" on:click={doSleep}> Sleep </Button>
	<Button class="primary large" on:click={doThink}> Think </Button>
	<br>
	<Button class="primary large" on:click={doPlaySound}> Play Sound </Button>
	<Button class="primary large" on:click={() => (advancedControlsVisible = !advancedControlsVisible)}>Toggle controls</Button>
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

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
