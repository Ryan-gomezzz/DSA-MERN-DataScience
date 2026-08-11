# NumPy Study Guide: Fundamentals to Advanced

Use this guide to learn NumPy, revise before a test, and look up common operations. Run the examples yourself: changing values and predicting the result before execution is one of the fastest ways to learn.

## 1. What NumPy Is

NumPy, short for **Numerical Python**, is the core Python library for fast numerical computing. Its main object is the `ndarray`: an efficient, fixed-size, multidimensional array whose elements normally share one data type.

```python
import numpy as np
```

Why use NumPy instead of ordinary Python lists?

- Arrays use compact, homogeneous storage.
- Vectorized operations avoid slow Python loops.
- Broadcasting makes differently shaped arrays work together.
- It provides statistics, random sampling, linear algebra, and file I/O.
- pandas, SciPy, scikit-learn, and many other libraries build on it.

```python
values = np.array([1, 2, 3, 4])
print(values * 10)       # [10 20 30 40]
```

With a Python list, `values_list * 2` repeats the list. With a NumPy array, `values * 2` multiplies every element.

## 2. Creating Arrays

### From Python objects

```python
a = np.array([1, 2, 3])
b = np.array([[1, 2, 3], [4, 5, 6]])
c = np.array([1, 2, 3], dtype=np.float64)

print(a)          # [1 2 3]
print(b.shape)    # (2, 3)
print(c)          # [1. 2. 3.]
```

A rectangular nested list creates a proper numeric array. Ragged nested lists should usually be fixed rather than stored as `dtype=object`.

### Filled arrays

```python
np.zeros((2, 3))              # all 0.0
np.ones((2, 3), dtype=int)    # all 1
np.full((2, 3), 7)            # all 7
np.empty((2, 3))              # uninitialized; values are unpredictable
np.eye(3)                     # 3 x 3 identity matrix
np.diag([2, 4, 6])            # values on the diagonal
```

`np.empty` is fast, but its values must be overwritten before use.

### Numeric sequences

```python
np.arange(0, 10, 2)       # [0 2 4 6 8]; stop is excluded
np.linspace(0, 1, 5)      # [0.   0.25 0.5  0.75 1.  ]; stop included by default
np.logspace(0, 3, 4)      # [1, 10, 100, 1000]
```

Use `arange` mainly for integer steps. For decimal endpoints, `linspace` avoids floating-point step surprises.

### Create like another array

```python
x = np.array([[1, 2], [3, 4]])
np.zeros_like(x)
np.ones_like(x, dtype=float)
np.full_like(x, 9)
```

## 3. Essential Array Properties

```python
x = np.array([[10, 20, 30], [40, 50, 60]], dtype=np.int64)

x.ndim       # 2: number of axes
x.shape      # (2, 3): rows, columns
x.size       # 6: total elements
x.dtype      # int64 on many systems
x.itemsize   # bytes used by one element
x.nbytes     # total bytes used by array data
len(x)       # 2: length of the first axis only
```

Important distinction:

- `shape` describes each axis.
- `size` is the product of all shape values.
- `len(array)` returns only `shape[0]`.

### Dimensions

```python
scalar = np.array(5)                     # shape ()
vector = np.array([1, 2, 3])             # shape (3,)
matrix = np.array([[1, 2], [3, 4]])      # shape (2, 2)
tensor = np.zeros((2, 3, 4))             # shape (2, 3, 4)
```

A one-dimensional array with shape `(3,)` is not the same as a row array `(1, 3)` or column array `(3, 1)`.

```python
v = np.array([1, 2, 3])
row = v.reshape(1, 3)
column = v.reshape(3, 1)
```

## 4. Data Types (`dtype`)

Common types include:

- Integers: `int8`, `int16`, `int32`, `int64`
- Unsigned integers: `uint8`, `uint16`, and others
- Floating point: `float32`, `float64`
- Complex: `complex64`, `complex128`
- Boolean: `bool_`
- Fixed-width text: Unicode such as `<U10`
- Python objects: `object` (flexible but slower)

```python
a = np.array([1, 2, 3], dtype=np.float32)
b = a.astype(np.int32)       # converted copy
```

NumPy chooses a common type when values differ:

```python
np.array([1, 2.5, 3]).dtype      # float64 in a typical installation
np.array([1, "two", 3]).dtype    # Unicode string type
```

Watch for:

