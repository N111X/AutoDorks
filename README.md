# Herramienta Avanzada para Dorking y Automatizacion de Busquedas

Desarrollado por: **N111X**

La herramienta **DorksAuto.py** permite realizar **Dorking** y **automatizacion de busquedas** de manera eficiente. Puedes configurar busquedas avanzadas utilizando diferentes parametros y exportar los resultados en diversos formatos. Ademas, incluye la capacidad de automatizar busquedas mediante Selenium.

## Requisitos

- Python 3.x
- Selenium (si se usa la opcion `--selenium`)
- Librerias necesarias: 
  ```bash
  requests~=2.32.3
  python-dotenv~=1.0.1
  rich~=13.9.4
  gpt4all~=2.8.2
  openai~=1.59.7
  transformers~=4.48.0


## Uso

### Argumentos disponibles:

### 1. `-q` / `--query`
Especifica el **Dork** a realizar. Puedes usar un Dork como ejemplo: `intitle:"index of" filetype:sql`.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql"
```

### 2. `-c` / `--configure`
Configura el archivo `.env` para definir tus claves API y el ID de motor de busqueda.

**Ejemplo**:
```bash
python DorksAuto.py -c
```

### 3. `-sp` / `--start-page`
Especifica la **pagina de inicio** para obtener los resultados. El valor por defecto es `1`.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -sp 2
```

### 4. `-p` / `--pages`
Especifica el numero de **paginas de resultados** a obtener. El valor por defecto es `1`.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -p 5
```

### 5. `-l` / `--language`
Especifica el **idioma** de los resultados. El valor por defecto es `lang_es` (espanol).

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -l "lang_en"
```

### 6. `-j` / `--json`
Especifica el **archivo de salida** en formato JSON.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -j resultados.json
```

### 7. `-html` / `--html`
Especifica el **archivo de salida** en formato HTML.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -html resultados.html
```

### 8. `-d` / `--download`
Especifica los **tipos de archivos** a descargar (por ejemplo, `pdf`, `zip`, `sql`).

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -d "pdf,zip"
```

### 9. `-gd` / `--generate-dork`
Genera un **Dork automaticamente** usando IA. Ejemplo: `dork para contrasenas en texto plano`.

**Ejemplo**:
```bash
python DorksAuto.py -gd "dork para contrasenas en texto plano"
```

### 10. `-s` / `--selenium`
Activa **Selenium** para realizar busquedas automatizadas en el navegador.

**Ejemplo**:
```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -s
```

## Ejemplo completo

```bash
python DorksAuto.py -q "intitle:\"index of\" filetype:sql" -p 5 -l "lang_en" -j "resultados.json" -d "pdf,zip" -s
```

Este comando realiza una busqueda con el Dork especificado, obtiene 5 paginas de resultados en ingles, guarda los resultados en un archivo JSON, descarga archivos PDF y ZIP, y utiliza Selenium para realizar las busquedas automaticamente en el navegador.

## Configuracion del archivo `.env`

Asegurate de configurar tus claves API y el ID del motor de busqueda en el archivo `.env` generado al usar la opcion `-c`.

## Licencia

Este proyecto esta licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para mas detalles.
