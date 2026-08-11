# pandas Study Guide: Fundamentals to Advanced

pandas is Python's main library for labeled, tabular data. This guide moves from creating a table to cleaning, joining, reshaping, aggregating, and analyzing real datasets.

```python
import numpy as np
import pandas as pd
```

## 1. The Core Objects

### Series

A `Series` is a one-dimensional labeled array. It has values and an index.

```python
scores = pd.Series([82, 91, 76], index=["Asha", "Ben", "Chen"], name="score")

scores["Ben"]       # 91
scores.index         # Index(['Asha', 'Ben', 'Chen'], dtype='object')
scores.dtype         # usually int64
```

### DataFrame

A `DataFrame` is a two-dimensional labeled table. Columns can have different data types.

```python
students = pd.DataFrame({
    "name": ["Asha", "Ben", "Chen", "Dia"],
    "score": [82, 91, 76, 91],
    "city": ["Pune", "Delhi", "Pune", "Mumbai"],
    "passed": [True, True, True, True]
})
```

| Concept | NumPy | pandas |
|---|---|---|
| Main object | `ndarray` | `Series`, `DataFrame` |
| Labels | Position based | Index and column labels |
| Data types | Usually one per array | One dtype per column |
| Best suited for | Numeric arrays | Labeled/tabular data |
| Missing data tools | Basic | Rich, column-aware tools |

## 2. Creating and Loading Data

### From Python structures

```python
df = pd.DataFrame({
    "product": ["Pen", "Book", "Bag"],
    "price": [10.0, 80.0, 500.0],
    "stock": [100, 40, 8]
})

records = [
    {"product": "Pen", "price": 10},
    {"product": "Book", "price": 80}
]
df2 = pd.DataFrame(records)
```

### Common file formats

```python
df = pd.read_csv("sales.csv")
df = pd.read_csv("sales.tsv", sep="\t")
df = pd.read_excel("sales.xlsx", sheet_name="January")
df = pd.read_json("sales.json")
df = pd.read_parquet("sales.parquet")
```

Useful CSV arguments:

```python
df = pd.read_csv(
    "sales.csv",
    usecols=["date", "product", "revenue"],
    dtype={"product": "string"},
    parse_dates=["date"],
    na_values=["NA", "?", "missing"]
)
```

Use explicit paths instead of changing the process working directory:

```python
from pathlib import Path

data_path = Path("data") / "sales.csv"
df = pd.read_csv(data_path)
```

## 3. First Inspection of Any Dataset

```python
df.head()             # first 5 rows
df.tail(3)            # last 3 rows
df.sample(5, random_state=42)
df.shape              # (rows, columns)
df.columns
df.index
df.dtypes
df.info()             # structure, non-null counts, dtypes, memory summary
df.describe()         # numeric descriptive statistics
df.describe(include="all")
```

Also inspect quality:

```python
df.isna().sum()                    # missing count per column
df.isna().mean().mul(100)          # missing percentage
df.nunique()                       # unique count per column
df.duplicated().sum()              # duplicate row count
df["category"].value_counts(dropna=False)
```

A strong first pass asks:

- Is one row one observation?
- What does each column mean and what unit does it use?
- Are dtypes correct?
- Are missing values random or systematic?
- Are categories spelled consistently?
- Are numeric ranges plausible?
- Is the target column accidentally present in a feature?

## 4. Selecting Rows and Columns

### Column selection

```python
df["price"]                    # Series
df[["product", "price"]]     # DataFrame
df.price                       # works sometimes, but bracket syntax is safer
```

Bracket syntax works with spaces, method-name conflicts, and dynamic column names.

### `loc`: label based

```python
df.loc[0, "product"]
df.loc[0:2, ["product", "price"]]    # label slice includes both endpoints
df.loc[df["price"] > 50, ["product", "price"]]
```

### `iloc`: position based

