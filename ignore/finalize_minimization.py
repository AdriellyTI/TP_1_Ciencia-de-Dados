import shutil
from pathlib import Path
import pandas as pd
import json

ignore_dir = Path("projeto/ignore")
ignore_dir.mkdir(parents=True, exist_ok=True)

# 1. Move temporary check scripts to ignore
temp_scripts = [
    "check_tse.py", "check_candidatos.py", "check_cargo.py",
    "check_cargo2.py", "check_cargo3.py", "create_tse_derivada.py"
]
print("=== MOVING TEMP SCRIPTS ===")
for script in temp_scripts:
    src = Path(script)
    if src.exists():
        dest = ignore_dir / script
        shutil.move(str(src), str(dest))
        print(f"  {script} -> ignore/{script}")

# 2. Update proveniencia.csv with TSE derived table entry
print("\n=== UPDATING PROVENIENCIA ===")
prov_file = Path("projeto/documentacao/proveniencia.csv")
if prov_file.exists():
    with open(prov_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"Current proveniencia.csv has {len(content.split(chr(10)))} lines")
    
    # Add TSE derived table entry
    new_entry = '4,TSE/Dados Abertos,Derived table,"projeto/dados_tratados/tse_derivada_presidentes_governadores.csv","2026-09-19T00:00:00-03:00","America/Sao_Paulo","Candidatos-{ano} ZIP extraction","Filtered CD_CARGO IN (1,3), CD_SIT_TOT_TURNO=1, no personal data","projeto/dados_tratados/tse_derivada_presidentes_governadores.csv",200,452,"1994-2022","TSE Candidatos data filtered for elected presidents and governors only; personal data excluded (CPF, birth date, etc.); derived table created from raw ZIP extraction"'
    
    if "4,TSE/Dados Abertos,Derived" not in content:
        content = content.rstrip("\n") + "\n" + new_entry + "\n"
        with open(prov_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("Added derived table entry")
    else:
        print("Entry already exists")

# 3. Update README.md with minimization note
print("\n=== UPDATING README ===")
readme = Path("projeto/README.md")
if readme.exists():
    content = readme.read_text(encoding="utf-8")
    if "Minimização" not in content:
        addition = """
## Minimização de dados TSE

A coleta original do TSE totalizou **6.38 GB** (272 arquivos ZIP/CSV). Para o propósito analítico do projeto — estudar a relação entre preços da cesta básica, inflação e períodos de governos presidenciais/estaduais — apenas uma fração mínima desses dados é necessária.

**Dados mantidos para análise:**
- `tse_derivada_presidentes_governadores.csv` — 452 registros de presidentes e governadores eleitos (1994-2022), com partido, UF e coligação

**Dados descartados da análise (mantidos apenas como referência bruta):**
- Votação por seção eleitoral (~1.9 GB) — granularidade excessiva, sem relação direta com a análise
- Votação nominal por município/zona (~1.7 GB) — granularidade excessiva
- Votação por partido por município/zona (~111 MB) — granularidade excessiva
- Bens de candidatos (~26 MB) — dados pessoais/financeiros, sem relação com a análise
- Detalhes de apuração por município/zona (~28 MB) — granularidade excessiva
- Notas fiscais de candidatos (~28 MB) — dados financeiros pessoais
- Coligações (~3 MB) — parcialmente relevante, já refletido nos dados derivados
- Informações complementares, fotos, propostas, certidões criminais, redes sociais — não relevantes para análise

**Justificativa:** A base derivada contém apenas variáveis necessárias para contextualizar períodos de governo e espectros partidários. Dados pessoais (CPF, data de nascimento, título eleitoral, etc.) foram excluídos conforme princípios de minimização da LGPD.

"""
        # Insert before any trailing content
        content = content.rstrip("\n") + "\n" + addition
        readme.write_text(content, encoding="utf-8")
        print("README.md updated with minimization note")
    else:
        print("README.md already has minimization note")

# 4. Update dataset_card.md
print("\n=== UPDATING DATASET CARD ===")
card = Path("projeto/documentacao/dataset_card.md")
if card.exists():
    content = card.read_text(encoding="utf-8")
    
    # Update Fonte 3 section
    old_tse = "### Fonte 3 — TSE/Dados Abertos (API)"
    if old_tse in content:
        new_tse = """### Fonte 3 — TSE/Dados Abertos (API)

> **Minimização de dados:** A coleta original totalizou ~6.38 GB (272 arquivos). Para a análise final, foram utilizados apenas dados de candidatos eleitos (presidentes e governadores), extraídos via API CKAN. Dados pessoais (CPF, nascimento, título eleitoral, etc.), votação detalhada por seção, notas fiscais e outros dados operacionais foram descartados. A base derivada contém apenas as variáveis necessárias para contextualizar períodos de governo e espectros partidários."""
        content = content.replace(old_tse, new_tse)
    
    # Update Dados descartados section
    old_discarded = "### Dados descartados\n\n`[Descrever os registros, colunas ou períodos removidos e justificar cada descarte. Caso nenhum dado tenha sido descartado, informar \"Nenhum dado descartado\"]`"
    new_discarded = """### Dados descartados

**TSE/Dados Abertos:**
- Votação por seção eleitoral (1998-2022): ~1.9 GB — granularidade excessiva, sem relação direta com a análise de inflação/ governos
- Votação nominal por município/zona (1994-2022): ~1.7 GB — granularidade excessiva
- Votação por partido por município/zona (1994-2022): ~111 MB — granularidade excessiva
- Bens de candidatos (2006-2022): ~26 MB — dados pessoais/financeiros sem relação com análise
- Notas fiscais de candidatos (2018): ~28 MB — dados financeiros pessoais
- Informações complementares, fotos, propostas, certidões criminais, redes sociais: não relevantes
- Detalhes de apuração por município/zona (1994-2022): ~28 MB — granularidade excessiva

**Justificativa:** A base derivada contém apenas variáveis necessárias para contextualizar períodos de governo e espectros partidários. Dados pessoais excluídos conforme LGPD (art. 6, III — minimização).

**IBGE/SIDRA e DIEESE:** Nenhum dado descartado — coleta já limitada ao escopo analítico."""
    if old_discarded in content:
        content = content.replace(old_discarded, new_discarded)
        print("  Updated 'Dados descartados' section")
    
    # Update A.7 Arquivos da entrega
    old_files = "| Dados brutos da API (TSE/Dados Abertos) | `../dados_brutos/tse/[arquivos ZIP CSV]` | `[A preencher]` |"
    new_files = "| Dados brutos da API (TSE/Dados Abertos) | `../dados_brutos/tse/` (272 arquivos, referência apenas) | `[A preencher]` |\n| Base derivada TSE | `../dados_tratados/tse_derivada_presidentes_governadores.csv/.parquet` | `[A preencher]` |"
    if old_files in content:
        content = content.replace(old_files, new_files)
        print("  Updated 'Arquivos da entrega' section")
    
    # Update proveniencia reference
    old_prov = "| Registro de proveniência | `proveniencia.csv` | `[A preencher]` |"
    new_prov = "| Registro de proveniência | `proveniencia.csv` | `[A preencher]` |\n| Registro de proveniência (TSE detalhado) | `proveniencia_tse.csv` (em dados_brutos/proveniencia/) | `[A preencher]` |"
    if old_prov in content:
        content = content.replace(old_prov, new_prov)
        print("  Updated proveniência reference")
    
    with open(card, "w", encoding="utf-8") as f:
        f.write(content)
    print("dataset_card.md updated")

print("\n=== DONE ===")
