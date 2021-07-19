        
        <svelte:head>
        <script src="https://unpkg.com/jquery"></script>
        <script src="https://unpkg.com/knockout@3.5.1/build/output/knockout-latest.js" ></script>
        <script src="https://unpkg.com/survey-knockout@1.8.56/survey.ko.min.js"></script>

        <script src="https://unpkg.com/emotion-ratings@2.0.1/dist/emotion-ratings.js"></script>
        <script src="https://unpkg.com/surveyjs-widgets@1.8.56/surveyjs-widgets.min.js"></script>
    </svelte:head>
        
    <div class="emoRating bg-white w-1/5 rounded shadow p-6 float-right">
        <h2 class="">Votre avis nous intéresse</h2>
        <div id="surveyElement" class='p-3' >
        
        <script>
   
        var json = {
            elements: [
                {
                    "type": "emotionsratings",
                    "name": "emotionsratings-widget",
                    "title": "Comment décrieriez vous votre expérience sur le site",
                    "choices": ["1", "2", "3", "4", "5"]
                }
            ]
        };
        survey = new Survey.Model(json);


        survey.onComplete.add(function (sender) {
        document
            .querySelector('#surveyResult')
            .textContent = "Result JSON:\n" + JSON.stringify(sender.data, null, 3);
    });
        survey.render("surveyElement");
        
        </script>
        </div>

        <div id="surveyResult"></div>
    </div>

    <style>
        h2{
            color: var(--primary);
            font-weight: bold;
            text-decoration: underline;
        }
        sv_nav{
            float:right;
            background-color: var(--primary);
            border-radius: 2px;
        }
    </style>