```python
df.iloc[0, 1]
df.iloc[0:3, 0:2]                    # normal Python stop exclusion
df.iloc[[0, 2], [1, 3]]
```

### Scalar access

`at` and `iat` are optimized for a single scalar:

```python
df.at[0, "price"]
df.iat[0, 1]
```

### Filtering

```python
expensive = df[df["price"] > 100]

filtered = df[
    (df["price"] >= 50)
    & (df["stock"] > 0)
    & (df["product"].isin(["Book", "Bag"]))
]
```

Important rules:

- Use `&`, `|`, and `~`, not `and`, `or`, and `not`.
- Parenthesize each comparison.
- `isin` handles membership tests.
- `between` handles ranges inclusively by default.

```python
df[df["price"].between(50, 500)]
df[df["city"].notna()]
df.query("price >= 50 and stock > 0")
```

`query` is readable for simple expressions, but direct boolean masks are more general.

## 5. The Index

The index labels rows; it is not necessarily a simple row number.

```python
df = df.set_index("product")
df.loc["Book"]
df = df.reset_index()
```

Changing labels:

```python
df = df.rename(columns={"old_name": "new_name"})
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
```

Sorting:

```python
df.sort_values("price")
df.sort_values(["city", "price"], ascending=[True, False])
df.sort_index()
```

Most pandas operations align data by index labels, not merely by physical position:

```python
a = pd.Series([10, 20], index=["x", "y"])
b = pd.Series([1, 2], index=["y", "x"])
a + b       # x=12, y=21 because labels align
```

This alignment is powerful but can create unexpected missing values when labels differ.

## 6. Adding, Updating, and Removing Data

```python
df["value"] = df["price"] * df["stock"]
df["in_stock"] = df["stock"] > 0
df["discounted"] = np.where(df["price"] >= 100, df["price"] * 0.9, df["price"])
```

Use `loc` for conditional assignment:

```python
df.loc[df["stock"] == 0, "status"] = "sold out"
df.loc[df["stock"] > 0, "status"] = "available"
```

This avoids chained-assignment ambiguity such as `df[df["stock"] == 0]["status"] = ...`.

Functional assignment is useful in method chains:

```python
result = (
    df.assign(
        value=lambda x: x["price"] * x["stock"],
        price_with_tax=lambda x: x["price"] * 1.18
    )
)
```

Remove data:

```python
df = df.drop(columns=["temporary_column"])
df = df.drop(index=[0, 2])
```

Many methods return a new object by default. Assign the result or use a method chain. Overusing `inplace=True` often makes code harder to compose and does not guarantee a memory saving.

## 7. Missing Data

pandas may represent missing values with `NaN`, `NaT`, or `pd.NA`, depending on dtype.

### Detect

```python
df.isna()
df.isna().sum()
df.notna()
```

Never rely on `value == np.nan`. Use `isna`.

### Remove

```python
df.dropna()                              # rows with any missing value
df.dropna(subset=["target"])            # only target must be present
df.dropna(axis="columns", how="all")    # drop entirely empty columns
df.dropna(thresh=3)                      # keep rows with at least 3 non-missing values
```

### Fill

```python
df["age"] = df["age"].fillna(df["age"].median())
df["city"] = df["city"].fillna("Unknown")
df["reading"] = df["reading"].ffill()
df["reading"] = df["reading"].bfill()
```

Group-aware filling:

```python
df["income"] = df["income"].fillna(
    df.groupby("job")["income"].transform("median")
)
```

Do not blindly fill missing values. Missingness may itself contain information, and filling before train/test splitting can leak test information into training.

## 8. Data Types and Conversion

```python
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["active"] = df["active"].astype("boolean")
df["name"] = df["name"].astype("string")
df["category"] = df["category"].astype("category")
df = df.convert_dtypes()
```

`errors="coerce"` turns invalid values into missing values, which should then be audited.

Categories can reduce memory and express a finite set of labels:

