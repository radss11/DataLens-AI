# Data provenance

## Bundled dataset
`data/gapminder.csv` is the real Gapminder-style country-year dataset distributed by Plotly Express (`plotly.express.data.gapminder`). It contains 1,704 observations and 8 fields covering country, continent, year, life expectancy, population, GDP per capita, and ISO identifiers.

The dataset is bundled unchanged as the demonstration dataset. The application also accepts user-provided CSV files.

## Integrity policy
- No synthetic rows are generated.
- No values are imputed in the bundled data.
- The app does not silently drop rows.
- Any analysis is computed from the loaded dataframe.
- LLM prompts contain computed evidence rather than the raw dataframe, reducing the chance of unsupported claims.

For an interview or public GitHub repository, keep this provenance file and cite the upstream Plotly/GitHub source used to obtain the dataset.

## Upstream references

- Plotly Express documents `gapminder()` as a built-in dataset with 1,704 rows and the eight fields used here.
- The upstream Gapminder project provides the original data documentation and attribution guidance.

For the portfolio repository, link the Plotly documentation and Gapminder data pages from the README rather than claiming the data was collected by the project.
