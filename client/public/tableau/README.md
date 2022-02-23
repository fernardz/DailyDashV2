# Creating WDC connector for our FastAPI using Pydantic model definitions

One of the downsides I have with the free version of Tableau is that I cannot generate direct connections to my db's. Generally in Qlikview I would just go ahead and write queries to be loaded on refresh.
However there is an option, to address it, even if a bit more convoluted than just typing in `SELECT * FROM Table`.
We can use Tableau's Web Data Connectors. This consist in an html site loading all the libraries and a button, and a js script presenting the schema of the table and the `GET` call to the API.

This is just a quick and dirty web data connector to present the data to
Tableau. This currently this is only set for Strava Activities.

>Since for this specific project I was already running Vue, the WDC connector can just be stored in the `client\public` folder and it will served properly for Tableau Desktop to use as a data source. We could also autogenerate a JSON on Airflow as periodically.

## Setting up the HTML

We are going to be keeping the HTML short and sweet. All we really need is to generate a landing page and load all our external dependencies.

```html
<html>

<head>
    <title>Strava Activities</title>
    <meta http-equiv="Cache-Control" content="no-store" />

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"
        integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS"
        crossorigin="anonymous"></script>

    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
</head>

<body>
    <div class="container container-table">
        <div class="row vertical-center-row">
            <div class="text-center col-md-4 col-md-offset-4">
                <button type="button" id="submitButton" class="btn btn-success" style="margin: 10px;">Get Strava
                    Data!</button>
            </div>
        </div>
    </div>
</body>

```

The important dependencies are `jquery` and `connectors.tableau`. Really all our code is doing is submitting a form on press of the button. There are additional ways in which we can provide entry for additional filters, but since this is only for my individual data I'm not too worried about time.

## Setting up the JavaScript

