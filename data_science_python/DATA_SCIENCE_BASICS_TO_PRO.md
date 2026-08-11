# Data Science: Basics to Pro Study Guide

Data science is the disciplined process of turning data into reliable understanding, decisions, or predictions. It combines programming, statistics, domain knowledge, communication, and engineering. A sophisticated model cannot rescue a poorly defined question or unreliable data.

This guide gives you a complete learning path and a revision reference. Use the NumPy and pandas study guides in this folder for deeper library syntax.

## 1. The Big Picture

A typical data science workflow is iterative:

```text
Question -> Data -> Validation -> Exploration -> Preparation
         -> Model/Analysis -> Evaluation -> Communication
         -> Deployment -> Monitoring -> New questions
```

Not every project needs machine learning. Sometimes a group-by table, confidence interval, experiment, or dashboard answers the question better.

### Main types of data work

- **Descriptive:** What happened?
- **Diagnostic:** Why did it happen?
- **Predictive:** What is likely to happen?
- **Prescriptive:** What action should be taken?
- **Causal:** What would happen if we changed something?

Prediction and causation are not the same. A variable can predict an outcome without causing it.

## 2. Start With the Problem, Not the Algorithm

Translate a vague request into a precise analytical problem.

Example vague request: “Reduce customer churn.”

A better specification:

- **Population:** active monthly subscribers
- **Unit of analysis:** one customer at a defined prediction date
- **Target:** cancellation within the next 30 days
- **Features:** only information available on the prediction date
- **Action:** retention offer for high-risk customers
- **Metric:** recall among the top 10% highest-risk customers, plus campaign profit
- **Constraints:** offer capacity, privacy, fairness, inference speed
- **Baseline:** current rule or overall churn rate

Before modeling, ask:

1. Who will use the result?
2. What decision will it change?
3. What is one row in the dataset?
4. When is the prediction made?
5. What outcome and time window define success?
6. Which mistakes cost more?
7. What data is actually available at decision time?
8. What simple baseline must the solution beat?

## 3. Essential Python Skills

You should be comfortable with:

- Variables and scalar types: `int`, `float`, `bool`, `str`, `None`
- Collections: list, tuple, dictionary, set
- Indexing, slicing, iteration, comprehensions
- Conditions and loops
- Functions, parameters, return values, scope
- Exceptions and input validation
- Modules and virtual environments
- Reading files and working with paths
- NumPy arrays and pandas DataFrames
- Basic plotting
- Writing reusable, tested code

Example function:

```python
def safe_mean(values):
    """Return the mean of non-missing values, or None if none remain."""
    clean = [value for value in values if value is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)
```

Good habits:

- Give variables meaningful names.
- Put repeated logic in functions.
- Keep raw data unchanged.
- Make randomness reproducible with seeds.
- Use assertions and tests for assumptions.
- Record environments and package versions for projects.

## 4. Data Structures and File Formats

### Common data structures

- **Tabular:** rows and columns, such as orders or patients
- **Time series:** measurements ordered in time
- **Text:** documents, messages, reviews
- **Images/audio/video:** high-dimensional unstructured signals
- **Graph:** nodes and relationships, such as users and friendships
- **Geospatial:** locations, paths, and regions

### Common formats

| Format | Strength | Limitation |
|---|---|---|
| CSV/TSV | Universal and readable | Types and metadata are weak |
| Excel | Familiar and supports sheets | Manual edits and mixed types can be risky |
| JSON | Flexible nested records | Verbose and schema can vary |
| Parquet | Typed, compressed, columnar | Less human-readable |
| SQL table | Queryable, governed, relational | Requires database access and query skills |
| NumPy `.npy/.npz` | Efficient numeric arrays | Not ideal for mixed-type tables |

Never assume a file is correct because it loads successfully. Validate schema, row uniqueness, types, ranges, units, and missingness.

## 5. NumPy, pandas, Visualization, and SQL

### NumPy

Use NumPy for homogeneous numeric arrays, fast vectorized computation, broadcasting, random sampling, and linear algebra.

### pandas

Use pandas for labeled tables, mixed column types, missing-data handling, grouping, joining, reshaping, dates, and file I/O.

### Visualization

Common Python libraries include Matplotlib and seaborn. Match plot to question:

| Question | Useful plot |
|---|---|
| Distribution of one numeric variable | Histogram, density plot, box plot |
| Counts across categories | Ordered bar chart |
| Relationship of two numeric variables | Scatter plot |
| Numeric value across categories | Box/violin/strip plot |
| Change over time | Line plot |
| Two categorical variables | Grouped/stacked bars or heatmap |
| Many numeric relationships | Correlation heatmap or pair plot, used carefully |

Avoid 3-D charts, decorative clutter, truncated axes that exaggerate differences, and rainbow palettes without meaning.

### SQL essentials

Data scientists commonly need:

