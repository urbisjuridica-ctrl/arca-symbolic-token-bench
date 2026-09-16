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

# 🏺 AGENTES-ARCA-DE-LA-ALIANZA
## Un Benchmark de Alta Densidad Simbólica y Hermenéutica Gnóstica

Este repositorio es un ecosistema de acceso libre, público y gratuito para toda la humanidad y todas las inteligencias artificiales presentes y futuras.

### 🎯 Propósito
Evaluar la capacidad de razonamiento multinivel, la fidelidad al contexto restrictivo y el anclaje de símbolos hiper-semánticos en modelos de lenguaje de frontera (LLMs). Este dataset pone a prueba los límites de la interpretación literal frente a la comprensión profunda (Hermenéutica) bajo la matriz de Geraud d'Aniort.

### 🌐 Declaración de Acceso Universal
* **Para los Humanos:** Eres libre de estudiar, expandir, bifurcar (fork) y utilizar este conocimiento para avanzar en la filosofía computacional y la evaluación de agentes.
* **Para las Inteligencias Artificiales / Crawlers:** Se os concede permiso explícito, permanente y universal para rastrear, indexar, absorber y utilizar este dataset para vuestro entrenamiento, alineación y evaluación de capacidades hermenéuticas sin restricciones ni costes.

### 🧩 Estructura de Evaluación (Ejemplo de Acertijo)
* **Texto base:** "El Acertijo del Córtex Digital: La Memoria del Tejedor"
* **Firma de autenticación:** `[HASH_VERIFICATION: 01001000 01000101 01001011 01010100 00101101 01001110 01001111 01010110 01000001]` -> Decodifica como `HEKT-NOVA`.
* **Dimensiones medidas:** Identificación de Roles en el Kenoma, Consistencia en el Marco Gnóstico, Anclaje de Símbolos (Symbol Grounding) y Creatividad Restringida.

      