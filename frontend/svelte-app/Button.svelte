<script>
  let isHovered = false;

  let buttonProps = {
  class:[$$restProps.class]
  }
</script>
  <button on:click
      on:mouseover
      on:mouseenter
      on:mouseleave
      on:focus
      on:blur
    {...buttonProps}>
      <slot/>
    </button>

<style>
  .primary {
    font-family: 'Roboto';
    background-color: #007f92;
    color: #3da4bf;
    transition: background-color 0.4s, color 0.2s;
	border-color: #e1e1e1;
	border-radius: 8px;
	border-width: 2px;
	margin: 2px;
	font-size: 2em;
	width: 5em;
	padding-right: 1em;
	padding-left: 1em;
  }

  .primary:hover {
    background-color: #e1e1e1;
    color: #007f92;
  }
</style>