- Integer overflow in small integer types.
- Decimal rounding because binary floating point is approximate.
- Assigning a float to an integer array truncates or rejects information.
- `np.nan` is a floating-point value, so ordinary integer arrays cannot store it.

## 5. Indexing and Slicing

### One-dimensional arrays

```python
a = np.array([10, 20, 30, 40, 50])

a[0]        # 10
a[-1]       # 50
a[1:4]      # [20 30 40]
a[:3]       # [10 20 30]
a[::2]      # [10 30 50]
a[::-1]     # reversed view
```

The stop position is excluded, just like normal Python slicing.

### Two-dimensional arrays

```python
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

m[1, 2]       # 6: row 1, column 2
m[1]          # [4 5 6]: entire second row
m[:, 1]       # [2 5 8]: entire second column
m[0:2, 1:3]   # [[2 3], [5 6]]
```

For a 3-D array, use `array[layer, row, column]`. A colon selects everything on that axis.

### Boolean masking

```python
a = np.array([5, 12, 7, 20, 3])
mask = a >= 10

mask                 # [False True False True False]
a[mask]              # [12 20]
a[a >= 10]           # same result
a[(a >= 5) & (a < 20)]
a[(a < 5) | (a > 15)]
a[~(a >= 10)]        # invert condition
```

Use `&`, `|`, and `~` for element-wise boolean logic. Put each comparison in parentheses. Python's `and`, `or`, and `not` do not perform element-wise array logic.

Masks can also assign values:

```python
a[a < 10] = 0
```

### Fancy indexing

```python
a = np.array([10, 20, 30, 40, 50])
a[[4, 0, 2]]                   # [50 10 30]

m = np.arange(12).reshape(3, 4)
m[[0, 2], [1, 3]]              # elements m[0,1] and m[2,3]
m[np.ix_([0, 2], [1, 3])]      # rectangular submatrix
```

Basic slicing usually returns a **view**. Boolean and fancy indexing return a **copy**.

## 6. Copies Versus Views

This is a frequent exam and debugging topic.

```python
original = np.array([1, 2, 3, 4])
view = original[1:3]
view[0] = 99
print(original)                # [ 1 99  3  4]

independent = original[1:3].copy()
independent[0] = -1
print(original)                # unchanged by this assignment
```

- A view shares the same underlying data.
- A copy owns independent data.
- Use `.copy()` when an isolated result is required.

`view.base` may help reveal whether memory is shared, and `np.shares_memory(a, b)` is a clearer check.

## 7. Reshaping and Rearranging

```python
a = np.arange(12)
m = a.reshape(3, 4)
n = a.reshape(3, -1)       # NumPy infers 4
```

The new shape must contain the same total number of elements. Only one dimension may be `-1`.

```python
m.ravel()          # flattened view when possible
m.flatten()        # always a flattened copy
m.T                # transpose: axes reversed for a matrix
m.transpose()
np.swapaxes(m, 0, 1)
```

Adding or removing size-one axes:

```python
v = np.array([1, 2, 3])
v[:, np.newaxis]           # shape (3, 1)
v[None, :]                 # shape (1, 3)
np.expand_dims(v, axis=0)  # shape (1, 3)
np.squeeze(np.array([[[1], [2], [3]]]))  # removes size-one axes
```

For arrays with more than two dimensions, `.T` reverses all axes. Use `transpose(axes)` or `moveaxis` when exact axis order matters.

## 8. Vectorized Operations and Universal Functions

Arithmetic normally happens element by element:

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b          # [11 22 33]
a - b
a * b          # element-wise multiplication
b / a
b // a
b % a
a ** 2
```

Common universal functions, called **ufuncs**:

```python
np.sqrt(a)
np.exp(a)
np.log(a)
np.log10(a)
np.sin(a)
np.abs(a)
np.round(np.array([1.234, 5.678]), 2)
np.maximum(a, b)
```

Comparisons also work element by element:

```python
a > 1
a == np.array([1, 0, 3])
np.isclose(0.1 + 0.2, 0.3)       # safer for floats
np.allclose([0.1 + 0.2], [0.3])
```

Do not normally test floats with exact `==` because of representation error.

### Conditional selection

```python
scores = np.array([35, 82, 60, 49])
labels = np.where(scores >= 50, "pass", "fail")

