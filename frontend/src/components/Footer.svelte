<footer>
  <span>
    &copy; {new Date().getFullYear()} DNUM - {data.index_name}.
    Powered by <a href="https://sapper.svelte.dev" target="_blank">Sapper</a>.
    Nous écrire <a href="mailto://{data.contact}">✉️</a>.
    <a href="https://github.com/datalab-mi/moteur-de-recherche">Dépot</a>
  </span>
</footer>




<script>
  import { onMount } from 'svelte';
  import { userData } from './stores.js';
  let data = {}
  const unsubscribe = userData.subscribe(value => {
    data = value;
  });

</script>

<style>
  footer {
    color: #AAA;
    font-size: 1em;
    font-family: Rubik, sans-serif;
    margin: 1em auto;
    padding: 1em 2em;
    text-align: center;
    width: 100%;
    }

</style>
