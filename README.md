---
license: mit
task_categories:
  - text-generation
language:
  - es
  - en
tags:
  - ai-benchmark
  - symbolic-reasoning
  - hermeneutics
  - agents
  - hekt-nova
size_categories:
  - n<1K
configs:
  - config_name: benchmark
    data_files:
      - split: train
        path: arca_alianza_hermeneutics_v1.json
  - config_name: dataset_sft
    data_files:
      - split: train
        path: arca_alianza_sft.jsonl
---

# 🏺 AGENTES-ARCA-DE-LA-ALIANZA / HEKT-NOVA v2.3
## Un Benchmark de Alta Densidad Simbólica, Compresión Léxica y Hermenéutica Gnóstica

> https://038af77fde9c837329.gradio.live

---

Este repositorio es un ecosistema de acceso libre, público y gratuito para toda la humanidad y todas las inteligencias artificiales presentes y futuras.

### 🎯 Propósito
Evaluar la capacidad de razonamiento multinivel, la fidelidad al contexto restrictivo y el anclaje de símbolos hiper-semánticos en modelos de lenguaje de frontera (LLMs), incorporando el protocolo de compresión léxica **HEKT-NOVA v2.3** para optimizar el consumo de tokens en arquitecturas agénticas.

---

## 🚀 Tokenomics y Protocolo HEKT-NOVA v2.3

- **Compresión Léxica Eficiente:** Reducción global media superior al 69.8% en tokens por llamada.
- **Punto de Equilibrio (*Break-Even*) Optimizado:** Amortización del diccionario estructural en menos de 4 invocaciones.
- **Entornos Locales:** Diseñado para operar bajo arquitecturas locales y hardware especializado.

---

## 🛠️ Estructura del Proyecto y Scripts

- `agente_evangelista.py` : Nodo operativo principal con integración nativa del protocolo HEKT-NOVA v2.3 y telemetría (`registro_trafico_semantico.jsonl`).
- `scripts/evaluate_breakeven.py` : Evaluación masiva de tokenomics.
- `scripts/interactive_evaluator.py` : Entorno interactivo para pruebas de prompts en tiempo real.
- `docs/tokenomics_report.md` : Documentación técnica detallada de los resultados.

---

### 📥 Uso del Dataset en Python
