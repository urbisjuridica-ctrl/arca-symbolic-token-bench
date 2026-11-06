import time
import torch
import json
import os

def monitor_gpu_performance():
    print("Inicializando monitor de telemetría VRAM (PyTorch)...")
    
    # Verificar disponibilidad de GPU CUDA
    if not torch.cuda.is_available():
        print("[AVISO] No se detectó ninguna GPU CUDA activa. Ejecutando en modo simulación CPU.")
        device = torch.device("cpu")
    else:
        device = torch.device("cuda")
        torch.cuda.reset_peak_memory_stats(device)
        print(f"[OK] Dispositivo activo: {torch.cuda.get_device_name(0)}")

    input_path = "data/arca_symbolic_benchmark.jsonl"
    if not os.path.exists(input_path):
        print(f"Error: No se encuentra el archivo en {input_path}")
        return

    print("\nEjecutando pruebas de rendimiento y consumo de memoria...\n")
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            
            # Simulación de carga en GPU para benchmark de tokens crudos vs simbólicos
            start_time = time.time()
            
            if device.type == "cuda":
                # Limpiar caché previa para medición limpia
                torch.cuda.empty_cache()
                start_vram = torch.cuda.memory_allocated(device)
                
                # Simular asignación de tensores basada en el tamaño del prompt
                dummy_tensor = torch.randn((len(record["raw_prompt"]) * 128, 512), device=device)
                peak_vram = torch.cuda.max_memory_allocated(device) / (1024 * 1024) # en MB
                del dummy_tensor
                torch.cuda.empty_cache()
            else:
                peak_vram = 0.0

            # Medir latencia simulada de inferencia
            time.sleep(0.02) # Simulación de tiempo de procesamiento por bloque
            latency_ms = (time.time() - start_time) * 1000

            print(f"[{record['id']}] Dominio: {record['domain']}")
            print(f"  - VRAM Pico Registrada: {peak_vram:.2f} MB")
            print(f"  - Latencia Estimada:    {latency_ms:.2f} ms\n")

    if device.type == "cuda":
        max_global_vram = torch.cuda.max_memory_reserved(device) / (1024 * 1024)
        print("=" * 40)
        print(f"ESTadísticas DE HARDWARE HEKT-NOVA:")
        print(f"  - VRAM Máxima Reservada en GPU: {max_global_vram:.2f} MB")
        print("=" * 40)

if __name__ == "__main__":
    monitor_gpu_performance()
