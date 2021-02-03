<footer>
  <span>
    &copy; {new Date().getFullYear()} DNUM - {(data.index_name + "").toUpperCase()}.
    Powered by <a href="https://sapper.svelte.dev" target="_blank">Sapper</a>.
    Nous écrire <a href="mailto://{data.contact}">✉️</a>.
    <a href={data.repository}>Dépot : v{appVersion}</a>

  </span>
</footer>

<script>
  import { userData } from './stores.js';
  import { onDestroy } from 'svelte';
  let data = {index_name: "", contact: ""}
  const unsubscribe = userData.subscribe(value => {
    data = value;
  });
  const appVersion = "APP_VERSION"
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
