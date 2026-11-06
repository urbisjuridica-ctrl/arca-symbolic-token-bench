# ARCA-DE-LA-ALIANZA-AGENTS / HEKT-NOVA v2.1

Repositorio oficial para el protocolo de compresión léxica y optimización de tokens **HEKT-NOVA**. Este sistema permite reducir significativamente el consumo de contexto en modelos de lenguaje locales mediante un diccionario compacto basado en namespaces estructurados (`[H::...]`).

---

## 🚀 Características Principales

* **Compresión Léxica Eficiente:** Reducción global media superior al 39% en tokens por llamada.
* **Punto de Equilibrio (*Break-Even*) Optimizado:** Amortización del diccionario estructural en menos de 4 invocaciones (~3.7).
* **Entornos Locales:** Diseñado para operar de forma fluida bajo arquitecturas locales y CPU/GPU en Python.

---

## 🛠️ Estructura del Proyecto

* `scripts/evaluate_breakeven.py` : Evaluación masiva de tokenomics en los 12 dominios del benchmark.
* `scripts/interactive_evaluator.py` : Entorno interactivo para pruebas de prompts en tiempo real.
* `scripts/export_tokenomics_doc.py` : Generador automático de reportes formales en Markdown.
* `scripts/monitor_vram.py` : Supervisión de recursos de hardware local.
* `docs/tokenomics_report.md` : Documentación técnica detallada de los resultados.

---

## 📋 Próximos Pasos y Roadmap (v2.1+)

- [ ] **Paso 1:** Extraer y ejecutar scripts automáticos de validación (`scripts/`). ⏳ *Pendiente*
- [ ] **Paso 2:** Implementar comparador robusto de fidelidad semántica para las salidas del LLM. ⏳ *Pendiente*
- [ ] **Paso 3:** Realizar mediciones de rendimiento en GPU real utilizando precisión mixta (BF16/FP8). ⏳ *Pendiente*
- [ ] **Paso 4:** Ampliar el dataset de benchmarks a $\ge 100$ casos de prueba diversos. ⏳ *Pendiente*
- [ ] **Paso 5:** Publicar la tabla comparativa definitiva de rendimiento y ahorro de tokens en la documentación. ⏳ *Pendiente*
