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