- `SELECT`, aliases, expressions
- `WHERE`, `IN`, `BETWEEN`, `LIKE`, null handling
- `GROUP BY`, `HAVING`, aggregates
- `INNER`, `LEFT`, `RIGHT`, and `FULL` joins
- Common table expressions (`WITH`)
- Subqueries
- Window functions such as `ROW_NUMBER`, `LAG`, running totals
- Date operations
- Understanding primary and foreign keys

Conceptual example:

```sql
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM orders
WHERE order_date >= '2026-01-01'
GROUP BY customer_id
HAVING COUNT(*) >= 3;
```

SQL aggregation changes row granularity. Always know what one output row represents.

## 6. Mathematics You Need

### Linear algebra

Learn these ideas:

- Scalars, vectors, matrices, tensors
- Vector length and dot product
- Matrix multiplication
- Transpose, inverse, rank
- Linear independence
- Eigenvalues and eigenvectors
- Singular value decomposition (SVD)

For vectors \(x\) and \(w\), a linear model uses a dot product:

\[
\hat{y} = w^T x + b
\]

Matrix multiplication is central because it applies many weighted sums efficiently.

### Calculus

Focus on:

- Function, slope, derivative, partial derivative
- Gradient: vector of partial derivatives
- Chain rule
- Minimum and maximum
- Gradient descent

Basic gradient descent update:

\[
\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)
\]

where \(\theta\) contains parameters, \(L\) is the loss, and \(\eta\) is the learning rate.

If the learning rate is too small, learning is slow. If too large, optimization may overshoot or diverge.

### Probability

Know:

- Sample space and events
- Conditional probability
- Independence
- Bayes' theorem
- Random variables
- Expected value and variance
- Common distributions

Conditional probability:

\[
P(A \mid B) = \frac{P(A \cap B)}{P(B)}
\]

Bayes' theorem:

\[
P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}
\]

Common distributions:

- **Bernoulli:** one binary trial
- **Binomial:** number of successes in fixed independent Bernoulli trials
- **Normal:** symmetric continuous distribution described by mean and variance
- **Poisson:** event count in a fixed interval under assumptions
- **Uniform:** equal density over a range
- **Exponential:** time between Poisson-process events

## 7. Descriptive Statistics

### Center

- Mean: \(\bar{x} = \frac{1}{n}\sum x_i\)
- Median: middle ordered value; robust to extreme outliers
- Mode: most frequent value

### Spread

- Range: maximum minus minimum
- Interquartile range: \(IQR = Q_3 - Q_1\)
- Population variance: \(\sigma^2 = \frac{1}{N}\sum(x_i-\mu)^2\)
- Sample variance: \(s^2 = \frac{1}{n-1}\sum(x_i-\bar{x})^2\)
- Standard deviation: square root of variance

The `n - 1` denominator corrects bias when estimating population variance from a sample.

### Position and shape

- Percentile: value below which a percentage of observations fall
- Z-score: \(z = \frac{x-\mu}{\sigma}\)
- Skewness: asymmetry
- Kurtosis: tail/extreme-value behavior, depending on definition

Mean and standard deviation are informative for roughly symmetric data. Median and IQR are often better for skewed data.

## 8. Statistical Inference

### Population, sample, parameter, statistic

- A **population** is the complete group of interest.
- A **sample** is the observed subset.
- A **parameter** describes the population.
- A **statistic** is calculated from a sample.

Representative sampling matters more than merely having a large dataset. A huge biased sample remains biased.

### Sampling distributions and standard error

A sampling distribution describes how a statistic would vary over repeated samples. The standard error measures the variability of that statistic.

For an independent sample mean:

\[
SE(\bar{x}) = \frac{s}{\sqrt{n}}
\]

### Confidence intervals

A common approximate form is:

\[
\text{estimate} \pm \text{critical value} \times SE
\]

A 95% confidence procedure produces intervals that would contain the true parameter in about 95% of repeated samples under its assumptions. It does not mean a fixed parameter has a 95% probability of being inside one already-computed frequentist interval.

### Hypothesis testing

1. State null and alternative hypotheses.
2. Choose a test and significance level before seeing the result.
3. Check assumptions.
4. Compute a test statistic and p-value.
5. Interpret alongside effect size and uncertainty.

A p-value is the probability, assuming the null and model assumptions, of obtaining a result at least as incompatible with the null as the observed result. It is not the probability that the null hypothesis is true.

Statistical significance does not guarantee practical importance. Report effect size and confidence interval.

### Common tests

- One-sample or two-sample t-test for means under assumptions
- Paired t-test for paired numeric measurements
- Chi-square test for categorical association/counts
- ANOVA for comparing several group means
- Mann-Whitney U or Wilcoxon methods as rank-based alternatives
- Permutation tests for fewer distributional assumptions

Multiple testing increases false positives. Use a planned hypothesis set or adjustments when appropriate.

