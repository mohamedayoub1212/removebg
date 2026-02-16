# Replit - Importação manual (quando "repository too big")

Se o Replit não importar do GitHub, crie manualmente:

## Passo a passo

1. **Crie um Repl novo:**
   - Replit → **+ Create Repl**
   - Escolha **Python** (template em branco)
   - Nome: `removebg`
   - Create Repl

2. **Apague** o arquivo `main.py` que vem por padrão

3. **Crie/adicione os arquivos** (copie o conteúdo de cada um):

   - **app.py** – copie de [app.py](app.py)
   - **core.py** – copie de [core.py](core.py)
   - **requirements.txt** – copie de [requirements.txt](requirements.txt)
   - **.replit** – crie com:
     ```
     run = "python app.py"
     entrypoint = "app.py"
     ```

4. **Clique em Run**

5. Aguarde a instalação (2–5 min na primeira vez)

---

**Ou use o método "Upload":** arraste a pasta do projeto para o Replit (se a interface permitir).
