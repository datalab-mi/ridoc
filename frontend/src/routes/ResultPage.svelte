<script>
  import { onMount } from "svelte";
  import {
    httpClient,
    index,
    upload,
    createMeta,
    isEmpty,
  } from "../components/utils.js";
  import { envJson, itemJson } from "../components/user-data.store";
  import Ratesearch from "../components/ratesearch.svelte";
  import { user } from "../components/stores.js";

  import * as pdfjsLib from "pdfjs-dist/build/pdf";
  import * as pdfjsWorker from "pdfjs-dist/build/pdf.worker.mjs";
  pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;
  // import  pdfjs  from 'pdfjs-dist';
  // const pdfjsWorker = await import('pdfjs-dist/build/pdf.worker.entry');
  // import * as pdfjsLib from "pdfjs-dist";
  // import * as pdfjsWorker from "pdfjs-dist/build/pdf.worker.mjs";
  // import pdfjsWorker from "../../../../node_modules/pdfjs-dist/build/pdf.worker.entry";
  // pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

  import Entry from "../components/Entry.svelte";
  let titre = true;
  let meta = undefined;
  let display;
  let readonly = true;
  let required = false;
  let inputs = [];
  let _source_includes = "";
  let filename;
  let link;

  const displayPdf = (url) => {
    // Asynchronous download of PDF
    var loadingTask = pdfjsLib.getDocument({
      url: url,
      httpHeaders: { Authorization: `Bearer ${$user.jwToken}` },
      withCredentials: true,
    });
    loadingTask.promise.then(
      function (pdf) {
        console.log("PDF loaded");

        // Fetch the first page
        var pageNumber = 1;
        pdf.getPage(pageNumber).then(function (page) {
          console.log("Page loaded");

          var scale = 1.5;
          var viewport = page.getViewport({ scale: scale });

          // Prepare canvas using PDF page dimensions
          var canvas = document.getElementById("the-canvas");
          var context = canvas.getContext("2d");
          canvas.height = viewport.height;
          canvas.width = viewport.width;

          // Render PDF page into canvas context
          var renderContext = {
            canvasContext: context,
            viewport: viewport,
          };
          var renderTask = page.render(renderContext);
          renderTask.promise.then(function () {
            console.log("Page rendered");
          });
        });
      },
      function (reason) {
        // PDF loading error
        console.error(reason);
      },
    );
  };
  onMount(() => {
    // const pdfjs = await import('../node_modules/pdfjs-dist/build/pdf');
    // const pdfjsWorker = await import('../../node_modules/pdfjs-dist/build/pdf.worker.entry');

    function getMeta() {
      // Filter entries in $itemJson with isDetailed at false
      inputs = $itemJson.inputs.filter(
        (entry) =>
          (entry.isDetailed !== undefined && entry.isDetailed) ||
          entry.isDetailed == undefined,
      );
      _source_includes = inputs.map((x) => x.key).join();
      httpClient()
        .fetch(
          "./backend/user/" +
            $envJson["index_name"] +
            "/_doc/" +
            filename +
            "?_source_includes=" +
            _source_includes,
        )
        .then((response) => response.json())
        .then((data) => {
          [meta, display] = createMeta(inputs, data, {});
        });
    }
    function waitindex() {
      //eviter les problèmes de undefined
      if ($envJson["index_name"] != undefined) {
        //const { page } = stores(); // sveltekit
        const urlParams = new URLSearchParams(window.location.search);
        filename = urlParams.get("filename");
        link = `/ViewerJS/?zoom=page-width#../backend/user/files/${$envJson.dstDir}/${filename}`;
        const url = `/backend/user/files/${$envJson.dstDir}/${filename}`;

        getMeta();
        displayPdf(url);
      } else {
        setTimeout(waitindex, 100);
      }
    }
    waitindex();
  });
</script>

<svelte:head>
  <title>{filename}</title>
</svelte:head>

{#if meta != undefined && $itemJson != undefined && filename != undefined}
  <div class="grid grid-cols justify-center">
    <div
      class="card bg-white place-self-center p-10 grid grid-cols justify-center rounded shadow w-auto"
    >
      <div class="mb-6">
        <Ratesearch class="" {filename} />

        {#each meta as { value, key, type, placeholder, innerHtml, highlight, metadata, rows, color } (key)}
          {#if !isEmpty(value) || (!readonly && metadata)}
            <Entry
              {readonly}
              {required}
              bind:value
              {key}
              {type}
              {placeholder}
              {innerHtml}
              {highlight}
              {metadata}
              {rows}
              {color}
            />
          {/if}
        {/each}
      </div>
      <!-- <iframe
        class="place-self-center"
        src={link}
        width="1025"
        height="578"
        allowfullscreen
        webkitallowfullscreen
      ></iframe> -->

      <canvas id="the-canvas"></canvas>
    </div>
  </div>
{/if}

<style>
  .card {
    max-width: min-content !important;
  }
  .tag {
    max-width: min-content !important;
    background-color: #f0f0f0;
    border-radius: 40px;
  }

  #the-canvas {
    border: 1px solid black;
    direction: ltr;
  }
</style>