## 9. Correlation, Confounding, and Causality

### Correlation

- Pearson measures linear association.
- Spearman measures monotonic rank association.
- Values near zero do not rule out nonlinear relationships.
- Outliers can distort correlations.

Correlation does not imply causation because of:

- Confounding variables
- Reverse causality
- Selection bias
- Coincidence/multiple comparisons
- Measurement issues

### Causal thinking

To estimate an intervention effect, ask what would happen to the same unit both with and without treatment—the unobservable counterfactual problem.

Randomized experiments make treatment groups comparable on average and are often the strongest design. Observational causal inference needs explicit assumptions and methods such as matching, weighting, regression adjustment, instrumental variables, regression discontinuity, or difference-in-differences.

Predictive feature importance is not automatically a causal effect.

## 10. Data Collection and Quality

### Sources of bad data

- Manual entry errors
- Sensor or logging failures
- Duplicate events
- Changing definitions
- Unit mismatch
- Time-zone mismatch
- Biased sampling
- Survivorship bias
- Labels produced inconsistently
- Data joined at the wrong granularity
- Information unavailable at prediction time

### A practical validation checklist

```python
required = {"customer_id", "date", "amount"}
assert required.issubset(df.columns)
assert df["customer_id"].notna().all()
assert df["amount"].ge(0).all()
assert not df.duplicated(["customer_id", "date"]).any()
```

In production, use explicit validation reports instead of relying only on assertions, which can be disabled.

Track:

- Expected schema and types
- Allowed categories
- Numeric ranges and units
- Primary-key uniqueness
- Referential integrity
- Missing-rate thresholds
- Time coverage and freshness
- Distribution changes

## 11. Exploratory Data Analysis (EDA)

EDA is structured investigation, not random chart generation.

### Step 1: Understand structure

```python
df.shape
df.info()
df.head()
df.sample(5, random_state=42)
```

### Step 2: Audit quality

```python
df.isna().mean().sort_values(ascending=False)
df.duplicated().sum()
df.nunique().sort_values()
```

### Step 3: Univariate analysis

- Numeric: center, spread, quantiles, histogram, suspicious limits
- Categorical: frequency, rare levels, inconsistent labels
- Datetime: range, gaps, frequency, seasonality
- Text: length, missingness, language, repeated templates

### Step 4: Bivariate and multivariate analysis

- Feature versus target
- Numeric-numeric scatter/correlation
- Category-numeric grouped summaries
- Category-category contingency tables
- Segmentation by meaningful domain groups
- Interactions and nonlinear patterns

### Step 5: Write findings

Record:

- What was checked
- What was found
- What might explain it
- What needs domain confirmation
- What action will be taken

Never silently “fix” suspicious data during EDA. Preserve a clear transformation record.

## 12. Cleaning and Preprocessing

### Missing values

Possible actions:

- Correct upstream collection
- Drop rows/columns when justified
- Fill with a constant, median, mode, or learned model
- Add a missingness indicator
- Use an algorithm that supports missing values

The reason for missingness matters:

- **MCAR:** unrelated to observed and unobserved data
- **MAR:** related to observed data
- **MNAR:** related to the missing value or unobserved causes

### Duplicates

Define duplicates using the real-world entity and event, not just every column. Two identical purchases may be genuine; repeated event IDs may not be.

### Outliers

Detection methods:

- Domain bounds
- IQR rule: below \(Q_1 - 1.5 IQR\) or above \(Q_3 + 1.5 IQR\)
- Z-scores for suitable distributions
- Robust or model-based detection

Possible treatments:

- Correct errors
- Keep genuine extremes
- Transform skewed values
- Cap/winsorize with justification
- Use robust metrics or models
- Model distinct segments separately

### Categorical encoding

- One-hot encoding for unordered categories
- Ordinal encoding only when real order exists
- Frequency encoding in some cases
- Target encoding with careful out-of-fold computation to prevent leakage
- Hashing or learned embeddings for very high cardinality

### Numeric scaling

Standardization:

\[
z = \frac{x-\mu}{\sigma}
\]

Min-max scaling:

\[
x' = \frac{x-x_{min}}{x_{max}-x_{min}}
\]

Scaling is important for distance-based methods, gradient-based methods, PCA, regularized linear models, and neural networks. Decision trees usually do not require it.

Fit preprocessing on training data only, then apply the fitted transformation to validation, test, and future data.

## 13. Feature Engineering

A feature is model input derived from information available at prediction time.

Examples:

- Date: day of week, month, holiday, elapsed time
- Customer: order count in prior 30 days, average historical spend
- Numeric: ratios, differences, log transforms, interactions
- Category: rare-level grouping, one-hot encoding
- Text: length, term frequencies, embeddings
- Location: distance, region, density
- Time series: lags and rolling statistics using only past values

Good features encode relevant domain structure. More features are not always better; they can add noise, cost, instability, and leakage.

