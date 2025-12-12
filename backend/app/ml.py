import pandas as pd
import torch
import torch.nn as nn
import os

# Define a simple Linear Regression Model
class StockModel(nn.Module):
    def __init__(self, input_dim):
        super(StockModel, self).__init__()
        # Input: 4 features (open, high, low, volume)
        # Output: 1 prediction (close price)
        self.linear = nn.Linear(input_dim, 1)

    def forward(self, x):
        return self.linear(x)

def train(csv_path: str, model_save_path: str):
    """
    Reads a CSV, trains a PyTorch model, and saves the .pth file.
    """
    print(f"ML: Loading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"ML: Error reading CSV: {e}")
        raise e

    # Simple Feature Engineering
    # Ensure these columns exist in your CSV
    required_cols = ['open', 'high', 'low', 'volume', 'close']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    X_data = df[['open', 'high', 'low', 'volume']].values
    y_data = df[['close']].values

    # Normalize Data (Simple Min-Max Scaling)
    # This prevents 'nan' loss by keeping values small (between 0 and 1)
    X_min, X_max = X_data.min(axis=0), X_data.max(axis=0)
    y_min, y_max = y_data.min(axis=0), y_data.max(axis=0)
    
    # Avoid division by zero
    X_data = (X_data - X_min) / (X_max - X_min + 1e-7)
    y_data = (y_data - y_min) / (y_max - y_min + 1e-7)

    # Convert to PyTorch tensors
    X = torch.tensor(X_data, dtype=torch.float32)
    y = torch.tensor(y_data, dtype=torch.float32)

    # Initialize Model
    model = StockModel(input_dim=4)
    criterion = nn.MSELoss()
    # Learning rate can be slightly higher now that data is normalized
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    # Train loop (100 epochs)
    print("ML: Training model...")
    for epoch in range(100):
        # Forward pass
        outputs = model(X)
        loss = criterion(outputs, y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 20 == 0:
            print(f"ML: Epoch [{epoch+1}/100], Loss: {loss.item():.4f}")

    # Save the model
    print(f"ML: Saving model to {model_save_path}...")
    torch.save(model.state_dict(), model_save_path)
    return model_save_path

