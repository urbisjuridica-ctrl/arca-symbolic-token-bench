#!/usr/bin/env python3
"""
Generador del Banco de Pruebas Núcleo v2.3 para HEKT-NOVA.
Construye un dataset basado exclusivamente en núcleos técnicos únicos y diversos,
descartando variantes artificiales y asegurando paridad lingüística real (ES/EN).
"""

import json
import os

# Banco de núcleos técnicos reales, diversos y sin relleno artificial
CASOS_NUCLEO = [
    {
        "id": "HEKT-CORE-001",
        "domain": "cybersecurity",
        "symbolic_namespace": "[H::SEC]",
        "complexity": 2,
        "language_parity": ["es"],
        "task_type": "incident_analysis",
        "raw_prompt": "Detecté múltiples intentos fallidos de autenticación SSH desde la IP 192.168.1.45 contra la cuenta root en los últimos 4 minutos. El patrón coincide con fuerza bruta. ¿Qué acciones inmediatas recomiendas y cómo debería registrarse el incidente?",
        "compressed_payload": "[H::SEC] INCIDENT ssh_bruteforce src=192.168.1.45 target=root window=4m → actions=[drop, alert_secops, ban_temp] log=structured"
    },
    {
        "id": "HEKT-CORE-002",
        "domain": "cybersecurity",
        "symbolic_namespace": "[H::SEC]",
        "complexity": 2,
        "language_parity": ["en"],
        "task_type": "incident_analysis",
        "raw_prompt": "We are seeing a sudden spike in failed SSH logins from 192.168.1.45 targeting the root account. It looks like a brute-force attempt. What should we do right now and how do we properly log this?",
        "compressed_payload": "[H::SEC] INCIDENT ssh_bruteforce src=192.168.1.45 target=root → immediate=[drop_packet, alert, temp_ban] log_format=json"
    },
    {
        "id": "HEKT-CORE-003",
        "domain": "software_architecture",
        "symbolic_namespace": "[H::ARCH]",
        "complexity": 3,
        "language_parity": ["es"],
        "task_type": "system_design",
        "raw_prompt": "Necesito diseñar el servicio de usuarios. Debe autenticar peticiones, hablar con PostgreSQL y usar Redis para caché de sesiones. Prefiero el patrón Repository y que las dependencias se inyecten. ¿Cómo estructurarías los módulos principales?",
        "compressed_payload": "[H::ARCH] MODULE UserService deps=[AuthMiddleware, PostgresPool, RedisSessionCache] pattern=Repository+DI expose=[getUser, createUser, invalidateSession]"
    },
    {
        "id": "HEKT-CORE-004",
        "domain": "symbolic_logic",
        "symbolic_namespace": "[H::LOGIC]",
        "complexity": 3,
        "language_parity": ["en"],
        "task_type": "formal_proof",
        "raw_prompt": "Given the premises: If A then B, if B then not C, and C or D. Can you prove that A implies D? Please use strict classical logic and show the main steps.",
        "compressed_payload": "[H::LOGIC] PROVE A→D FROM {A→B, B→¬C, C∨D} system=classical proof_style=steps"
    },
    {
        "id": "HEKT-CORE-005",
        "domain": "machine_learning",
        "symbolic_namespace": "[H::ML]",
        "complexity": 2,
        "language_parity": ["es"],
        "task_type": "model_monitoring",
        "raw_prompt": "Tengo un modelo XGBoost que predice si una petición va a cumplir el umbral de fidelidad semántica. Las features son latencia, uso de VRAM y número de tokens. El objetivo es mantener fidelity > 0.81. ¿Qué métricas y checks de drift me recomiendas monitorear en producción?",
        "compressed_payload": "[H::ML] MODEL XGBoost target=semantic_fidelity>0.81 features=[latency_ms, vram_mb, token_count] monitor=[drift, calibration, latency_p99]"
    },
    {
        "id": "HEKT-CORE-006",
        "domain": "database",
        "symbolic_namespace": "[H::DB]",
        "complexity": 2,
        "language_parity": ["en"],
        "task_type": "query_optimization",
        "raw_prompt": "This query is getting slow as the table grows. It filters by status and created_at, then joins with the users table. We need it under 80ms at p95. What indexes and rewriting would you suggest?",
        "compressed_payload": "[H::DB] OPTIMIZE query=filter(status, created_at)+join(users) target_p95=80ms suggest=[indexes, rewrite, covering]"
    },
    {
        "id": "HEKT-CORE-007",
        "domain": "async_systems",
        "symbolic_namespace": "[H::ASYNC]",
        "complexity": 3,
        "language_parity": ["es"],
        "task_type": "pipeline_design",
        "raw_prompt": "Tenemos un pipeline que procesa eventos de pago. Algunos fallan por timeouts de terceros. Quiero reintentos con backoff exponencial, dead-letter queue después de 5 intentos y que el orden por usuario se preserve. ¿Cómo lo modelarías?",
        "compressed_payload": "[H::ASYNC] PIPELINE payment_events retry=exp_backoff max=5 dlq=true ordering=by_user_id guarantee=at_least_once"
    },
    {
        "id": "HEKT-CORE-008",
        "domain": "api_design",
        "symbolic_namespace": "[H::API]",
        "complexity": 1,
        "language_parity": ["en"],
        "task_type": "endpoint_design",
        "raw_prompt": "Design a clean REST endpoint to let a user revoke all active sessions except the current one. It should be safe, idempotent and return how many sessions were revoked.",
        "compressed_payload": "[H::API] ENDPOINT DELETE /users/me/sessions?except=current auth=required idempotent=true response={revoked_count}"
    }
]

def main():
    print(f"Generando dataset purificado v2.3 con {len(CASOS_NUCLEO)} núcleos únicos...")
    os.makedirs("data", exist_ok=True)
    ruta_salida = "data/arca_symbolic_benchmark_extended.jsonl"
    
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for c in CASOS_NUCLEO:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"[OK] Dataset núcleo v2.3 generado exitosamente en: {ruta_salida}")

if __name__ == "__main__":
    main()