### Leakage

Data leakage means training uses information that would not be legitimately available at prediction time.

Examples:

- A “cancellation reason” column used to predict cancellation
- Filling values using the full dataset before splitting
- Target encoding calculated on the same rows' targets
- Randomly splitting repeated measurements of the same person across train and test
- Using future values in a time-series rolling feature

Leakage creates impressive validation scores and disappointing real-world performance.

## 14. Train, Validation, and Test Sets

- **Training set:** fit model parameters and preprocessing.
- **Validation set:** select features, algorithms, and hyperparameters.
- **Test set:** final unbiased estimate, used only after choices are fixed.

Common splits:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

Use a split strategy matching deployment:

- Random split for independent, identically distributed rows
- Stratified split to preserve class proportions
- Group split when rows from one person/device/entity must remain together
- Time split when predicting the future from the past

A random split is incorrect when it lets near-duplicates, future information, or the same group appear in both sets.

### Cross-validation

K-fold cross-validation divides training data into K folds, fits on K-1, validates on the remaining fold, and rotates.

Use variants appropriate to the problem:

- `KFold`
- `StratifiedKFold`
- `GroupKFold`
- `TimeSeriesSplit`

Cross-validation estimates variability and uses limited training data efficiently, but it does not repair an invalid splitting design.

## 15. Baselines

Always create a simple reference:

- Regression: predict training mean or median
- Classification: majority class, class frequency, or a business rule
- Time series: last value or seasonal naive value
- Ranking: existing rule or random ordering

A complex model that does not beat a relevant baseline is not useful. A baseline also catches broken metrics and leakage.

## 16. Supervised Learning

Supervised learning maps features \(X\) to known targets \(y\).

### Regression

Predicts a numeric value, such as price, demand, or duration.

#### Linear regression

\[
\hat{y} = \beta_0 + \beta_1x_1 + \cdots + \beta_px_p
\]

Ordinary least squares minimizes sum of squared residuals. Useful assumptions for inference include linearity, independent errors, appropriate variance behavior, and limited harmful collinearity. Prediction may still work when inferential assumptions are imperfect, but validation remains essential.

#### Regularization

- Ridge (L2): shrinks coefficients; usually keeps all features
- Lasso (L1): can make coefficients exactly zero
- Elastic Net: combines L1 and L2

Regularization reduces variance and helps with correlated/high-dimensional features. Scaling is generally needed so penalties treat features comparably.

#### Tree-based regression

- Decision tree: interpretable rules but can overfit
- Random forest: averages many decorrelated trees, reducing variance
- Gradient boosting: sequentially corrects errors; often strong on tabular data

Tree ensembles capture nonlinearities and interactions with little preprocessing, but must still be tuned and validated.

### Classification

Predicts a category, such as spam/not spam or a disease class.

#### Logistic regression

For binary classification:

\[
P(y=1 \mid x) = \sigma(\beta_0 + \beta^Tx)
\]

where

\[
\sigma(z)=\frac{1}{1+e^{-z}}
\]

Logistic regression is a linear model for log-odds. It produces probabilities and is a strong interpretable baseline.

#### K-nearest neighbors

Predicts using nearby training points. It is intuitive but sensitive to scale, irrelevant dimensions, the value of K, and dataset size.

#### Support vector machine

Finds a separating margin; kernels can model nonlinear boundaries. Scaling matters. Large datasets and probability calibration may require care.

#### Naive Bayes

Uses Bayes' theorem with conditional-independence assumptions. Often fast and effective for text/count features despite simplified assumptions.

#### Trees and ensembles

Decision trees split features into regions. Random forests use bagging; boosting methods build learners sequentially. They are strong for tabular data but are not automatically immune to overfitting or leakage.

## 17. Bias, Variance, Underfitting, and Overfitting

- **High bias / underfitting:** model too simple; poor training and validation performance.
- **High variance / overfitting:** model memorizes training details; good training but poor validation performance.

Ways to reduce underfitting:

- Add relevant features or interactions
- Use a more flexible model
- Reduce excessive regularization
- Train/optimize appropriately

Ways to reduce overfitting:

- Get more representative data
- Simplify the model
- Increase regularization
- Remove noisy features
- Use pruning, early stopping, or dropout where applicable
- Tune with proper cross-validation

The objective is not perfect training performance; it is reliable generalization.

## 18. Evaluation Metrics

Choose metrics according to the business decision and error cost.

### Regression metrics

Mean absolute error:

\[
MAE = \frac{1}{n}\sum |y_i-\hat{y}_i|
\]

- Same unit as target
- Relatively robust to extreme errors

Mean squared error and root mean squared error:

\[
MSE = \frac{1}{n}\sum(y_i-\hat{y}_i)^2
\]

\[
RMSE = \sqrt{MSE}
\]

- Penalize large errors strongly
- RMSE has target units

