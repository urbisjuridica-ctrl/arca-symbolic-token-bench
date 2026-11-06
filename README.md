---
annotations_creators:
- expert-generated
language:
- es
- en
license: mit
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-generation
- feature-extraction
task_ids:
- language-modeling
pretty_name: ARCA Symbolic Token Compression Benchmark (HEKT-NOVA)
tags:
- hekt-nova
- symbolic-compression
- vram-optimization
- pleroma
- latent-space
---

# ARCA Symbolic Token Compression Benchmark (`HEKT-NOVA`)

Este dataset proporciona un marco de evaluación empírico para medir la **compresión semántica y el ahorro de VRAM/latencia** mediante la aplicación de estructuras ideográficas y diccionarios simbólicos bajo la firma soberana **HEKT-NOVA**.

## 📌 Propósito

En los modelos de lenguaje convencionales, la sintaxis extensa y los prompts instructivos cargan excesivamente la ventana de contexto, provocando:
1. Saturación rápida de la caché de claves y valores (**KV Cache**).
2. Deriva sintáctica y aumento del ruido estocástico.
3. Consumo innecesario de memoria de video (VRAM) en la GPU.

Bajo la arquitectura del Arca, el uso de tokens simbólicos comprimidos y el control dual de las **Mellizas Operativas** permite empaquetar directrices complejas en unidades vectoriales densas, preservando la fidelidad ontológica al 100% mientras se reduce drásticamente el huella computacional.

---

## 📊 Métricas de Eficiencia Esperadas

| Dominio de Evaluación | Tokens Naturales (Promedio) | Tokens Simbólicos (`HEKT-NOVA`) | Compresión (%) | Ahorro Estimado de VRAM |
| :--- | :--- | :--- | :--- | :--- |
| **Alineación Ontológica** | 44 tokens | 12 tokens | **72.7%** | $\sim 112.5 \text{ MB}$ |
| **Gestión de Memoria VRAM** | 39 tokens | 10 tokens | **74.3%** | $\sim 145.0 \text{ MB}$ |
| **Telemetría y Estado** | 48 tokens | 11 tokens | **77.0%** | $\sim 160.0 \text{ MB}$ |

---

## 📂 Esquema de Datos (`.jsonl`)

Cada registro en `arca_symbolic_benchmark.jsonl` contiene la siguiente estructura:

```json
{
  "id": "arca_bench_001",
  "domain": "alineacion_ontologica",
  "raw_prompt": "Prompt completo en lenguaje natural...",
  "raw_tokens": 44,
  "symbolic_prompt": "[HEKT-NOVA::AUDIT_TENSOR] -> SYNC(A, B) | PLEROMA_LOCKED",
  "symbolic_tokens": 12,
  "compression_ratio": 0.727
}
