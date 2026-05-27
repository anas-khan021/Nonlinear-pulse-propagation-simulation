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

Pulse propagation is governed by the Generalized Nonlinear Schrödinger Equation (GNLSE):

$$
\frac{\partial A}{\partial z}
=
-\frac{\alpha}{2}A
+
i\sum_{k\ge2}
\frac{\beta_k}{k!}
\left(
i\frac{\partial}{\partial t}
\right)^k A
+
i\gamma |A|^2 A
$$

where:

| Parameter | Description |
|----------|-------------|
| $A(z,t)$ | Pulse envelope |
| $\alpha$ | Linear loss |
| $\beta_2$ | Group velocity dispersion |
| $\beta_3$ | Third order dispersion |
| $\gamma$ | Nonlinear coefficient |

---

## Simulation Method

The propagation is solved using the Split Step Fourier Method (SSFM):

### Nonlinear Step

$$
A(z+\Delta z)
=
A(z)
\exp(i\gamma |A|^2\Delta z)
$$

### Fourier Transform

$$
\tilde A = FFT(A)
$$

### Linear Step

$$
\tilde A
\leftarrow
\tilde A
\exp(D(\omega)\Delta z)
$$

### Inverse Fourier Transform

$$
A = IFFT(\tilde A)
$$

---

## Dispersion Operator

$$
D(\omega)
=
i\frac{\beta_2}{2}\omega^2
+
i\frac{\beta_3}{6}\omega^3
+
i\frac{\beta_4}{24}\omega^4
+\cdots
$$

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
