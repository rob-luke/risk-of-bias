# Visualisation

There's no need to reinvent the wheel when it comes to figures. We recommend using [robvis](https://mcguinlu.shinyapps.io/robvis/) to create plots from risk-of-bias data. Our export functions generate files that robvis can read directly. See the [exporting for visualisation](api.md#exporting-for-visualization) section of the API docs for details.

For a quick look at agreement between two assessors you can create a simple scatter plot using `plot_assessor_agreement`. This displays each question along the x-axis and the response categories on the y-axis, with marker colours indicating agreement.
