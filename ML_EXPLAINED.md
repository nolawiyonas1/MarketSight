# Machine Learning in MarketSight

## 1. The Model (StockModel)
We use a **Linear Regression** model built with PyTorch. It is a foundational ML algorithm suitable for predicting continuous values like stock prices.

- **Inputs (4 Features):**
  - `Open`: Opening price
  - `High`: Highest price of the day
  - `Low`: Lowest price of the day
  - `Volume`: Number of shares traded
- **Output (1 Prediction):**
  - `Close`: The closing price

The model learns a linear equation:
$$ Price = (w_1 \times Open) + (w_2 \times High) + (w_3 \times Low) + (w_4 \times Volume) + Bias $$

## 2. Technical Implementation (PyTorch)

### The Architecture (`nn.Linear`)
```python
self.linear = nn.Linear(input_dim, 1)
```
This single line creates a **Dense Layer**. It initializes a weight matrix ($W$) of shape `[4, 1]` and a bias vector ($b$). When data passes through it (`forward` method), it performs the matrix multiplication: $y = xW^T + b$.

### The Loss Function (`MSELoss`)
```python
criterion = nn.MSELoss()
```
The "Objective Function" that measures performance. We use **Mean Squared Error**, which calculates the average squared difference between the model's prediction and the actual stock price.
$$ Loss = \frac{1}{N} \sum (prediction - actual)^2 $$

### The Optimizer (`SGD`)
```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```
**Stochastic Gradient Descent**. This is the algorithm that updates the weights.
- `lr=0.01` (Learning Rate): Controls how big of a "step" we take during each update. Too high = unstable; too low = too slow.

### The Training Step (Backpropagation)
Inside the loop, four critical steps happen:
1.  **`outputs = model(X)`**: The model makes a guess.
2.  **`loss = criterion(outputs, y)`**: We calculate how wrong the guess was.
3.  **`loss.backward()`**: PyTorch automatically calculates the **gradients** (calculus derivatives). It figures out exactly how much each weight contributed to the error.
4.  **`optimizer.step()`**: The weights are adjusted slightly in the opposite direction of the gradient to reduce the error for next time.

## 3. The Data Pipeline
The training pipeline executed by the worker follows these steps:

1.  **Normalization:**
    - Raw financial data contains large values (e.g., 150.0) which can cause numerical instability.
    - Data is scaled to the range [0, 1] using Min-Max Scaling:
    - *Formula:* $X_{new} = \frac{X - X_{min}}{X_{max} - X_{min}}$

2.  **Persistence:**
    - The trained state (weights and biases) is saved to a `.pth` file.
    - The artifact is uploaded to AWS S3 for storage.

## Future Phase: Advanced Improvements
- **Algorithm Upgrade:** Transition to LSTM (Long Short-Term Memory) or Transformer-based models to capture temporal dependencies (time-series patterns).
- **Data Expansion:** Incorporate historical datasets spanning multiple years.
- **Feature Engineering:** Integrate technical indicators such as Moving Averages (SMA/EMA) and RSI.