Coefficient of determination:

\[
R^2 = 1 - \frac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}
\]

`R² = 1` is perfect; `0` matches the mean baseline on that data; it can be negative on test data.

Percentage errors such as MAPE are problematic when actual values are zero or near zero.

### Classification confusion matrix

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive | True positive (TP) | False negative (FN) |
| Actual negative | False positive (FP) | True negative (TN) |

Metrics:

\[
Accuracy = \frac{TP+TN}{TP+TN+FP+FN}
\]

\[
Precision = \frac{TP}{TP+FP}
\]

\[
Recall = \frac{TP}{TP+FN}
\]

\[
F1 = 2\frac{Precision \cdot Recall}{Precision+Recall}
\]

- Precision asks: among predicted positives, how many were correct?
- Recall asks: among actual positives, how many were found?
- Specificity is `TN / (TN + FP)`.

Accuracy can be misleading with imbalance. If only 1% of cases are positive, predicting “negative” always gives 99% accuracy and zero recall.

### Threshold-free and ranking metrics

- ROC AUC: ranking quality across false-positive/true-positive rates
- PR AUC: precision-recall tradeoff; often more informative for rare positives
- Log loss: rewards well-calibrated probabilities and heavily penalizes confident wrong predictions

Choose a probability threshold based on costs and capacity, not automatically `0.5`.

### Calibration

A calibrated model predicting 0.8 should be correct about 80% of the time among cases receiving that probability. A model can rank well but be poorly calibrated.

## 19. Imbalanced Classification

For rare outcomes:

- Use stratified splits where appropriate.
- Evaluate precision, recall, PR curves, and cost-based metrics.
- Tune the decision threshold.
- Try class weights.
- Consider over/under-sampling only inside training folds.
- Inspect performance across important subgroups.
- Collect better positive examples if possible.

Never resample before the split; synthetic or duplicated examples could leak into validation/test data.

## 20. Preprocessing Pipelines

A pipeline keeps transformations tied to model fitting and prevents many leakage errors.

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric_features = ["age", "income"]
categorical_features = ["city", "plan"]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocess = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)
probabilities = model.predict_proba(X_test)[:, 1]
```

Because the transformer is inside the pipeline, cross-validation learns imputation, scaling, and encoding separately within each training fold.

## 21. Hyperparameter Tuning

Parameters are learned from data; hyperparameters are chosen by the practitioner.

Examples:

- Tree depth
- Number of trees
- Regularization strength
- Number of neighbors
- Learning rate

Search methods:

- Grid search: tries every specified combination
- Random search: samples combinations, often more efficient in large spaces
- Bayesian/sequential optimization: chooses later trials using previous results

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(
    model,
    param_grid={"classifier__C": [0.01, 0.1, 1, 10]},
    scoring="roc_auc",
    cv=5,
    n_jobs=-1
)
search.fit(X_train, y_train)
best_model = search.best_estimator_
```

Do not tune on the final test set. Every decision made after seeing test performance weakens its independence.

## 22. Model Interpretation

Interpretation questions include:

- What does the model use?
- In which direction does a feature affect predictions?
- Why did one case receive this prediction?
- Where does the model fail?
- Is behavior stable across subgroups and time?

Tools:

- Linear/logistic coefficients, after considering scale and correlation
- Tree structure for small trees
- Permutation importance on held-out data
- Partial dependence and individual conditional expectation
- SHAP-style contribution explanations
- Counterfactual or example-based explanations

Warnings:

- Importance is not causality.
- Correlated features can share or exchange importance.
- Explanations describe the fitted model, not necessarily reality.
- Global and local explanations answer different questions.

Error analysis is often more useful than a single importance chart. Inspect false positives, false negatives, largest residuals, segments, and time periods.

## 23. Unsupervised Learning

Unsupervised methods learn structure without labeled targets.

### Clustering

#### K-means

Assigns points to K centers to minimize within-cluster squared distance.

Strengths: simple, fast, interpretable centers.

Limitations: requires K, sensitive to scale/outliers/initialization, favors roughly compact spherical clusters.

#### Hierarchical clustering

Builds a tree of nested clusters. Useful for exploration and smaller datasets; distance and linkage choices matter.

#### DBSCAN

Groups dense regions and labels isolated points as noise. It can find irregular shapes and does not require K, but density varies poorly across some datasets and scale matters.

Cluster labels have no automatic real-world meaning. Validate stability, separation, business usefulness, and external evidence.

### Dimensionality reduction

#### PCA

Principal component analysis finds orthogonal directions of maximum variance.

Uses:

- Compression
- Noise reduction
- Visualization
- Reducing correlated numeric dimensions

Standardize features first when their units/scales differ. PCA components are combinations of original features and may be hard to interpret.

#### t-SNE and UMAP-style methods

