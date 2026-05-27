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

<p align="center">

$${\frac{\partial A}{\partial z}=-\frac{\alpha}{2}A+i\sum_{k\ge2}\frac{\beta_k}{k!}\left(i\frac{\partial}{\partial t}\right)^kA+i\gamma|A|^2A}$$

</p>

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

## Nonlinear Operator

The nonlinear step accounts for Kerr nonlinearity and self-phase modulation (SPM):

$$
A(z+\Delta z, t) = A(z,t)\,\exp\left(i\gamma |A(z,t)|^2 \Delta z\right)
$$

The nonlinear operator applies Kerr nonlinearity and models self phase modulation (SPM) during propagation.

### Fourier Transform

$$
\tilde A = FFT(A)
$$

### Linear Step

$$
\tilde A \leftarrow \tilde A \exp(D(\omega)\Delta z)
$$

### Inverse Fourier Transform

$$
A = IFFT(\tilde A)
$$

---
## Dispersion Operator

The linear dispersion operator in the frequency domain is given by:

$$
D(\omega) =
i\frac{\beta_2}{2}\omega^2
+
i\frac{\beta_3}{6}\omega^3
+
i\frac{\beta_4}{24}\omega^4
+
\cdots
$$

The field evolution in Fourier space is given by:

$$
\tilde{A}(\omega, z+\Delta z)
=
\tilde{A}(\omega, z)\,
\exp\left(D(\omega)\Delta z\right)
$$

The dispersion operator models phase accumulation due to higher order chromatic dispersion during propagation.

---

## System Overview

This work consists of two coupled models:

### 1. Mode-locked laser cavity (SSFM round-trip simulation)

The pulse evolves inside a nonlinear laser cavity including:

- Erbium-doped fiber (gain + saturation)
- Dispersion compensating fiber (DCF)
- Single mode fiber (SMF)
- Saturable absorber
- Spectral filter
- Output coupler

The cavity is solved using iterative round-trip propagation.

---

### 2. External nonlinear propagation system

The output pulse from the cavity is injected into:

- Single Mode Fiber (SMF)
- Integrated nonlinear waveguide (WG)

This stage is used to study:
- Spectral broadening
- Self-phase modulation
- Dispersion effects in integrated platforms

---

## Waveguide Dispersion Model (COMSOL Multiphysics)

Waveguide dispersion parameters are computed using a **COMSOL eigenmode solver (EMW module)**.

The model solves the electromagnetic eigenvalue problem for a SiNx waveguide structure including:

- Core (SiNx)
- Silica substrate
- Cladding / superstrate
- PML boundaries

Material dispersion is included using:
- Sellmeier model (silica)
- Polynomial / interpolated SiNx refractive index

---

## Dispersion Extraction

From COMSOL eigenmode results:

Effective index:

$$
n_{\mathrm{eff}}(\lambda)
$$

Propagation constant:

$$
\beta(\lambda) = \frac{2\pi n_{\mathrm{eff}}(\lambda)}{\lambda}
$$

Angular frequency:

$$
\omega = \frac{2\pi c}{\lambda}
$$

Group velocity:

$$
v_g = \left(\frac{d\beta}{d\omega}\right)^{-1}
$$

Group velocity dispersion (GVD):

$$
\beta_2 = \frac{d^2 \beta}{d\omega^2}
$$

Dispersion parameter:

$$
D = -\frac{2\pi c}{\lambda^2}\beta_2
$$

---

## COMSOL Output Files

The script generates:

- `dispParams-Gwidth-*.dat`
- `dispGVD-Gwidth-*.dat`

These are directly used in the SSFM simulation for waveguide propagation.

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
├── dispersion_comsol.m
├── figures/
├── data/
└── README.md
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
- Adaptive SSFM step size
- Full GNLSE vectorial model
- Experimental validation
