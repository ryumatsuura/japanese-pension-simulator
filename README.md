# Japanese Pension Simulator 🇯🇵

A Python-based simulator to compare the present value of Japanese pension benefits against the opportunity cost of investing pension contributions abroad.

The project provides:
- Deterministic pension vs investment comparison
- Simulations with uncertainty
- An interactive Streamlit web app

---

## 🚀 Live Demo

👉 **[Streamlit App Link]**

---

## 📊 What this does

- Computes the present value of Japanese pension receipts and investment returns
- Simulates under uncertainty (exchange rates, returns, interest rates)
- Visualises distributions and probabilities
- Allows interactive exploration via a web UI

---

## 🧩 Project Structure

```text
pension/
  core.py        # Core pension & investment logic
  simulation.py  # Simulation
  config.py      # Constants

app.py           # Streamlit app