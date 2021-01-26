<script>

  import { onMount } from "svelte";
  import { user, list_logger, displayLogin } from '../stores.js';
  let email = "";
  let password = "";

  let isLoading = false;
  let isSuccess = false;

  async function submit({ email, password }) {
    var headers = new Headers();
    headers.append("Content-Type", "application/json");
    const res = await fetch("/api/auth", {
      method: "POST",
      body: JSON.stringify({username: email, password: password}),
      headers: headers
    })
    if (res.ok) {
      const resp = await res.json()
      return resp
    } else {
      throw new Error('mauvaise combinaison')
    }

  }

  let errors = {};

  const handleSubmit = () => {
    errors = {};

    if (email.length === 0) {
      errors.email = "Champs email vide!";
    }
    if (password.length === 0) {
      errors.password = "Champs mot de passe vide!";
    }

    if (Object.keys(errors).length === 0) {
      isLoading = true;
      submit({ email, password })
        .then(({access_token, role, rules, resources}) => {
          console.log(`Your new token is: ${access_token}`)
          const request_user = {role:role, jwToken:access_token, rules:rules, resources:resources}
          user.authenticate(request_user)
          isSuccess = true;
          isLoading = false;
          $displayLogin = false
          list_logger.concat({level: "success", message: `Loggé en tant que ${$user.role}`, ressource: "login"})
        })
        .catch(err => {
          console.log($user)
          user.updateKey("role", "visitor")
          list_logger.concat({level: "error", message: err, ressource: "login"})
          //errors.server = err;
          isLoading = false;
        });
    }
  };
</script>

<div class="form-popup">

<form on:submit|preventDefault={handleSubmit} >

  {#if isSuccess}
    <div class="success">
    <svg class="inline-block object-center fill-current w-8 h-8 " xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M4 8V6a6 6 0 1 1 12 0h-3v2h4a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8c0-1.1.9-2 2-2h1zm5 6.73V17h2v-2.27a2 2 0 1 0-2 0zM7 6v2h6V6a3 3 0 0 0-6 0z"/></svg>
      <br />
      Vous êtes désormais identifié.
    </div>
  {:else}
    <label>Email</label>
    <input name="email" placeholder="nom@dom.gouv.fr" bind:value={email} />

    <label>Password</label>
    <input name="password" type="password" bind:value={password} />

    <button type="submit" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
      {#if isLoading}
        <span>Identification...</span>
      {:else}
        <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M4 8V6a6 6 0 1 1 12 0v2h1a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8c0-1.1.9-2 2-2h1zm5 6.73V17h2v-2.27a2 2 0 1 0-2 0zM7 6v2h6V6a3 3 0 0 0-6 0z"/></svg>
        <span>Identification</span>
      {/if}

    </button>

    {#if Object.keys(errors).length > 0}
      <ul class="errors">
        {#each Object.keys(errors) as field}
          <li>{field}: {errors[field]}</li>
        {/each}
      </ul>
    {/if}
  {/if}
</form>
</div>

<style>
  form {
    padding: 4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  label {
    margin: 10px 0;
    align-self: flex-start;
    font-weight: 500;
  }

  input {
    border: none;
    border-bottom: 1px solid #ccc;
    margin-bottom: 20px;
    transition: all 300ms ease-in-out;
    width: 100%;
  }

  input:focus {
    outline: 0;
    border-bottom: 1px solid #666;
  }

  button {
    cursor: pointer;
    transition: all 300ms ease-in-out;
  }

  h1 {
    margin: 10px 20px 30px 20px;
    font-size: 40px;
  }


  .errors {
    list-style-type: none;
    padding: 10px;
    margin: 0;
    border: 2px solid #be6283;
    color: #be6283;
    background: rgba(190, 98, 131, 0.3);
  }

  .success {
    font-size: 24px;
    text-align: center;
  }

  .form-popup {
  display: block;
  position: fixed;
  top: 5em;
  right: 15px;
  width: 20rem;
  height: 20rem;
  border: 1px solid #f1f1f1;
  box-shadow: 2px 2px 8px black;
  border-radius: 4px;
  z-index: 9;
  background: #fff;

}

</style>
