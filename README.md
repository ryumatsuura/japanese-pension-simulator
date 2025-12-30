# Japanese Pension Simulator 🇯🇵

A Python-based simulator to compare the present value of Japanese pension benefits against the opportunity cost of investing pension contributions abroad.

The project provides:
- Simulations of pension vs investment with uncertainty
- An interactive Streamlit web app

---

## 🚀 Live Demo

👉 **[[Simulator Link](https://japanese-pension-simulator.streamlit.app/)]**

---

## 📊 What this does

- Simulates the present value of Japanese pension receipts and investment returns under uncertainty (exchange rates, returns, interest rates)
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