```python
size_type = pd.CategoricalDtype(
    categories=["small", "medium", "large"],
    ordered=True
)
df["size"] = df["size"].astype(size_type)
```

Nullable pandas dtypes such as `Int64`, `boolean`, and `string` can represent `pd.NA` without forcing the column to ordinary floating point or Python objects.

## 9. String Data

Use the `.str` accessor for vectorized string operations:

```python
names = df["name"].astype("string")
df["name_clean"] = names.str.strip().str.title()

df["email"].str.lower()
df["code"].str.startswith("IN-")
df["text"].str.contains("python", case=False, na=False)
df["full_name"].str.split(" ", n=1, expand=True)
df["phone"].str.replace(r"\D", "", regex=True)
df["email"].str.extract(r"@([A-Za-z0-9.-]+)$", expand=False)
```

Specify `na=False` in boolean string tests when missing values should count as no match.

## 10. Dates and Times

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
df["weekday"] = df["date"].dt.day_name()
df["is_weekend"] = df["date"].dt.dayofweek >= 5
```

Date arithmetic:

```python
df["duration_days"] = (df["end_date"] - df["start_date"]).dt.days
df["due_date"] = df["start_date"] + pd.Timedelta(days=30)
```

Time-based resampling requires a datetime-like index:

```python
daily = df.set_index("date")["sales"].resample("D").sum()
monthly = df.set_index("date")["sales"].resample("MS").sum()
```

Time zones matter for real systems. Store event times in a consistent zone, often UTC, and convert for display.

## 11. Duplicates and Invalid Values

```python
df.duplicated()
df.duplicated(subset=["customer_id", "date"], keep=False)
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["customer_id"], keep="last")
```

Validate ranges and categories:

```python
invalid_age = ~df["age"].between(0, 120) & df["age"].notna()
invalid_status = ~df["status"].isin(["new", "active", "closed"])
```

Replacement:

```python
df["city"] = df["city"].replace({"Bombay": "Mumbai", "New Delhi": "Delhi"})
df["score"] = df["score"].clip(lower=0, upper=100)
```

Do not delete outliers merely because they are unusual. First decide whether they are data errors, genuine rare events, or values that need robust analysis.

## 12. Mapping, Applying, and Vectorization

For element mappings in a Series:

```python
grade_map = {"A": 4, "B": 3, "C": 2}
df["points"] = df["grade"].map(grade_map)
```

Prefer vectorized operations:

```python
df["revenue"] = df["price"] * df["quantity"]
df["label"] = np.where(df["revenue"] >= 1000, "high", "normal")
```

Use `apply` when no clear vectorized operation exists:

```python
def classify(row):
    if row["revenue"] >= 1000 and row["quantity"] >= 5:
        return "bulk-high"
    return "other"

df["class"] = df.apply(classify, axis=1)
```

Row-wise `apply(axis=1)` is convenient but often slower. Look for arithmetic, `.str`, `.dt`, `map`, `where`, `select`, or grouped transformations first.

## 13. Grouping and Aggregation

The pattern is **split, apply, combine**:

```python
summary = df.groupby("city")["revenue"].sum()
```

- Split rows into city groups.
- Apply `sum` within each group.
- Combine results into a Series.

Multiple statistics with clear output names:

```python
summary = (
    df.groupby("city", as_index=False)
      .agg(
          total_revenue=("revenue", "sum"),
          average_order=("revenue", "mean"),
          order_count=("order_id", "nunique"),
          max_order=("revenue", "max")
      )
)
```

Multiple grouping columns:

```python
df.groupby(["city", "category"], as_index=False)["revenue"].sum()
```

### `agg`, `transform`, and `filter`

- `agg` reduces each group to summary rows.
- `transform` returns one value per original row, aligned to the original index.
- Group `filter` keeps or removes whole groups.

```python
df["city_average"] = df.groupby("city")["revenue"].transform("mean")
df["vs_city_average"] = df["revenue"] - df["city_average"]

