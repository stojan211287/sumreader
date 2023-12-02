from sumreader.monad import Playbook
from sumreader.data import PandasDataframeConfig, Config

from jinja2 import Template

from sumreader.type_mapper import pyarrow2redshift, pyarrow2athena, pyarrow_types_from_pandas

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


def generate_create_table_statement_for_redshift(config: Config) -> str:
    template = """
        CREATE TABLE IF NOT EXISTS {{ table_schema }}.{{ table_name }}(
            {% for column, col_type in table_columns.items() -%}
                {{ column }} {{ col_type }}{% if not loop.last %},{% endif %}
            {% endfor -%}
        );
    """

    raw_mapping = pyarrow_types_from_pandas(df=config.sample, index=False)
    dest_mapping = {k: pyarrow2redshift(v, string_type="VARCHAR(256)") for k, v in raw_mapping.items()}

    return jinja_render(
        template=template,
        table_schema="test",
        table_name="test",
        table_columns=dest_mapping,
    )

def generate_create_table_statement_for_athena(config: Config) -> str:
    template = """
        CREATE TABLE IF NOT EXISTS {{ table_schema }}.{{ table_name }}(
            {% for column, col_type in table_columns.items() -%}
                {{ column }} {{ col_type }}{% if not loop.last %},{% endif %}
            {% endfor -%}
        );
    """

    raw_mapping = pyarrow_types_from_pandas(df=config.sample, index=False)
    dest_mapping = {k: pyarrow2athena(v) for k, v in raw_mapping.items()}

    return jinja_render(
        template=template,
        table_schema="test",
        table_name="test",
        table_columns=dest_mapping,
    )


# define playbook pipeline
# ONLY defines the `recipe` for cation
# no execution will happen until a dataset example has been passed
pipeline = Playbook() >> print_schema >> generate_create_table_statement_for_athena >> generate_create_table_statement_for_redshift

if __name__ == "__main__":
    pipeline << PandasDataframeConfig(
        url="https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv"
    )