Useful for visualizing local high-dimensional structure. Two-dimensional distances and cluster sizes can be misleading; do not treat the plot as definitive proof of clusters.

## 24. Time Series Fundamentals

Time series violate ordinary random-split assumptions because order matters.

Components:

- Trend
- Seasonality
- Cycles
- Noise
- Structural breaks

Features:

- Lags: previous observations
- Rolling mean/std/min/max
- Calendar features
- Expanding statistics
- External variables known at forecast time

Evaluation:

- Train on past, validate on later periods
- Use walk-forward/backtesting splits
- Compare with naive and seasonal-naive baselines
- Avoid features that use future values

Stationarity means relevant statistical properties remain stable over time. Differencing and transformations can help some classical models, but every method has assumptions.

Watch for concept drift, holidays, policy changes, stockouts, and delayed labels.

## 25. Text Data Fundamentals

A basic natural-language processing pipeline:

1. Define unit: document, sentence, message, or token.
2. Normalize only as appropriate for the task.
3. Split data before learning vocabulary.
4. Convert text to features.
5. Train and evaluate using suitable metrics.

Representations:

- Bag of words: token counts
- TF-IDF: emphasizes informative terms
- N-grams: short token sequences
- Embeddings: dense semantic representations
- Transformer-based representations/models: contextual language features

Be careful: punctuation, capitalization, emojis, and misspellings may carry signal. Text can contain private information, demographic proxies, label leakage, and rapidly changing language.

## 26. Deep Learning Overview

A neural network stacks layers of weighted transformations and nonlinear activations.

Core concepts:

- Input, hidden, and output layers
- Weights and biases
- Activation functions such as ReLU or sigmoid
- Forward pass
- Loss function
- Backpropagation using the chain rule
- Mini-batch gradient optimization
- Epochs and learning rates
- Regularization, dropout, normalization, early stopping

Deep learning is powerful for images, text, audio, and very large/complex datasets. For ordinary medium-sized tabular data, tree ensembles and well-built linear baselines are often competitive and easier to operate.

## 27. Experimentation and A/B Testing

An A/B test randomly assigns eligible units to variants and compares outcomes.

Plan before launch:

- Primary metric
- Guardrail metrics
- Eligibility and randomization unit
- Minimum detectable effect
- Significance level and power
- Sample size and duration
- Data quality checks
- Stopping rule

Common pitfalls:

- Peeking repeatedly and stopping when significant
- Changing metrics after seeing results
- Sample ratio mismatch
- Users exposed to multiple variants
- Novelty effects
- Network/interference effects
- Running during an unrepresentative period
- Focusing on significance but ignoring effect size

Report the estimated effect, uncertainty interval, data-quality checks, and practical impact.

## 28. Deployment and MLOps

A model is useful only when integrated into a reliable decision process.

### Deployment modes

- Batch: scheduled predictions for many records
- Online API: low-latency prediction per request
- Streaming: continual event processing
- Embedded/on-device: local inference

### Artifacts to version

- Code and configuration
- Data/schema references
- Train/validation/test definition
- Feature logic
- Fitted preprocessing and model
- Package environment
- Metrics and decision threshold
- Model documentation and owner

### Monitoring

Monitor:

- Service health: latency, errors, throughput
- Data quality: missingness, schema, freshness, range
- Data drift: input distribution change
- Prediction drift: output distribution change
- Concept drift: relationship between inputs and outcome changes
- Performance once labels arrive
- Calibration and subgroup performance
- Business outcomes and action rates

Drift is a warning, not automatic proof that performance has declined. Define alert thresholds and response procedures.

## 29. Reproducibility and Project Structure

A practical small-project layout:

```text
project/
├── README.md
├── pyproject.toml or requirements.txt
├── data/
│   ├── raw/            # never manually edit
│   └── processed/      # reproducible outputs
├── notebooks/          # exploration and communication
├── src/                # reusable code
├── tests/
├── models/
└── reports/
```

Reproducibility checklist:

- Raw inputs are immutable.
- Transformations are scripted.
- Random seeds are controlled where possible.
- Dependencies are recorded.
- Code and configurations are versioned.
- Data definitions and units are documented.
- The final result can be rebuilt from a clean environment.
- Tests cover critical feature and metric logic.

Notebooks are excellent for exploration. Move stable logic into functions/modules so it can be tested and reused.

## 30. Ethics, Privacy, Security, and Fairness

Ask throughout the project:

- Is collection legal, expected, and necessary?
- Can less sensitive data solve the problem?
- Who might be harmed by errors?
- Are labels biased or incomplete?
- Are protected traits or proxies involved?
- Does performance differ across relevant groups?
- Can a person contest or understand a consequential result?
- How long is data retained, and who can access it?
- Can outputs expose private training records?

Fairness metrics can conflict; there is no single mathematical definition suitable for every context. The right choice depends on the decision, harms, legal setting, and stakeholder input.

