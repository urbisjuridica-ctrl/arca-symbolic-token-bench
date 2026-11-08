#!/usr/bin/env python3
"""
Generador automático de banco de pruebas extendido para HEKT-NOVA v2.2.
Produce más de 100 ejemplos únicos distribuidos en 10 dominios sin duplicados,
con soporte bilingüe (ES/EN) y etiquetas de namespaces simbólicos [H::...].
"""

import json
import os
import random

DOMINIOS = [
    "software_architecture",
    "machine_learning_pipelines",
    "cybersecurity_audit",
    "symbolic_logic",
    "hermeneutic_ontology",
    "cryptocurrency_trading",
    "concurrency_systems",
    "database_optimization",
    "network_protocols",
    "distributed_agents"
]

ESTRUCTURAS_PROMPT = [
    ("Optimiza el siguiente bloque de código aplicando {constraint} asegurando {format_out}.", 
     "Optimize the following code block applying {constraint} ensuring {format_out}."),
    ("Analiza la traza de ejecución bajo el namespace [H::SYS] y valida contra {constraint} en formato {format_out}.", 
     "Analyze the execution trace under [H::SYS] namespace validating against {constraint} in {format_out} format."),
    ("Resuelve el siguiente dilema lógico aplicando restricciones de tipo {constraint} con salida estricta en {format_out}.", 
     "Resolve the following logical dilemma applying {constraint} constraints with strict {format_out} output."),
    ("Audita el subsistema de seguridad usando el arquetipo [H::SEC] evaluando {constraint} bajo {format_out}.", 
     "Audit the security subsystem using [H::SEC] archetype evaluating {constraint} under {format_out}."),
    ("Diseña un pipeline de procesamiento escalable considerando {constraint} y reportando métricas en {format_out}.", 
     "Design a scalable processing pipeline considering {constraint} reporting metrics in {format_out}.")
]

CONSTRAINTS = [
    "baja latencia y cero dependencias externas",
    "tipado estricto y manejo defensivo de excepciones",
    "invarianza semántica y compresión simbólica máxima",
    "aislamiento de procesos y trazabilidad criptográfica",
    "consistencia eventual y tolerancia a particiones"
]

FORMATS = ["JSON", "Markdown Table", "YAML", "Plain Text Structured", "JSONL"]

NAMESPACES = ["[H::SYS]", "[H::LOG]", "[H::SEC]", "[H::OPT]", "[H::NET]"]

def generar_dataset(total_objetivo=120):
    dataset = []
    id_contador = 1
    hashes_vistos = set()
    
    while len(dataset) < total_objetivo:
        dominio = random.choice(DOMINIOS)
        plantilla_es, plantilla_en = random.choice(ESTRUCTURAS_PROMPT)
        constraint = random.choice(CONSTRAINTS)
        fmt = random.choice(FORMATS)
        ns = random.choice(NAMESPACES)
        
        prompt_es = plantilla_es.format(constraint=constraint, format_out=fmt)
        prompt_en = plantilla_en.format(constraint=constraint, format_out=fmt)
        
        content_signature = (dominio, prompt_es, constraint)
        if content_signature in hashes_vistos:
            continue
        hashes_vistos.add(content_signature)
        
        registro = {
            "id": f"HEKT-EXT-{id_contador:03d}",
            "domain": dominio,
            "namespace": ns,
            "complexity_level": random.randint(1, 3),
            "language_parity": {
                "es": {
                    "prompt": f"{ns} {prompt_es}",
                    "expected_format": fmt,
                    "target_metric": round(random.uniform(0.80, 0.95), 4)
                },
                "en": {
                    "prompt": f"{ns} {prompt_en}",
                    "expected_format": fmt,
                    "target_metric": round(random.uniform(0.80, 0.95), 4)
                }
            }
        }
        
        dataset.append(registro)
        id_contador += 1

    return dataset

def main():
    os.makedirs("data", exist_ok=True)
    ruta_salida = "data/arca_symbolic_benchmark_extended.jsonl"
    
    print(f"Generando banco de pruebas extendido (120+ casos únicos)...")
    casos = generar_dataset(125)
    
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for item in casos:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"[OK] Dataset generado exitosamente en: {ruta_salida}")
    print(f"Total de casos únicos registrados: {len(casos)}")

if __name__ == "__main__":
    main()
