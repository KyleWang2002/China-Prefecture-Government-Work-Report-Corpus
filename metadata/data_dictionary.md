# Data dictionary

## `city_coverage.csv`

One row per municipal series in the current inventory.

| field | meaning |
|---|---|
| `province` | provincial-level division |
| `province_code` | six-digit province code used in the project |
| `city` | municipal series name |
| `city_code` | six-digit city code used in the project |
| `unit_type` | `prefecture-level city` or `municipality` |
| `start_year` | first year included in the current series |
| `end_year` | last year included in the current series |
| `missing_years` | explicitly recorded gaps inside the start/end interval |
| `verified` | whether the city-level series completed the current manual coverage check |

The public file intentionally omits the private source-link column and informal collection notes.

## `city_year_coverage.csv`

One row per year inside each city's recorded start/end interval.

`status` is:
- `available`
- `missing`

Years before `start_year` or after `end_year` are not automatically coded as missing.

## `prefecture_changes_2000_2018.csv`

Administrative changes relevant to interpreting municipal time series, including:
- prefecture-to-city conversions;
- league-to-city conversions;
- upgrades to prefecture-level city status;
- city renamings;
- newly established prefecture-level cities;
- abolished / merged prefecture-level cities.

Source URLs used to compile the table remain in the private research log rather than the public CSV.