clipped = np.clip(scores, 40, 75)  # lower than 40 -> 40; higher than 75 -> 75
```

## 9. Broadcasting

Broadcasting lets NumPy perform operations on compatible shapes without physically copying the smaller array.

Compare shapes from the **rightmost dimension**. Two dimensions are compatible when:

1. They are equal, or
2. One of them is `1`, or
3. One shape has no dimension at that position.

Examples:

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])       # shape (2, 3)

m + 10                           # scalar broadcasts everywhere
m + np.array([10, 20, 30])      # (2, 3) + (3,): add by column
m + np.array([[10], [20]])      # (2, 3) + (2, 1): add by row
```

Shape reasoning:

```text
(2, 3)
   (3)   -> compatible; result (2, 3)

(2, 3)
(2, 1)   -> compatible; result (2, 3)

(2, 3)
   (2)   -> incompatible
```

To make a row statistic broadcast across columns, keep the reduced axis or restore it:

```python
row_means = m.mean(axis=1, keepdims=True)  # shape (2, 1)
centered_by_row = m - row_means
```

## 10. Aggregation and the Meaning of `axis`

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])

m.sum()             # 21: every element
m.sum(axis=0)       # [5 7 9]: collapse rows, one result per column
m.sum(axis=1)       # [6 15]: collapse columns, one result per row
```

Think: **the named axis is removed/collapsed**.

Common reductions:

```python
np.sum(m, axis=0)
np.mean(m, axis=0)
np.median(m, axis=0)
np.min(m, axis=0)
np.max(m, axis=0)
np.std(m, axis=0)       # population standard deviation by default (ddof=0)
np.var(m, axis=0)
np.prod(m, axis=0)
np.any(m > 5, axis=0)
np.all(m > 0, axis=0)
np.argmin(m, axis=0)    # positions of minima
np.argmax(m, axis=0)    # positions of maxima
```

Sample standard deviation commonly uses `ddof=1`:

```python
sample_std = np.std(m, ddof=1)
```

Cumulative calculations preserve element count:

```python
np.cumsum([1, 2, 3, 4])       # [1 3 6 10]
np.cumprod([1, 2, 3, 4])      # [1 2 6 24]
```

## 11. Missing and Invalid Numeric Values

```python
x = np.array([1.0, np.nan, 3.0, np.inf])

np.isnan(x)
np.isinf(x)
np.isfinite(x)
```

Normal reductions propagate `NaN`:

```python
np.mean(x)          # nan
np.nanmean(x)       # ignores nan, but not infinity
np.nansum(x)
np.nanmedian(x)
np.nanstd(x)
np.nanmin(x)
np.nanmax(x)
```

`np.nan == np.nan` is `False`. Detect missing numeric values with `np.isnan`, not equality.

```python
clean = x[np.isfinite(x)]
replaced = np.nan_to_num(x, nan=0.0, posinf=999.0, neginf=-999.0)
```

## 12. Sorting, Searching, and Set Operations

```python
a = np.array([40, 10, 30, 20, 20])

np.sort(a)                  # sorted copy
a.sort()                    # sorts a in place
np.argsort(a)               # indices that would sort a
np.unique(a)                # sorted unique values
np.unique(a, return_counts=True)
np.where(a == 20)           # tuple of matching index arrays
np.nonzero(a > 20)
np.count_nonzero(a > 20)
```

Set-like operations:

```python
np.intersect1d([1, 2, 3], [2, 3, 4])
np.union1d([1, 2, 3], [2, 3, 4])
np.setdiff1d([1, 2, 3], [2, 4])
np.isin([1, 2, 3], [2, 4])
```

For a sorted array, `np.searchsorted` finds insertion positions efficiently.

## 13. Combining and Splitting Arrays

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

np.concatenate([a, b], axis=0)  # append rows -> shape (4, 2)
np.concatenate([a, b], axis=1)  # append columns -> shape (2, 4)
np.vstack([a, b])                # vertical stack
np.hstack([a, b])                # horizontal stack
np.stack([a, b], axis=0)         # new axis -> shape (2, 2, 2)
```

Key difference:

- `concatenate` joins along an **existing** axis.
- `stack` creates a **new** axis.

Splitting:

```python
x = np.arange(12)
np.split(x, 3)             # equal pieces; must divide exactly
np.array_split(x, 5)       # allows unequal pieces

m = np.arange(16).reshape(4, 4)
np.vsplit(m, 2)
np.hsplit(m, 2)
```

## 14. Linear Algebra

