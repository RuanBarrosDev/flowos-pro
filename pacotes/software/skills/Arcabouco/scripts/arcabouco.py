#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arcabouço — motor determinístico do modelo de dados.

Este script NÃO conversa nem inventa nada. Ele lê UM arquivo de modelo
(`.arcabouco/modelo.json`) — a única fonte da verdade — e faz quatro coisas,
sempre iguais para o mesmo modelo:

  validar     confere a integridade do modelo (chaves, relações, tipos de dinheiro…)
  mermaid     desenha o diagrama entidade-relação (texto Mermaid, cola em qualquer lugar)
  sql         gera o CREATE TABLE (SQLite / PostgreSQL / MySQL) com chaves, índices e travas
  dicionario  escreve o dicionário de dados em português claro (uma linha por campo)
  semear      gera linhas de exemplo (INSERT) para você testar o modelo

A IA (o Claude) é quem conversa com o dono, entende o negócio e ESCREVE o
modelo.json. O motor só GARANTE que o que sai (diagrama, SQL, dicionário) é
correto e consistente com o modelo — e trava quando algo não fecha.

Uso:
    python3 arcabouco.py validar     [caminho_do_modelo.json]
    python3 arcabouco.py mermaid      [caminho]
    python3 arcabouco.py sql          [caminho] [--dialeto sqlite|postgres|mysql]
    python3 arcabouco.py dicionario   [caminho]
    python3 arcabouco.py semear       [caminho] [--por N]