large_cities = df.groupby("city").filter(lambda group: len(group) >= 10)
```

By default, missing group keys are excluded. Use `dropna=False` when missing keys should form a group.

## 14. Combining Tables

### Concatenation

Use `concat` to place compatible tables below or beside one another:

```python
all_months = pd.concat([january, february, march], ignore_index=True)
side_by_side = pd.concat([features, predictions], axis=1)
```

### Merge: database-style joins

```python
orders_with_customers = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
    indicator=True
)
```

Join types:

| Join | Rows kept |
|---|---|
| `inner` | Keys found in both tables |
| `left` | Every left row; matching right data |
| `right` | Every right row; matching left data |
| `outer` | All keys from both tables |
| `cross` | Every left/right combination |

Different key names:

```python
result = left.merge(
    right,
    left_on="customer_code",
    right_on="id",
    how="left"
)
```

`validate` catches unexpected key relationships:

- `one_to_one`
- `one_to_many`
- `many_to_one`
- `many_to_many`

Always check row counts before and after a merge. Duplicate keys can multiply rows. `indicator=True` adds `_merge`, showing whether each result came from the left table, right table, or both.

### Index join

```python
result = left.join(right, how="left", rsuffix="_right")
```

`join` is convenient for index-based alignment; `merge` makes column-key joins explicit.

## 15. Reshaping Data

### Long to wide: `pivot`

```python
wide = df.pivot(index="date", columns="product", values="sales")
```

`pivot` requires each index/column combination to be unique.

### Long to wide with aggregation: `pivot_table`

```python
report = pd.pivot_table(
    df,
    index="city",
    columns="category",
    values="revenue",
    aggfunc="sum",
    fill_value=0,
    margins=True
)
```

### Wide to long: `melt`

```python
long = wide_df.melt(
    id_vars=["student"],
    value_vars=["math", "science", "english"],
    var_name="subject",
    value_name="score"
)
```

### Frequency tables

```python
pd.crosstab(df["city"], df["category"])
pd.crosstab(df["city"], df["category"], normalize="index")
```

Tidy data usually means one variable per column, one observation per row, and one observational unit per table.

## 16. Window and Ranking Operations

```python
df["rank"] = df["score"].rank(method="dense", ascending=False)
df["running_total"] = df["sales"].cumsum()
df["previous_sales"] = df["sales"].shift(1)
df["change"] = df["sales"].diff()
df["percentage_change"] = df["sales"].pct_change()
df["moving_average"] = df["sales"].rolling(window=7, min_periods=1).mean()
df["expanding_average"] = df["sales"].expanding().mean()
df["ewm_average"] = df["sales"].ewm(span=7, adjust=False).mean()
```

Within groups:

```python
ordered = df.sort_values(["customer_id", "date"])
ordered["previous_order"] = ordered.groupby("customer_id")["amount"].shift(1)
ordered["customer_total"] = ordered.groupby("customer_id")["amount"].cumsum()
```

Always sort by time before time-dependent shifts, differences, and rolling operations.

## 17. MultiIndex

A `MultiIndex` uses multiple levels of labels.

```python
summary = df.groupby(["city", "category"])["revenue"].sum()
summary.loc[("Pune", "Books")]

flat = summary.reset_index(name="revenue")
```

Useful operations:

```python
summary.unstack("category")
wide.stack()
df.set_index(["city", "category"]).sort_index()
```

MultiIndex can express hierarchical data elegantly, but a flat table is often simpler for exporting and machine learning.

## 18. Descriptive Statistics and Relationships

```python
df["sales"].mean()
df["sales"].median()
df["sales"].mode()
df["sales"].quantile([0.25, 0.5, 0.75])
df["sales"].std()
df["sales"].var()
df["sales"].min()
df["sales"].max()
df["sales"].idxmax()       # row label of maximum
```

Correlation:

```python
numeric = df.select_dtypes(include="number")
numeric.corr(method="pearson")
numeric.corr(method="spearman")
```

Correlation describes association, not causation. Pearson correlation focuses on linear relationships and can be strongly influenced by outliers.

## 19. Input, Output, and Large Files

Writing data:

```python
df.to_csv("clean_sales.csv", index=False)
df.to_excel("clean_sales.xlsx", index=False)
df.to_parquet("clean_sales.parquet", index=False)
```

CSV is portable and human-readable but does not preserve types reliably. Parquet is compact, typed, and efficient for analytics.

Process a large CSV in chunks:

```python
totals = []

