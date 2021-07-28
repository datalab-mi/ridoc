        
        <svelte:head>
        <script src="https://unpkg.com/jquery"></script>
        <script src="https://unpkg.com/knockout@3.5.1/build/output/knockout-latest.js" ></script>
        <script src="https://unpkg.com/survey-knockout@1.8.56/survey.ko.min.js"></script>

        <script src="https://unpkg.com/emotion-ratings@2.0.1/dist/emotion-ratings.js"></script>
        <script src="https://unpkg.com/surveyjs-widgets@1.8.56/surveyjs-widgets.min.js"></script>
        <link href="https://unpkg.com/survey-knockout@1.8.57/modern.css" type="text/css" rel="stylesheet" />
    </svelte:head>
        
    <div class="emoRating bg-white rounded shadow p-6 float-right">
        <h2 class="">Votre avis nous intéresse</h2>
        <div id="surveyContainer" class='' >
        
        <script>
Survey.StylesManager.applyTheme("modern");

var surveyJSON = {"pages":[{"name":"page1","elements":[{"type":"rating","name":"Comment décririez-vous votre expèrience sur le site ?","useDisplayValuesInTitle":false,"maxWidth":"450px","startWithNewLine":false,"hideNumber":true,"minRateDescription":"Médiocre","maxRateDescription":"Optimale"}]}]}

function sendDataToServer(survey) {
    survey.sendResult('fad344d2-af8d-458b-b7df-874a9d1e8955');
}

var survey = new Survey.Model(surveyJSON, "surveyContainer");
survey.onComplete.add(sendDataToServer);
        
        </script>
        </div>
    </div>

    <style>
        h2{
            color: var(--primary);
            font-weight: bold;
            text-decoration: underline;
        }
        .emorating{
            width: fit-content;
        }
    </style>