For matrices, `*` is element-wise multiplication. Use `@` or `np.matmul` for matrix multiplication.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A * B                 # element-wise
A @ B                 # matrix product
np.matmul(A, B)       # matrix product
np.dot(A, B)          # dot/matrix product in common 1-D and 2-D cases
```

Useful functions:

```python
np.linalg.det(A)          # determinant
np.linalg.matrix_rank(A)  # rank
np.linalg.eig(A)          # eigenvalues and eigenvectors
np.linalg.svd(A)          # singular value decomposition
np.linalg.norm(A)         # vector/matrix norm
```

Solve `Ax = b` like this:

```python
A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])
x = np.linalg.solve(A, b)
```

Prefer `solve(A, b)` to `inv(A) @ b`: it is generally faster and more numerically stable. Use `np.linalg.lstsq` for least-squares problems.

## 15. Random Numbers

Modern NumPy code should create a generator:

```python
rng = np.random.default_rng(seed=42)

rng.random(5)                    # uniform floats in [0, 1)
rng.integers(1, 7, size=10)      # integers 1 through 6
rng.normal(loc=0, scale=1, size=5)
rng.uniform(low=-1, high=1, size=(2, 3))
rng.choice(["A", "B", "C"], size=5, p=[0.2, 0.5, 0.3])
rng.permutation(10)
```

A seed makes a pseudorandom sequence reproducible. It does not make the values truly random.

Shuffle in place:

```python
items = np.arange(10)
rng.shuffle(items)
```

## 16. Reading and Writing Arrays

Native binary format:

```python
np.save("array.npy", a)
loaded = np.load("array.npy")

np.savez("arrays.npz", first=a, second=b)
bundle = np.load("arrays.npz")
print(bundle["first"])
```

Text format:

```python
np.savetxt("array.csv", a, delimiter=",", fmt="%.2f")
loaded = np.loadtxt("array.csv", delimiter=",")
```

`np.genfromtxt` is more flexible than `loadtxt` when a text file contains missing values. For mixed-type tables with column names, pandas is usually a better choice.

## 17. Performance and Memory

### Prefer vectorization

```python
# Slower Python approach
result = [value ** 2 for value in range(1_000_000)]

# NumPy approach
values = np.arange(1_000_000)
result = values ** 2
```

### Avoid repeated growth

Repeated `np.append` creates a new array each time. Accumulate in a Python list and convert once, or preallocate:

```python
result = np.empty(1000)
for i in range(1000):
    result[i] = i ** 2