for chunk in pd.read_csv("large.csv", chunksize=100_000):
    totals.append(chunk.groupby("category")["sales"].sum())

grand_total = pd.concat(totals, axis=1).sum(axis=1)
```

Read only required columns and supply useful dtypes to reduce memory.

## 20. Plotting

pandas plotting uses Matplotlib by default:

```python
import matplotlib.pyplot as plt

df["sales"].plot(kind="hist", bins=20, title="Sales distribution")
plt.xlabel("Sales")
plt.show()

df.groupby("category")["sales"].sum().sort_values().plot(kind="barh")
plt.tight_layout()
plt.show()
```

Use plots to answer a question, not merely decorate a report. Always label axes, show units, and avoid misleading scales.

## 21. A Reusable Cleaning Pipeline

```python
def clean_sales(raw):
    return (
        raw.rename(columns=lambda col: col.strip().lower().replace(" ", "_"))
           .drop_duplicates()
           .assign(
               date=lambda x: pd.to_datetime(x["date"], errors="coerce"),
               quantity=lambda x: pd.to_numeric(x["quantity"], errors="coerce"),
               price=lambda x: pd.to_numeric(x["price"], errors="coerce")
           )
           .dropna(subset=["date", "quantity", "price"])
           .query("quantity >= 0 and price >= 0")
           .assign(revenue=lambda x: x["quantity"] * x["price"])
           .sort_values("date")
           .reset_index(drop=True)
    )

