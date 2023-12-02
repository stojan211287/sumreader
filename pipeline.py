from sumreader.monad import Playbook
from sumreader.data import PandasDataframeConfig, Config

from jinja2 import Template


def jinja_render(template: str, **kwargs) -> str:
    return Template(template).render(**kwargs)


# define SystemCommand generating functions
# with signature (Config, **kwargs) => str
# (representing the SQL statement to use for example)
def print_schema(config: PandasDataframeConfig) -> str:
    output = ""
    for col, col_type in config.sample.dtypes.items():
        output += f"{col} {col_type}\n,"

    return output


def generate_create_table_statement_for_postgres(config: Config) -> str:
    template = """
        CREATE TABLE IF NOT EXISTS {{ table_schema }}.{{ table_name }}(
            {% for column, col_type in table_columns.items() -%}
                {{ column }} {{ col_type }}{% if not loop.last %},{% endif %}
            {% endfor -%}
        );
    """

    return jinja_render(
        template=template,
        table_schema="test",
        table_name="test",
        table_columns=config.to_mapping(),
    )


# define playbook pipeline
# ONLY defines the `recipe` for cation
# no execution will happen until a dataset example has been passed
pipeline = Playbook() >> print_schema >> generate_create_table_statement_for_postgres

if __name__ == "__main__":
    pipeline << PandasDataframeConfig(
        url="https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
    )