```

### Choose suitable types

```python
small = np.arange(1_000_000, dtype=np.int32)
```

Smaller dtypes save memory, but only when their numeric range and precision are sufficient.

### In-place operations

```python
a = np.arange(5, dtype=float)
a *= 2
```

In-place work can reduce allocations, but it mutates data and may fail when casting would be unsafe.

## 18. Practical Patterns

### Standardize each feature column

```python
X = np.array([[1.0, 10.0], [2.0, 30.0], [3.0, 20.0]])
means = X.mean(axis=0)
stds = X.std(axis=0)
X_standardized = (X - means) / stds
```

### Min-max scale each column

```python
mins = X.min(axis=0)
maxs = X.max(axis=0)
X_scaled = (X - mins) / (maxs - mins)
```

Constant columns have `maxs - mins == 0`; handle them explicitly to avoid division by zero.

### Pairwise Euclidean distances

```python
points = np.array([[0, 0], [3, 4], [6, 8]])
differences = points[:, None, :] - points[None, :, :]
distances = np.sqrt((differences ** 2).sum(axis=2))
```

Shape logic: `(n, 1, features) - (1, n, features)` broadcasts to `(n, n, features)`.

### One-hot encoding integer labels

```python
labels = np.array([0, 2, 1, 2])
one_hot = np.eye(3, dtype=int)[labels]
```

## 19. Common Mistakes and Test Traps

1. **Confusing list and array multiplication**: list multiplication repeats; array multiplication is numeric.
2. **Forgetting that stop is excluded** in slices and `arange`.
3. **Using `and`/`or` with arrays** instead of `&`/`|` plus parentheses.
4. **Assuming a slice is independent**: basic slices often share memory.
5. **Confusing `*` and `@`**: element-wise versus matrix multiplication.
6. **Reducing the wrong axis**: `axis=0` collapses rows; `axis=1` collapses columns in a matrix.
7. **Using exact equality for floats**: prefer `isclose` or `allclose`.
8. **Comparing `NaN` using equality**: use `isnan`.
9. **Ignoring dtype conversion**: assigning decimals to integer arrays loses information.
10. **Assuming reshape always copies**: it returns a view when possible, but not always.
11. **Using global random functions in new code**: prefer `default_rng`.
12. **Calling `np.append` repeatedly**: it reallocates and is not list-like in performance.
13. **Misunderstanding `np.append` without `axis`**: it flattens inputs.
14. **Getting broadcasting direction wrong**: compare dimensions from the right.
15. **Using `np.vectorize` for speed**: it is mainly convenience and usually still runs a Python-level loop.

## 20. Quick Reference

| Goal | NumPy expression |
|---|---|
| Create array | `np.array(data)` |
| Integer sequence | `np.arange(start, stop, step)` |
| Evenly spaced values | `np.linspace(start, stop, count)` |
| Inspect | `a.shape`, `a.ndim`, `a.size`, `a.dtype` |
| Convert type | `a.astype(np.float64)` |
| Reshape | `a.reshape(rows, cols)` |
| Flatten view if possible | `a.ravel()` |
| Guaranteed flattened copy | `a.flatten()` |
| Transpose matrix | `a.T` |
| Filter | `a[a > 0]` |
| Conditional values | `np.where(condition, yes, no)` |
| Total / column / row sum | `a.sum()`, `a.sum(0)`, `a.sum(1)` |
| Ignore NaN in mean | `np.nanmean(a)` |
| Sort / sorting indices | `np.sort(a)`, `np.argsort(a)` |
| Unique values | `np.unique(a)` |
| Join existing axis | `np.concatenate([...], axis=...)` |
| Create new stacking axis | `np.stack([...], axis=...)` |
| Matrix multiply | `a @ b` |
| Reproducible generator | `np.random.default_rng(seed)` |
| Independent data | `a.copy()` |

## 21. Practice Questions

Try these without running the code first.

1. What are the `shape`, `ndim`, and `size` of `np.zeros((2, 3, 4))`?
2. What does `np.arange(12).reshape(3, -1)` produce?
3. For a `(4, 5)` matrix, what shapes result from `sum(axis=0)` and `sum(axis=1)`?
4. Why might modifying `a[2:5]` modify `a`?
5. Is shape `(3, 4)` compatible with `(4,)` for broadcasting? Is it compatible with `(3,)`?
6. How do `ravel` and `flatten` differ?
7. What is the difference between `A * B` and `A @ B`?
8. Write a condition selecting values from 10 through 20 inclusive.
9. Why does `np.nan == np.nan` return `False`, and how should it be tested?
10. Write code to replace all negative array values with zero.
11. How would you calculate a sample standard deviation?
12. Why is `np.linalg.solve(A, b)` preferred to `np.linalg.inv(A) @ b`?

### Answers

1. Shape `(2, 3, 4)`, 3 dimensions, 24 elements.
2. A 3-by-4 array containing 0 through 11.
3. `(5,)` after collapsing rows; `(4,)` after collapsing columns.
4. Basic slicing normally creates a view that shares memory.
5. `(4,)` is compatible; `(3,)` is not because rightmost dimensions 4 and 3 conflict.
6. `ravel` returns a view when possible; `flatten` always returns a copy.
7. `*` multiplies matching elements; `@` performs matrix multiplication.
8. `a[(a >= 10) & (a <= 20)]`.
9. NaN represents an unknown/non-number value and is not equal even to itself; use `np.isnan`.
10. `a[a < 0] = 0` or `a = np.where(a < 0, 0, a)`.
11. `np.std(a, ddof=1)`.
12. Solving directly is normally faster and more numerically stable than explicitly computing an inverse.

## 22. Final Revision Checklist

Before a test, make sure you can explain and demonstrate:

- Array creation, shape, dimension, size, and dtype
- One-, two-, and multidimensional indexing
- Boolean and fancy indexing
- Views versus copies
- Reshaping, transposition, and size-one axes
- Vectorization and universal functions
- Broadcasting rules from right to left
- `axis=0` versus `axis=1`
- NaN-aware calculations
- Sorting, searching, joining, and splitting
- Element-wise versus matrix multiplication
- Reproducible random generators
- Why NumPy is faster than Python loops for bulk numeric operations

If you can predict the shapes and outputs of small examples involving indexing, broadcasting, and axes, you understand the most heavily tested parts of NumPy.