Now this is were the meat of the connector is located. A set of great examples can be obtained at the [Web Data Connector website](https://tableau.github.io/webdataconnector/docs/wdc_use_in_tableau.html).

The script requires two things:

* Schema
* Api Call

For the schema we already have a pydantic model define:

```python
class StravaActivityCreate(BaseModel):
    """
    Pydantic class used for data validation.
    Used to validate SQL inserts into Strava Table

    Args:
        BaseModel (BaseModel): Standard pydantic Base Model
    """
    name: str
    type: str
    start_date: datetime
    distance: float
    moving_time: int
    average_speed: Optional[int] = None
    max_speed: Optional[float] = None
    average_cadence: Optional[float] = None
    average_heartrate: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    kilojoules: Optional[float] = None
```

So to translate that into our JS definition is pretty straight forward. We are just replacing the python data types with the ones defined by the [Tableau Data Enum](https://tableau.github.io/webdataconnector/docs/api_ref.html#webdataconnectorapi.datatypeenum). We define them as the columns of the schema.

```javascript
            myConnector.getSchema = function (schemaCallback) {
                var cols = [{
                    id: "name",
                    dataType: tableau.dataTypeEnum.string
                }, {
                    id: "type",
                    dataType: tableau.dataTypeEnum.string
                }, {
                    id: "start_date",
                    dataType: tableau.dataTypeEnum.datetime
                }, {
                    id: "distance",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "moving_time",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_speed",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "max_speed",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_cadence",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_heartrate",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "weighted_average_watts",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "kilojoules",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "id",
                    dataType: tableau.dataTypeEnum.int
                }];

                var tableSchema = {
                    id: "strava_activity",
                    alias: "Personal Strava Activity Data",
                    columns: cols
                };

                schemaCallback([tableSchema]);
            };
```

Our actual schema definition is formed with the snippet at the end:

```javascript
                var tableSchema = {
                    id: "strava_activity",
                    alias: "Personal Strava Activity Data",
                    columns: cols
                };
```

That gets set as the callback for out `getSchema` on the connector. Now we need to provide the connector a way to actually get the data from our API. This requires setting the `getData` method of our `myConnector` object. This will be a basic `GET` call using `getJSON`.

```javascript
            myConnector.getData = function (table, doneCallback) {
                $.getJSON("http://rasp-srv:8000/strava", function (resp) {
                    var feat = resp,
                        tableData = [];

                    // Iterate over the JSON object
                    for (var i = 0, len = feat.length; i < len; i++) {
                        tableData.push({
                            "name": feat[i].name,
                            "type": feat[i].type,
                            "start_date": feat[i].start_date,
                            "distance": feat[i].distance,
                            "moving_time": feat[i].moving_time,
                            "average_speed": feat[i].average_speed,
                            "max_speed": feat[i].max_speed,
                            "average_cadence": feat[i].average_cadence,
                            "average_heartrate": feat[i].average_cadence,
                            "weighted_average_watts": feat[i].weighted_average_watts,
                            "kilojoules": feat[i].kilojoules,
                            "id": feat[i].id
                        });
                    }

                    table.appendRows(tableData);
                    doneCallback();
                });
            };

            tableau.registerConnector(myConnector);
```

We define each individual value in our dictionary and assign the corresponding value from our `feat` JSON response. Finally we need to append the result of the call to our previously defined table object.

Once that is done we register our component with `tableau.registerConnector`. Finally we create the event listener for when the user presses the button on our landing page.

```javascript
            $(document).ready(function () {
                $("#submitButton").click(function () {
                    tableau.connectionName = "Strava Activity Feed"; // This will be the data source name in Tableau
                    tableau.submit(); // This sends the connector object to Tableau
                });
            }
```

So overall our connector will look like this:

```html
<html>

<head>
    <title>Strava Activities</title>
    <meta http-equiv="Cache-Control" content="no-store" />

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"
        integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS"
        crossorigin="anonymous"></script>

    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
</head>

<body>
    <div class="container container-table">
        <div class="row vertical-center-row">
            <div class="text-center col-md-4 col-md-offset-4">
                <button type="button" id="submitButton" class="btn btn-success" style="margin: 10px;">Get Strava
                    Data!</button>
            </div>
        </div>
    </div>
</body>

<script type = "text/javascript">
    (function () {
            //Create the connector object
            var myConnector = tableau.makeConnector();

            // Define the schema
            myConnector.getSchema = function (schemaCallback) {
                var cols = [{
                    id: "name",
                    dataType: tableau.dataTypeEnum.string
                }, {
                    id: "type",
                    dataType: tableau.dataTypeEnum.string
                }, {
                    id: "start_date",
                    dataType: tableau.dataTypeEnum.datetime
                }, {
                    id: "distance",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "moving_time",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_speed",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "max_speed",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_cadence",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "average_heartrate",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "weighted_average_watts",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "kilojoules",
                    dataType: tableau.dataTypeEnum.float
                }, {
                    id: "id",
                    dataType: tableau.dataTypeEnum.int
                }];

                var tableSchema = {
                    id: "strava_activity",
                    alias: "Personal Strava Activity Data",
                    columns: cols
                };

                schemaCallback([tableSchema]);
            };

            // Download the data
            myConnector.getData = function (table, doneCallback) {
                $.getJSON("http://rasp-srv:8000/strava", function (resp) {
                    var feat = resp,
                        tableData = [];

                    // Iterate over the JSON object
                    for (var i = 0, len = feat.length; i < len; i++) {
                        tableData.push({
                            "name": feat[i].name,
                            "type": feat[i].type,
                            "start_date": feat[i].start_date,
                            "distance": feat[i].distance,
                            "moving_time": feat[i].moving_time,
                            "average_speed": feat[i].average_speed,
                            "max_speed": feat[i].max_speed,
                            "average_cadence": feat[i].average_cadence,
                            "average_heartrate": feat[i].average_cadence,
                            "weighted_average_watts": feat[i].weighted_average_watts,
                            "kilojoules": feat[i].kilojoules,
                            "id": feat[i].id
                        });
                    }

                    table.appendRows(tableData);
                    doneCallback();
                });
            };

            tableau.registerConnector(myConnector);

            // Create event listeners for when the user submits the form
            $(document).ready(function () {
                $("#submitButton").click(function () {
                    tableau.connectionName = "Strava Activity Feed"; // This will be the data source name in Tableau
                    tableau.submit(); // This sends the connector object to Tableau
                });
            });
        })();
</script>

</html>
```

## Taking it a step further

Obviously the connector already works. However if we needed to create some for all our tables this would take a while to accomplish. There are a couple of options we can take to make the creation of them faster. One that is extremely easy to accomplish is to just use the previously defined `pydantic` classes and use that to generate the code.

To do so we will make use of jinja2 templating to create self contained files for all of our connectors.

## Converting our schema definition

Assuming a `pydantic` class as follows:

```python

class StravaActivityCreate(BaseModel):
    name: str
    type: str
    start_date: datetime
    distance: float
    moving_time: int
    average_speed: Optional[int] = None
    max_speed: Optional[float] = None
    average_cadence: Optional[float] = None
    average_heartrate: Optional[float] = None
    weighted_average_watts: Optional[float] = None
    kilojoules: Optional[float] = None
    test_date: date
```

we first setup our equivalencies between the python types to the tableau ones:

```python
python_to_tableau_dict={
'float':'tableau.dataTypeEnum.float',
'int':'tableau.dataTypeEnum.int',
'datetime':'tableau.dataTypeEnum.datetime',
'date':'tableau.dataTypeEnum.date',
'str':'tableau.dataTypeEnum.string'}

python_to_tableau_dict = defaultdict(lambda: None, python_to_tableau_dict)
```

We use a default dict to take care of missing cases (we define `None` as the default response but could set something like `undefined` instead).

Now all we need to obtain the correct dictionary for our columns is to iterate over the objects `__fields__` object.

```python
schema=[]
for k,i in StravaActivityCreate.__fields__.items():
    schema.append({'id':k, 'dataType':python_to_tableau_dict.get(i.type_.__name__)})
```

We just get the type definition of each item in string form with `type_`. We now have a dictionary with our table schema definition in terms Tableau will understand.

### Jinja2 Template

In order to use jinja2 we need to provide a template. For this template we need to pass the following variables:

* schema_name: What we want to call our schema
* schema_description: A description of our table
* fields: The dictionary containing the schema for our table
* api_endpoint: The location of our api endpoint

The html part of our template will be exactly the same as the one we created above, just a button with submit. We just use the `schema_name` to change some of the values.

```html
<head>
    <title>{{schema_name}}</title>
    <meta http-equiv="Cache-Control" content="no-store" />

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"
        integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS"
        crossorigin="anonymous"></script>

    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
</head>

<body>
    <div class="container container-table">
        <div class="row vertical-center-row">
            <div class="text-center col-md-4 col-md-offset-4">
                <button type="button" id="submitButton" class="btn btn-success" style="margin: 10px;">Get {{schema_name}}
                    Data!</button>
            </div>
        </div>
    </div>
</body>
```

Now for the javascript we will take advantage of a few things. One will be looping in our jinja2 template. So our schema definition in the template will just be:

```javascript
        myConnector.getSchema = function (schemaCallback) {
            var cols = [
                {% for field in fields -%}
                {id: "{{field.id}}", dataType: {{field.dataType}},},
                {% endfor -%}
                ];
            var tableSchema = {
                id: "{{schema_name}}",
                alias: "{{schema_description}}",
                columns: cols
            };
```

We will just iterate over every item in our dictionary and write the correct `javascript`.

The other change we will make will be to take advantage that the elements of our field are named the same as the properties, for example (`"name": feat[i].name`). So our API call can just be modified.

```javascript
        myConnector.getData = function (table, doneCallback) {
            $.getJSON("{{api_endpoint}}", function (resp) {
                var feat = resp;
                var tableData = [];

                // Iterate over the JSON object
                for (var i = 0, len = feat.length; i < len; i++) {
                    tableEntry = {};
                    var ref = feat[i]
                    Object.getOwnPropertyNames(ref).forEach(function(val, idx, array){
                        tableEntry[val] = ref[val]
                    });
                    tableData.push(tableEntry);
                }
                table.appendRows(tableData);
                doneCallback();
            });
        };
```

Using `getOwnPropertyNames` lets us generalize our method for all of our schemas.

Our whole template will looks as follows:

```html
<html>

<head>
    <title>{{schema_name}}</title>
    <meta http-equiv="Cache-Control" content="no-store" />

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"
        integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS"
        crossorigin="anonymous"></script>

    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
</head>

<body>
    <div class="container container-table">
        <div class="row vertical-center-row">
            <div class="text-center col-md-4 col-md-offset-4">
                <button type="button" id="submitButton" class="btn btn-success" style="margin: 10px;">Get {{schema_name}}
                    Data!</button>
            </div>
        </div>
    </div>
</body>

<script type="text/javascript">
    (function () {
        //Create the connector object
        var myConnector = tableau.makeConnector();

        // Define the schema
        myConnector.getSchema = function (schemaCallback) {
            var cols = [
                {% for field in fields -%}
                {id: "{{field.id}}", dataType: {{field.dataType}},},
                {% endfor -%}
                ];
            var tableSchema = {
                id: "{{schema_name}}",
                alias: "{{schema_description}}",
                columns: cols
            };

            schemaCallback([tableSchema]);
        };

        // Download the data
        myConnector.getData = function (table, doneCallback) {
            $.getJSON("{{api_endpoint}}", function (resp) {
                var feat = resp;
                var tableData = [];

                // Iterate over the JSON object
                for (var i = 0, len = feat.length; i < len; i++) {
                    tableEntry = {};
                    var ref = feat[i]
                    Object.getOwnPropertyNames(ref).forEach(function(val, idx, array){
                        tableEntry[val] = ref[val]
                    });
                    tableData.push(tableEntry);
                }
                table.appendRows(tableData);
                doneCallback();
            });
        };

        tableau.registerConnector(myConnector);

        // Create event listeners for when the user submits the form
        $(document).ready(function () {
            $("#submitButton").click(function () {
                tableau.connectionName = "{{schema_name}} Feed"; // This will be the data source name in Tableau
                tableau.submit(); // This sends the connector object to Tableau
            });
        });
    })();
</script>

</html>

```

Now its very straight forward, we pass the variables to the template in jinja2 and save the result.

```python
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

...

env = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent))
    template = env.get_template(template_name)
    template_variables = {'schema_name': schema_name,
                          'schema_description': schema_description,
                          'fields': schema,
                          'api_endpoint': api_endpoint}
    html_out = template.render(template_variables)
    with open(file_name, 'w') as fh:
        fh.write(html_out)
```

Running that program would then generate the correct WDC file to be then served however we want it.

We make this a funciton and then can easily convert all our classes to WDC's.

```python
from pydantic import BaseModel
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pathlib


def gen_wdc_from_pydantic_class(PydanticModel: BaseModel,
                                api_endpoint: str, schema_name: str,
                                schema_description: str,
                                file_name: str,
                                template_name: str) -> None:
    """
    function to generate a WDC file for Tableau from a Pydantic Class.
    This does not address fields define as List. Also aggregation would
    need to be done at the js level, the WDC file can be modified
    to accommodate this.

    Args:
        PydanticModel (BaseModel): Pydantic base model representing the table
        api_endpoint (str): location of the API endpoint
        schema_name (str): name for the table in WDC
        schema_description (str): table description
        file_name (str): desired name of the wdc connector
        template_name (str): location of the template for jinja
    """
    python_to_tableau_dict = {
        'float': 'tableau.dataTypeEnum.float',
        'int': 'tableau.dataTypeEnum.int',
        'datetime': 'tableau.dataTypeEnum.datetime',
        'date': 'tableau.dataTypeEnum.date',
        'str': 'tableau.dataTypeEnum.string'}

    python_to_tableau_dict = defaultdict(lambda: None, python_to_tableau_dict)

    schema = []
    for k, i in PydanticModel.__fields__.items():
        schema.append(
            {'id': k,
             'dataType': python_to_tableau_dict.get(i.type_.__name__)})

    env = Environment(loader=FileSystemLoader(pathlib.Path(__file__).parent))
    template = env.get_template(template_name)
    template_variables = {'schema_name': schema_name,
                          'schema_description': schema_description,
                          'fields': schema,
                          'api_endpoint': api_endpoint}
    html_out = template.render(template_variables)
    with open(file_name, 'w') as fh:
        fh.write(html_out)


if __name__ == "__main__":

    class ExampleSchema(BaseModel):
        name: str
        type: str
        start_date: datetime
        distance: float

    template_name = pathlib.Path(__file__).parent

    print(template_name)

    class_input = {
        "PydanticModel": ExampleSchema,
        "api_endpoint": 'localhost:8000/myendpoint',
        "schema_name": 'MyCoolTable',
        "schema_description": 'A Super Cool Table',
        "file_name": 'MyCoolTableWDC.html',
        "template_name": str('tableau_wdc_template.html')
    }

    gen_wdc_from_pydantic_class(**class_input)
```

Now from Tableau Desktop we can just import our data using the WDC option.

The completed function can be access on my github [deployment/tableau](https://github.com/frodrig3ND/DailyDashV2/tree/master/deployment/tableau)
