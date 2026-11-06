# Reporte de Tokenomics y Eficiencia - HEKT-NOVA
*Generado automáticamente el 2026-11-06*

Este documento detalla el análisis de compresión de tokens, el coste estructural del diccionario y el punto de equilibrio (*break-even*) del protocolo **HEKT-NOVA** evaluado sobre el benchmark completo.

---

## 📊 Resumen Ejecutivo

* **Total de dominios evaluados:** 12
* **Tokens acumulados (Lenguaje Natural):** `1098`
* **Tokens acumulados (Simbólico HEKT-NOVA):** `651`
* **Ahorro neto medio por llamada:** `37.25 tokens`
* **Coste estructural fijo del diccionario:** `145 tokens`
* **Punto de Equilibrio (Break-Even):** **`3.89 invocaciones`** *(Amortización a partir de la 4ª llamada)*

---

## 📋 Rendimiento por Dominio

| Dominio | Tokens Naturales | Tokens Simbólicos | Ahorro (%) |
| :--- | :---: | :---: | :---: |
| `alineacion_ontologica` | 89 | 33 | **62.9%** |
| `gestion_memoria_vram` | 70 | 36 | **48.6%** |
| `contrato_inteligente` | 173 | 92 | **46.8%** |
| `telemetria_tiempo_real` | 90 | 63 | **30.0%** |
| `enrutamiento_agentes` | 87 | 52 | **40.2%** |
| `seguridad_so` | 87 | 48 | **44.8%** |
| `optimizacion_ollama` | 73 | 48 | **34.2%** |
| `transaccion_asincrona` | 91 | 53 | **41.8%** |
| `arquitectura_agentes` | 85 | 54 | **36.5%** |
| `analisis_tensores` | 89 | 59 | **33.7%** |
| `orquestacion_nodos` | 80 | 53 | **33.8%** |
| `criptografia_post_cuantica` | 84 | 60 | **28.6%** |

---

## 🛠️ Notas Metodológicas
1. **Tokenizador Base:** `hf-internal-testing/llama-tokenizer`.
2. **Overhead del Diccionario:** Corresponde a la inyección de definiciones semánticas de primitivas en el contexto de sistema o caché KV.
3. **Fórmula de Break-Even:** 
   `Invocaciones = Coste Diccionario / Ahorro Neto Promedio`
