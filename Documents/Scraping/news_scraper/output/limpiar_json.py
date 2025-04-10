import json

entrada = "output/articles.jsonl"
salida = "output/articles_limpio.jsonl"

urls_vistas = set()
articulos_limpios = []

with open(entrada, "r", encoding="utf-8") as f:
    for linea in f:
        try:
            articulo = json.loads(linea.strip())
            url = articulo.get("url")
            if url and url not in urls_vistas:
                urls_vistas.add(url)
                articulos_limpios.append(articulo)
        except json.JSONDecodeError:
            print("❌ Línea con error de formato JSON omitida.")

with open(salida, "w", encoding="utf-8") as f:
    for articulo in articulos_limpios:
        f.write(json.dumps(articulo, ensure_ascii=False) + "\n")

print(f"✅ Archivo limpio guardado como: {salida}")
print(f"📦 Artículos únicos: {len(articulos_limpios)}")