raw = pd.read_csv("sales.csv")
sales = clean_sales(raw)
```

Good pipelines make assumptions visible and repeatable. Add assertions for important invariants:

```python
assert sales["date"].notna().all()
assert sales["quantity"].ge(0).all()
assert sales["revenue"].ge(0).all()
```

## 22. Performance Habits

1. Prefer vectorized column operations over row loops.
2. Avoid repeated `pd.concat` inside a loop; collect frames and concatenate once.
3. Read only needed columns.
4. Use suitable dtypes, including `category` for repeated labels.
5. Filter early when later work only needs a subset.
6. Avoid `iterrows` for calculation-heavy code.
7. Use `itertuples` when iteration is genuinely required.
8. Use Parquet for large typed analytical datasets when available.
9. Profile before optimizing; readability is valuable.

## 23. Common Mistakes and Test Traps

1. **Confusing `loc` and `iloc`**: labels versus integer positions.
2. **Forgetting label slices are inclusive** in `loc`.
3. **Using `and`/`or` in masks** instead of `&`/`|`.
4. **Chained assignment**: use `df.loc[condition, column] = value`.
5. **Ignoring index alignment** during Series arithmetic or column assignment.
6. **Assuming `inplace=True` is always faster** or necessary.
7. **Comparing missing values with equality** instead of `isna`.
8. **Filling or scaling before splitting data** and causing leakage.
9. **Merging without checking key uniqueness**, causing row multiplication.
10. **Using `pivot` when duplicates exist**; use `pivot_table` with an aggregation.
11. **Using `count` when you mean row count**: `count` excludes missing values; `size` counts rows.
12. **Forgetting to sort by time** before `shift`, `diff`, or rolling analysis.
13. **Leaving numeric columns as strings**, producing lexical sorting and invalid calculations.
14. **Dropping outliers automatically** without domain reasoning.
15. **Saving an unwanted index**: use `index=False` for ordinary flat CSV exports.

## 24. Quick Reference

| Goal | pandas expression |
|---|---|
| Read CSV | `pd.read_csv(path)` |
| Inspect | `df.head()`, `df.info()`, `df.describe()` |
| Select column | `df["col"]` |
| Select columns | `df[["a", "b"]]` |
| Label selection | `df.loc[rows, columns]` |
| Position selection | `df.iloc[rows, columns]` |
| Filter | `df[df["x"] > 0]` |
| Missing counts | `df.isna().sum()` |
| Fill missing | `df["x"].fillna(value)` |
| Convert numeric | `pd.to_numeric(s, errors="coerce")` |
| Convert datetime | `pd.to_datetime(s, errors="coerce")` |
| Unique frequencies | `s.value_counts(dropna=False)` |
| Remove duplicates | `df.drop_duplicates()` |
| Sort | `df.sort_values("col")` |
| Group summary | `df.groupby("key").agg(...)` |
| Same-size group result | `groupby(...).transform(...)` |
| Database join | `left.merge(right, on="key", how="left")` |
| Stack tables | `pd.concat(frames, ignore_index=True)` |
| Long to wide | `pivot` / `pivot_table` |
| Wide to long | `melt` |
| Moving calculation | `s.rolling(window).mean()` |
| Write CSV | `df.to_csv(path, index=False)` |

## 25. Practice Questions

1. What is the difference between a Series and a DataFrame?
2. What is the difference between `loc` and `iloc`?
3. Write a filter for rows where age is at least 18 and city is Delhi or Pune.
4. Why is `df[df["x"] > 0]["y"] = 1` unsafe?
5. What is the difference between `groupby().agg()` and `groupby().transform()`?
6. Explain inner, left, and outer joins.
7. Why can a merge unexpectedly increase the number of rows?
8. When should `pivot_table` be used instead of `pivot`?
9. What is the difference between group `size` and `count`?
10. How do you convert invalid numeric text to missing values?
11. Why should imputation usually be learned only from training data?
12. What makes a dataset tidy?

### Answers

1. A Series is one-dimensional with one values array and an index; a DataFrame is a two-dimensional collection of aligned columns.
2. `loc` uses labels and inclusive label slices; `iloc` uses zero-based positions and exclusive stop positions.
3. `df[(df["age"] >= 18) & (df["city"].isin(["Delhi", "Pune"]))]`.
4. It can operate on a temporary object; use `df.loc[df["x"] > 0, "y"] = 1`.
5. `agg` reduces groups to summaries; `transform` returns a value aligned to every original row.
6. Inner keeps matched keys, left keeps every left row, and outer keeps all keys from both.
7. Duplicate keys create multiple matches, potentially a many-to-many Cartesian multiplication within each key.
8. Use `pivot_table` when index/column pairs repeat and must be aggregated.
9. `size` counts rows; `count` counts non-missing values in the selected column(s).
10. `pd.to_numeric(series, errors="coerce")`.
11. Using full-data statistics exposes information from validation/test data and gives an overly optimistic evaluation.
12. Each variable is a column, each observation is a row, and each observational unit has its own table.

## 26. Final Revision Checklist

Before a test, ensure you can:

- Create and inspect Series and DataFrames
- Load CSV, Excel, JSON, and Parquet conceptually
- Select with brackets, `loc`, and `iloc`
- Filter and assign safely with boolean masks
- Explain index alignment
- Clean missing values, duplicates, types, text, and dates
- Use `groupby` with `agg`, `transform`, and `filter`
- Explain `concat`, `merge`, and join types
- Reshape with `pivot`, `pivot_table`, and `melt`
- Use sorting, ranking, rolling, shifting, and cumulative operations
- Write a reproducible cleaning method chain
- Recognize leakage, merge multiplication, and chained assignment

The most valuable practice is to take a small messy CSV and produce a clean summary table while explaining every choice.
