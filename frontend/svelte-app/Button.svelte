<script>
  let buttonProps = {
  class:[$$restProps.class]
  }
</script>
  <button on:click
      on:mouseover
      on:mouseenter
      on:mouseleave
    {...buttonProps}>
      <slot/>
    </button>

<style>
  .primary{
    color:blue;
  }
  .lg{
    font-size:2em;
  }
</style>