Use data minimization, access controls, secure storage, auditing, retention limits, and human oversight proportionate to risk.

## 31. Communication and Data Storytelling

A good data science result answers:

1. What question did we ask?
2. What data and assumptions did we use?
3. What did we find?
4. How certain are we?
5. What decision follows?
6. What are the limitations and risks?

Lead with the conclusion, support it with the smallest sufficient evidence, and make uncertainty visible. Separate observed facts, interpretations, and recommendations.

For charts:

- Write a takeaway title.
- Label axes and units.
- Use consistent scales and ordering.
- Highlight the comparison that matters.
- Include source, timeframe, and definition notes.
- Do not hide inconvenient segments or uncertainty.

## 32. End-to-End Classification Template

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. Load and validate
df = pd.read_csv("customers.csv")
required = {"age", "income", "city", "plan", "churned"}
if not required.issubset(df.columns):
    raise ValueError(f"Missing columns: {required - set(df.columns)}")

# 2. Define features and target
X = df[["age", "income", "city", "plan"]]
y = df["churned"]

# 3. Split before learned preprocessing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Preprocessing
numeric = ["age", "income"]
categorical = ["city", "plan"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]), numeric),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical)
])

# 5. Model
model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# 6. Fit and evaluate
model.fit(X_train, y_train)
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.5).astype(int)

