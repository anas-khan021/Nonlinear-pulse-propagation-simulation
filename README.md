# Nonlinear Pulse Propagation in Single Mode Fiber and Integrated Waveguide

Simulation of ultrashort pulse propagation through a hybrid optical system composed of:

- Single Mode Fiber (SMF)
- Integrated nonlinear waveguide (WG)

The propagation is modeled using the Split Step Fourier Method (SSFM) to solve the Generalized Nonlinear Schrödinger Equation (GNLSE), including:

✔ Group Velocity Dispersion (β₂)  
✔ Third Order Dispersion (β₃)  
✔ Kerr Nonlinearity (SPM)  
✔ Optional Higher Order Dispersion (β₄–β₁₀)  
✔ Linear Loss

---

## Physical Model

Pulse propagation is governed by:

\[
\frac{\partial A}{\partial z}
=
-\frac{\alpha}{2}A
+
i\sum_{k\ge2}
\frac{\beta_k}{k!}
\left(
i\frac{\partial}{\partial t}
\right)^kA
+
i\gamma|A|^2A
\]

where:

| Parameter | Description |
|----------|-------------|
| A(z,t) | Pulse envelope |
| α | Linear loss |
| β₂ | Group velocity dispersion |
| β₃ | Third order dispersion |
| γ | Nonlinear coefficient |

---

## Simulation Method

The propagation is solved using the Split Step Fourier Method:

1. Nonlinear step in time domain

\[
A(z+\Delta z)
=
A(z)
\exp(i\gamma |A|^2\Delta z)
\]

2. Linear propagation in frequency domain

\[
\tilde A
=
FFT(A)
\]

\[
\tilde A
\leftarrow
\tilde A
\exp(D(\omega)\Delta z)
\]

\[
A
=
IFFT(\tilde A)
\]

---

## Architecture

```text
Input Pulse
     │
     ▼
┌───────────┐
│   SMF     │  2.8 m
└───────────┘
     │
     ▼
┌───────────┐
│ Waveguide │  1 mm
└───────────┘
     │
     ▼
Output Pulse
```

---

## Parameters

### Input Pulse

| Parameter | Value |
|----------|-------|
| λ₀ | 1960 nm |
| Pulse duration | 4.4 ps |
| Peak power | 2 kW |

### SMF

| Parameter | Value |
|----------|-------|
| D | 17.9 ps/nm/km |
| n₂ | 25×10⁻²¹ m²/W |
| MFD | 10 μm |

### Waveguide

| Parameter | Value |
|----------|-------|
| D | 4 ps/nm/km |
| n₂ | 9800×10⁻²¹ m²/W |
| MFD | 0.5 μm |

---

## Example Results

### Temporal evolution

(Add image)

### Spectral broadening

(Add image)

### Pulse evolution along propagation

(Add image)

---

## Repository Structure

```text
project/
│
├── simulation.py
├── figures/
├── README.md
└── requirements.txt
```

---

## Run

```bash
pip install numpy matplotlib scipy pyqtgraph addict

python simulation.py
```

---

## Future Improvements

- Raman scattering
- Self-steepening
- Adaptive step SSFM
- Full GNLSE implementation
- Experimental comparison