Sem caminho, procura ./.arcabouco/modelo.json a partir da pasta atual.
Feito só com a biblioteca padrão do Python (nada para instalar).
"""

import sys
import os
import json
import re

CAMINHO_PADRAO = os.path.join(".arcabouco", "modelo.json")

# ---------------------------------------------------------------------------
# Tipos abstratos em português -> tipo real de cada banco.
# O dono escolhe de um cardápio simples; o motor traduz e força as boas regras
# (dinheiro é SEMPRE decimal, nunca "float" — senão o centavo se perde).
# ---------------------------------------------------------------------------
TIPOS = {
    # nome_pt : (sqlite, postgres, mysql)
    "id":          ("INTEGER",        "BIGINT",        "BIGINT"),
    "texto":       ("TEXT",           "VARCHAR(255)",  "VARCHAR(255)"),
    "texto_longo": ("TEXT",           "TEXT",          "TEXT"),
    "numero":      ("INTEGER",        "INTEGER",       "INT"),
    "decimal":     ("DECIMAL(12,2)",  "DECIMAL(12,2)", "DECIMAL(12,2)"),
    "dinheiro":    ("DECIMAL(12,2)",  "DECIMAL(12,2)", "DECIMAL(12,2)"),
    "booleano":    ("INTEGER",        "BOOLEAN",       "TINYINT(1)"),
    "data":        ("DATE",           "DATE",          "DATE"),
    "datahora":    ("DATETIME",       "TIMESTAMP",     "DATETIME"),
    "opcao":       ("TEXT",           "VARCHAR(50)",   "VARCHAR(50)"),
    "ref":         ("INTEGER",        "BIGINT",        "BIGINT"),
}
TIPOS_DINHEIRO = ("dinheiro", "decimal")
# nomes de coluna que "cheiram" a dinheiro — se não forem dinheiro/decimal, avisamos
PALAVRAS_DINHEIRO = ("preco", "preço", "valor", "total", "salario", "salário",
                     "custo", "receita", "lucro", "desconto", "saldo", "montante")

VERDE, VERM, AMAR, CINZA, FIM = "\033[92m", "\033[91m", "\033[93m", "\033[90m", "\033[0m"


# ---------------------------------------------------------------------------
# Leitura do modelo
# ---------------------------------------------------------------------------
def resolver_caminho(args):
    """Aceita um caminho explícito; senão usa ./.arcabouco/modelo.json."""
    for a in args:
        if not a.startswith("--") and a.endswith(".json"):
            return a
    return CAMINHO_PADRAO


def carregar(caminho):
    if not os.path.exists(caminho):
        print(f"{VERM}✗ Não achei o modelo em '{caminho}'.{FIM}")
        print(f"  Peça ao Claude para criar o modelo primeiro (modo 'modelar'),")
        print(f"  ou passe o caminho certo: python3 arcabouco.py <comando> <caminho.json>")
        sys.exit(2)
    try:
        with open(caminho, encoding="utf-8") as f:
            m = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{VERM}✗ O modelo '{caminho}' não é um JSON válido: {e}{FIM}")
        sys.exit(2)
    if not isinstance(m, dict) or "tabelas" not in m:
        print(f"{VERM}✗ O modelo precisa ter uma lista 'tabelas'.{FIM}")
        sys.exit(2)
    return m


def snake_ok(nome):
    """True se o nome está em snake_case simples (minúsculas, _, dígitos, sem acento/espaço)."""
    return bool(re.fullmatch(r"[a-z][a-z0-9_]*", nome or ""))


def tem_pk(tabela):
    for c in tabela.get("colunas", []):
        if c.get("pk") or c.get("tipo") == "id":
            return True
    return False


def indice_tabelas(m):
    return {t.get("nome"): t for t in m.get("tabelas", []) if t.get("nome")}


# ---------------------------------------------------------------------------
# validar
# ---------------------------------------------------------------------------
def cmd_validar(m):
    erros, avisos = [], []
    tabs = m.get("tabelas", [])
    nomes_tab = [t.get("nome") for t in tabs]

    # tabelas duplicadas
    vistos = set()
    for n in nomes_tab:
        if not n:
            erros.append("Existe uma tabela sem 'nome'.")
        elif n in vistos:
            erros.append(f"Tabela '{n}' aparece mais de uma vez.")
        else:
            vistos.add(n)

    idx = indice_tabelas(m)

    for t in tabs:
        tn = t.get("nome", "?")
        cols = t.get("colunas", [])
        if not cols:
            erros.append(f"Tabela '{tn}' não tem nenhuma coluna.")
        if not tem_pk(t):
            erros.append(f"Tabela '{tn}' não tem chave primária (nenhuma coluna 'id' nem pk:true). "
                         f"Toda tabela precisa de uma chave que identifique cada linha.")
        if not snake_ok(tn):
            avisos.append(f"Nome de tabela '{tn}' fora do padrão. Prefira minúsculas sem acento "
                          f"(ex.: 'ordens_servico').")

        col_vistos = set()
        for c in cols:
            cn = c.get("nome")
            tipo = c.get("tipo")
            if not cn:
                erros.append(f"Tabela '{tn}' tem uma coluna sem 'nome'.")
                continue
            if cn in col_vistos:
                erros.append(f"Coluna '{cn}' repetida na tabela '{tn}'.")
            col_vistos.add(cn)
            if tipo not in TIPOS:
                erros.append(f"Coluna '{tn}.{cn}' usa tipo desconhecido '{tipo}'. "
                             f"Tipos válidos: {', '.join(TIPOS)}.")
            if not snake_ok(cn):
                avisos.append(f"Nome de coluna '{tn}.{cn}' fora do padrão (minúsculas sem acento).")

            # chave estrangeira (ref) tem que apontar para tabela.coluna existente
            if tipo == "ref":
                ref = c.get("ref")
                if not ref or "." not in str(ref):
                    erros.append(f"Coluna '{tn}.{cn}' é uma referência (ref) mas não diz para onde "
                                 f"aponta. Use \"ref\": \"outra_tabela.id\".")
                else:
                    alvo_t, alvo_c = str(ref).split(".", 1)
                    if alvo_t not in idx:
                        erros.append(f"A referência '{tn}.{cn}' aponta para a tabela '{alvo_t}', "
                                     f"que não existe no modelo.")
                    else:
                        alvo_cols = [x.get("nome") for x in idx[alvo_t].get("colunas", [])]
                        if alvo_c not in alvo_cols:
                            erros.append(f"A referência '{tn}.{cn}' aponta para "
                                         f"'{alvo_t}.{alvo_c}', mas essa coluna não existe.")

            # dinheiro pelo nome, tipo errado
            base = (cn or "").lower()
            if any(p in base for p in PALAVRAS_DINHEIRO) and tipo not in TIPOS_DINHEIRO:
                avisos.append(f"'{tn}.{cn}' parece ser dinheiro mas está como '{tipo}'. "
                              f"Use o tipo 'dinheiro' (senão você perde os centavos).")

            # opcao sem lista de opções
            if tipo == "opcao" and not c.get("opcoes"):
                avisos.append(f"'{tn}.{cn}' é do tipo 'opcao' mas não listou as opções "
                              f"(ex.: \"opcoes\": [\"aberto\",\"pago\"]).")

    # relatório
    print(f"\n{CINZA}Arcabouço — validação do modelo '{m.get('projeto','(sem nome)')}'{FIM}")
    print(f"{CINZA}{len(tabs)} tabela(s).{FIM}\n")
    for e in erros:
        print(f"{VERM}✗ ERRO  {FIM}{e}")
    for a in avisos:
        print(f"{AMAR}⚠ aviso {FIM}{a}")
    if not erros and not avisos:
        print(f"{VERDE}✓ Modelo íntegro. Todas as tabelas têm chave, as relações fecham "
              f"e o dinheiro está protegido.{FIM}")
    elif not erros:
        print(f"\n{VERDE}✓ Sem erros graves — só avisos acima para você decidir.{FIM}")
    else:
        print(f"\n{VERM}Corrija os {len(erros)} erro(s) antes de gerar o SQL.{FIM}")
    print()
    sys.exit(1 if erros else 0)


# ---------------------------------------------------------------------------
# mermaid  (diagrama entidade-relação)
# ---------------------------------------------------------------------------
def cmd_mermaid(m):
    linhas = ["erDiagram"]
    for t in m.get("tabelas", []):
        tn = t.get("nome", "tabela")
        linhas.append(f"    {tn} {{")
        for c in t.get("colunas", []):
            tipo = c.get("tipo", "texto")
            cn = c.get("nome", "campo")
            marca = ""
            if c.get("pk") or tipo == "id":
                marca = "PK"
            elif tipo == "ref":
                marca = "FK"
            elif c.get("unico"):
                marca = "UK"
            linhas.append(f"        {tipo} {cn} {marca}".rstrip())
        linhas.append("    }")
    # relações: cada ref (filho) -> pai
    for t in m.get("tabelas", []):
        filho = t.get("nome")
        for c in t.get("colunas", []):
            if c.get("tipo") == "ref" and c.get("ref") and "." in str(c["ref"]):
                pai = str(c["ref"]).split(".", 1)[0]
                rotulo = c.get("rotulo") or "tem"
                # pai UM-para-MUITOS filho:  pai ||--o{ filho
                linhas.append(f'    {pai} ||--o{{ {filho} : "{rotulo}"')
    print("\n".join(linhas))


# ---------------------------------------------------------------------------
# sql  (CREATE TABLE por dialeto)
# ---------------------------------------------------------------------------
def tipo_sql(coluna, dialeto):
    i = {"sqlite": 0, "postgres": 1, "mysql": 2}[dialeto]
    tipo = coluna.get("tipo", "texto")
    return TIPOS.get(tipo, TIPOS["texto"])[i]


def linha_coluna(coluna, dialeto):
    cn = coluna["nome"]
    tipo = coluna.get("tipo", "texto")
    partes = [cn, tipo_sql(coluna, dialeto)]

    # id -> chave primária autoincremento (varia por banco)
    if tipo == "id" or (coluna.get("pk") and tipo == "id"):
        if dialeto == "sqlite":
            return f"{cn} INTEGER PRIMARY KEY AUTOINCREMENT"
        if dialeto == "postgres":
            return f"{cn} BIGSERIAL PRIMARY KEY"
        return f"{cn} BIGINT AUTO_INCREMENT PRIMARY KEY"

    if coluna.get("nn"):
        partes.append("NOT NULL")
    if coluna.get("unico"):
        partes.append("UNIQUE")
    if tipo == "opcao" and coluna.get("opcoes"):
        ops = ", ".join("'" + str(o).replace("'", "''") + "'" for o in coluna["opcoes"])
        partes.append(f"CHECK ({cn} IN ({ops}))")
    if "default" in coluna and coluna["default"] is not None:
        d = coluna["default"]
        if d == "agora":
            partes.append("DEFAULT CURRENT_TIMESTAMP")
        elif isinstance(d, str):
            partes.append("DEFAULT '" + d.replace("'", "''") + "'")
        else:
            partes.append(f"DEFAULT {d}")
    return " ".join(partes)


def cmd_sql(m, dialeto):
    if dialeto not in ("sqlite", "postgres", "mysql"):
        print(f"{VERM}✗ Dialeto '{dialeto}' inválido. Use sqlite, postgres ou mysql.{FIM}")
        sys.exit(2)
    out = [f"-- Arcabouço — SQL do modelo '{m.get('projeto','(sem nome)')}' ({dialeto})",
           "-- Gerado a partir de .arcabouco/modelo.json — a fonte da verdade.",
           ""]
    idx = indice_tabelas(m)
    indices = []
    for t in m.get("tabelas", []):
        tn = t["nome"]
        linhas_col = []
        pks_extra = [c["nome"] for c in t.get("colunas", [])
                     if c.get("pk") and c.get("tipo") != "id"]
        for c in t.get("colunas", []):
            linhas_col.append("    " + linha_coluna(c, dialeto))
        # chaves estrangeiras como restrição de tabela
        for c in t.get("colunas", []):
            if c.get("tipo") == "ref" and c.get("ref") and "." in str(c["ref"]):
                alvo_t, alvo_c = str(c["ref"]).split(".", 1)
                ao_apagar = c.get("ao_apagar")  # 'cascata' | 'nulo' | None
                clausula = ""
                if ao_apagar == "cascata":
                    clausula = " ON DELETE CASCADE"
                elif ao_apagar == "nulo":
                    clausula = " ON DELETE SET NULL"
                linhas_col.append(
                    f"    FOREIGN KEY ({c['nome']}) REFERENCES {alvo_t}({alvo_c}){clausula}")
                indices.append(f"CREATE INDEX idx_{tn}_{c['nome']} ON {tn} ({c['nome']});")
        # chave primária composta (mais de uma coluna pk que não seja id)
        if len(pks_extra) >= 1 and not any(
                (c.get("tipo") == "id") for c in t.get("colunas", [])):
            linhas_col.append(f"    PRIMARY KEY ({', '.join(pks_extra)})")

        out.append(f"CREATE TABLE {tn} (")
        out.append(",\n".join(linhas_col))
        out.append(");")
        out.append("")
    if indices:
        out.append("-- Índices nas chaves estrangeiras (buscas e junções ficam rápidas)")
        out.extend(indices)
        out.append("")
    print("\n".join(out))


# ---------------------------------------------------------------------------
# dicionario  (uma linha por campo, em português claro)
# ---------------------------------------------------------------------------
NOME_AMIGAVEL = {
    "id": "número de identificação",
    "texto": "texto curto",
    "texto_longo": "texto longo",
    "numero": "número inteiro",
    "decimal": "número com casas decimais",
    "dinheiro": "valor em dinheiro (R$)",
    "booleano": "sim/não",
    "data": "data",
    "datahora": "data e hora",
    "opcao": "opção de uma lista",
    "ref": "ligação com outra tabela",
}


def cmd_dicionario(m):
    print(f"# Dicionário de dados — {m.get('projeto','(sem nome)')}\n")
    print("Cada tabela é uma *coisa* que o sistema guarda. Cada campo é uma *informação* dessa coisa.\n")
    for t in m.get("tabelas", []):
        print(f"## {t.get('nome')}")
        if t.get("descricao"):
            print(f"\n{t['descricao']}\n")
        print("| Campo | O que é | Tipo | Obrigatório |")
        print("|-------|---------|------|-------------|")
        for c in t.get("colunas", []):
            tipo = c.get("tipo", "texto")
            amig = NOME_AMIGAVEL.get(tipo, tipo)
            if tipo == "ref" and c.get("ref"):
                amig = f"ligação com **{str(c['ref']).split('.')[0]}**"
            if tipo == "opcao" and c.get("opcoes"):
                amig = "uma de: " + ", ".join(str(o) for o in c["opcoes"])
            obg = "sim" if (c.get("nn") or c.get("pk") or tipo == "id") else "não"
            desc = c.get("descricao", "")
            print(f"| `{c.get('nome')}` | {desc} | {amig} | {obg} |")
        print()


# ---------------------------------------------------------------------------
# semear  (linhas de exemplo para testar)
# ---------------------------------------------------------------------------
def valor_exemplo(coluna, i):
    tipo = coluna.get("tipo", "texto")
    cn = coluna.get("nome", "campo")
    if tipo == "opcao" and coluna.get("opcoes"):
        ops = coluna["opcoes"]
        return "'" + str(ops[i % len(ops)]).replace("'", "''") + "'"
    if tipo in ("dinheiro", "decimal"):
        return f"{100 + i * 10}.00"
    if tipo == "numero":
        return str(i + 1)
    if tipo == "booleano":
        return "1" if i % 2 == 0 else "0"
    if tipo == "data":
        return f"'2026-01-{(i % 27) + 1:02d}'"
    if tipo == "datahora":
        return f"'2026-01-{(i % 27) + 1:02d} 10:00:00'"
    if tipo == "ref":
        return str((i % 3) + 1)  # supõe que o pai tenha ids 1..3
    return f"'{cn} exemplo {i + 1}'"


def cmd_semear(m, por):
    print(f"-- Arcabouço — dados de exemplo ({por} por tabela) para testar o modelo")
    print("-- Insira as tabelas 'pai' antes das 'filho' (referências).\n")
    for t in m.get("tabelas", []):
        tn = t["nome"]
        cols = [c for c in t.get("colunas", []) if c.get("tipo") != "id"]
        nomes = ", ".join(c["nome"] for c in cols)
        for i in range(por):
            vals = ", ".join(valor_exemplo(c, i) for c in cols)
            print(f"INSERT INTO {tn} ({nomes}) VALUES ({vals});")
        print()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    comando = args[0]
    resto = args[1:]
    caminho = resolver_caminho(resto)

    if comando == "validar":
        cmd_validar(carregar(caminho))
    elif comando == "mermaid":
        cmd_mermaid(carregar(caminho))
    elif comando == "sql":
        dialeto = "sqlite"
        if "--dialeto" in resto:
            k = resto.index("--dialeto")
            if k + 1 < len(resto):
                dialeto = resto[k + 1]
        else:
            dialeto = (carregar(caminho).get("engine") or "sqlite")
        cmd_sql(carregar(caminho), dialeto)
    elif comando == "dicionario":
        cmd_dicionario(carregar(caminho))
    elif comando == "semear":
        por = 3
        if "--por" in resto:
            k = resto.index("--por")
            if k + 1 < len(resto):
                try:
                    por = max(1, int(resto[k + 1]))
                except ValueError:
                    pass
        cmd_semear(carregar(caminho), por)
    else:
        print(f"{VERM}Comando '{comando}' desconhecido.{FIM} "
              f"Use: validar | mermaid | sql | dicionario | semear")
        sys.exit(2)


if __name__ == "__main__":
    main()