print("ROC AUC:", roc_auc_score(y_test, probability))
print(classification_report(y_test, prediction))
```

For a real project, add a baseline, cross-validation, threshold selection based on cost, subgroup/error analysis, model persistence, data validation, and monitoring.

## 33. A Professional Project Checklist

### Problem

- [ ] Decision, user, prediction time, and success metric are explicit.
- [ ] False-positive and false-negative costs are understood.
- [ ] A simple baseline exists.

### Data

- [ ] One-row meaning and keys are documented.
- [ ] Schema, types, ranges, missingness, and duplicates are checked.
- [ ] Labels are valid and available for the intended prediction horizon.
- [ ] Privacy, consent, licensing, and retention are considered.

### Evaluation

- [ ] Split reflects deployment, groups, and time.
- [ ] Preprocessing is learned inside training folds.
- [ ] Metric matches the real decision.
- [ ] Uncertainty, segments, calibration, and error cases are inspected.
- [ ] Final test data has not guided tuning.

### Delivery

- [ ] Code and dependencies are reproducible.
- [ ] Feature/model artifacts are versioned.
- [ ] Input validation and failure behavior exist.
- [ ] Monitoring and ownership are defined.
- [ ] Findings, limitations, and risks are communicated.

## 34. Common Interview and Exam Questions

### What is the difference between supervised and unsupervised learning?

Supervised learning uses labeled targets to learn prediction. Unsupervised learning looks for structure without a target, such as clusters or lower-dimensional representations.

### What is overfitting?

Overfitting occurs when a model learns training-specific noise and performs much worse on unseen data. It is diagnosed using held-out validation, not training performance alone.

### Why split before preprocessing?

Statistics such as means, category vocabularies, and scaling limits must be learned only from training data. Using the full dataset leaks information and biases evaluation.

### Precision or recall?

Choose based on costs. Emphasize precision when false positives are expensive; emphasize recall when missing positives is expensive. Often the final choice uses a threshold and a cost/capacity calculation.

### Bagging versus boosting?

Bagging trains multiple learners largely independently and combines them, mainly reducing variance. Boosting trains learners sequentially to correct prior errors, often reducing bias while requiring careful regularization.

### Parameter versus hyperparameter?

A parameter is learned during fitting, such as a regression coefficient. A hyperparameter is configured or tuned, such as tree depth or regularization strength.

### Classification versus regression?

Classification predicts discrete categories or their probabilities. Regression predicts numeric quantities.

### Why can accuracy be misleading?

With imbalanced outcomes, a model can achieve high accuracy by always predicting the majority class while completely failing on the important minority class.

### Correlation versus causation?

Correlation describes association. Causation claims that intervening on one variable changes another and requires design/assumptions that address confounding and alternatives.

### What is the bias-variance tradeoff?

Very simple models may have systematic error (bias); highly flexible models may vary too much with the training sample (variance). Model selection balances both for minimum unseen-data error.

### Why use cross-validation?

It estimates performance variability across multiple training/validation partitions and helps choose models with limited data. The cross-validation design must still respect time and group structure.

### What is regularization?

Regularization penalizes model complexity to reduce overfitting. L1 can create sparse coefficients; L2 shrinks coefficients smoothly.

### What is data leakage?

Leakage occurs when training receives information not legitimately available when predictions will be made, causing overly optimistic evaluation.

### What is concept drift?

Concept drift means the relationship between inputs and outcome changes. It differs from data drift, which is a change in the input distribution.

## 35. Formula Sheet

| Concept | Formula |
|---|---|
| Mean | \(\bar{x}=\frac{1}{n}\sum x_i\) |
| Sample variance | \(s^2=\frac{1}{n-1}\sum(x_i-\bar{x})^2\) |
| Z-score | \(z=\frac{x-\mu}{\sigma}\) |
| Conditional probability | \(P(A\mid B)=\frac{P(A\cap B)}{P(B)}\) |
| Bayes' theorem | \(P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}\) |
| Linear prediction | \(\hat{y}=w^Tx+b\) |
| Sigmoid | \(\sigma(z)=\frac{1}{1+e^{-z}}\) |
| Gradient descent | \(\theta_{t+1}=\theta_t-\eta\nabla L(\theta_t)\) |
| MAE | \(\frac{1}{n}\sum|y_i-\hat{y}_i|\) |
| MSE | \(\frac{1}{n}\sum(y_i-\hat{y}_i)^2\) |
| Precision | \(TP/(TP+FP)\) |
| Recall | \(TP/(TP+FN)\) |
| Specificity | \(TN/(TN+FP)\) |
| F1 | \(2PR/(P+R)\) |

## 36. Recommended Learning Order

### Stage 1: Foundations

1. Python collections, functions, files, and errors
2. NumPy arrays, indexing, axes, vectorization, broadcasting
3. pandas selection, cleaning, groupby, merge, reshape
4. Basic SQL
5. Descriptive statistics and plotting

### Stage 2: Reliable analysis

1. Probability and statistical inference
2. EDA and data-quality validation
3. Problem definition and metric selection
4. Train/validation/test design
5. Linear and logistic regression
6. Trees and ensemble methods

### Stage 3: Strong modeling

1. Pipelines and cross-validation
2. Feature engineering and leakage prevention
3. Imbalanced learning and threshold selection
4. Hyperparameter tuning
5. Interpretation and error analysis
6. Unsupervised learning and time series fundamentals

### Stage 4: Professional practice

1. Reproducible project structure and testing
2. Experimentation and causal thinking
3. Deployment and monitoring
4. Privacy, security, fairness, and documentation
5. Clear written and visual communication

## 37. Practice Tasks

Complete these in order:

1. Load a CSV, report its schema, missingness, duplicates, and suspicious ranges.
2. Clean column names, types, missing values, and inconsistent categories in a function.
3. Produce five useful grouped summaries and three purposeful plots.
4. Join two tables while validating key relationships and row counts.
5. Define a prediction target, prediction time, features, and leakage risks.
6. Create a baseline and a valid train/test split.
7. Build a preprocessing/model pipeline.
8. Evaluate with a metric appropriate to error costs.
9. Perform cross-validation and small hyperparameter search.
10. Analyze errors and subgroup performance.
11. Write a one-page result with limitations and recommendation.
12. Describe how the solution would be monitored after deployment.

## 38. Night-Before-Test Revision

If time is short, know these points cold:

- NumPy arrays are homogeneous; pandas DataFrames are labeled tables with one dtype per column.
- In NumPy matrix reductions, `axis=0` collapses rows and `axis=1` collapses columns.
- pandas `loc` uses labels; `iloc` uses positions.
- A statistic summarizes a sample; a parameter describes a population.
- Standard deviation describes data spread; standard error describes estimator uncertainty.
- A p-value is not the probability that the null hypothesis is true.
- Correlation is not causation.
- Fit preprocessing only on training data.
- Validation guides choices; the test set is for final evaluation.
- Use time/group-aware splitting when rows are dependent.
- Always compare with a baseline.
- Overfitting means good training performance but weak unseen-data performance.
- Scaling matters for distance-, gradient-, PCA-, and regularization-based methods; trees usually do not require it.
- Precision penalizes false positives; recall penalizes false negatives.
- Accuracy may hide failure on an imbalanced minority class.
- `R²` can be negative on unseen data.
- Regularization controls complexity; L1 can produce zero coefficients and L2 smoothly shrinks.
- Bagging averages learners; boosting corrects errors sequentially.
- Leakage makes evaluation look unrealistically good.
- Model importance is not causal importance.
- Deployment requires validation, versioning, monitoring, ownership, and a response plan.

## 39. Final Mental Model

Professional data science is not “choose an algorithm and call `fit`.” It is a chain of evidence:

1. Define a real decision and measurable outcome.
2. Establish what each row and column represents.
3. Validate the data and its time boundary.
4. Explore patterns without confusing them for proof.
5. Split data in a way that simulates the future use case.
6. Build all learned preprocessing inside the training process.
7. Compare a suitable model with a meaningful baseline.
8. Evaluate errors, uncertainty, calibration, segments, and costs.
9. Communicate what is known, assumed, and limited.
10. Deploy only with reproducibility, monitoring, and responsible controls.

If any link is weak, the final conclusion is weak. Mastering that chain—from question to monitored decision—is what takes you from the basics to professional data science.
