<script>
import {displayComment} from "./stores"
import {clickOutside} from "./click-outside.action"
function dislike() {
    $displayComment=!$displayComment
}
let comment
const handleClickOutsideCom = (event) => {
		$displayComment = false;
        console.log("here")
	};

    //inserer fonctions bon et mauvais resultats

</script>

<div class="buttons float-right inline-flex" >
    <button class="dislike m-2 p-1" on:click={dislike}>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path></svg>
    </button>
    <button class="like m-2 p-1">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
    </button>
</div>
{#if $displayComment}
<div class="boxComment bg-white shadow max-w-xs absolute right-0 p-4 " use:clickOutside on:clickoutside={handleClickOutsideCom} >
<div class="titre text-xl"><b class="underline">Aidez nous</b> à nous améliorer</div>
<p>Pouvez-vous décrire pourquoi ce résultat de vous convient pas ?</p>
<textarea bind:value={comment} class="border-2 border-gray"></textarea>
<button class="envoyer py-1 px-2 text-white " >Envoyer</button>
</div>
{/if}

<style>
.like,.dislike{
    background-color: var(--primary);
    opacity: 58%;
    border-radius: 100%;
}
.like:hover,.dislike:hover{
    opacity: 100%;
}
.titre{
    color: var(--primary);
}
.envoyer{
    background-color: var(--primary);
}

</style>