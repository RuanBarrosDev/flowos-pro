#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aceno — o motor de reativacao de clientes que sumiram (win-back).

100% biblioteca padrao do Python. Offline. Nao acessa a internet.
Todos os dados ficam na pasta .aceno/ na raiz do projeto do usuario.

Uso:
    python3 aceno.py check
    python3 aceno.py termometro
    python3 aceno.py fila [--top N]
    python3 aceno.py registrar --nome "..." --faixa dormindo --canal whatsapp --acao "1o aceno" --resultado pendente [--valor 0]
    python3 aceno.py painel

O ARQUIVO com os clientes e .aceno/clientes.csv (cabecalho abaixo).
NUNCA inventa cliente, data ou valor: se a base esta vazia, avisa.
"""
import sys, os, csv, argparse, unicodedata
from datetime import date, datetime

# ---------- localizacao da pasta de dados (ancorada na raiz do projeto) ----------

def _strip(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s or '')
                   if not unicodedata.combining(c)).lower().strip()

def achar_raiz():
    """Ancora .aceno/ na raiz do projeto: CLAUDE_PROJECT_DIR > .git/.claude > cwd."""
    env = os.environ.get('CLAUDE_PROJECT_DIR')
    if env and os.path.isdir(env):
        return env
    d = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(d, '.git')) or os.path.isdir(os.path.join(d, '.claude')):
            return d
        pai = os.path.dirname(d)
        if pai == d:
            return os.getcwd()
        d = pai

RAIZ = achar_raiz()
DIR = os.path.join(RAIZ, '.aceno')
CLIENTES = os.path.join(DIR, 'clientes.csv')
RESGATES = os.path.join(DIR, 'resgates.csv')
CONFIG = os.path.join(DIR, 'config.md')

CAB_CLIENTES = ['nome', 'contato', 'ultimo_contato', 'valor_total', 'compras', 'status', 'observacao']
CAB_RESGATES = ['data', 'nome', 'faixa', 'canal', 'acao', 'resultado', 'valor_recuperado']

# ---------- config ----------

def ler_config():
    """Le .aceno/config.md no formato '- **Rotulo:** valor' (chave acento-insensivel)."""
    cfg = {}
    if not os.path.exists(CONFIG):
        return cfg
    with open(CONFIG, encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith('-') and ':' in linha:
                corpo = linha.lstrip('-').strip().replace('**', '')
                chave, _, val = corpo.partition(':')
                cfg[_strip(chave)] = val.strip()
    return cfg

def ciclo_dias():
    """Ciclo de recompra do ramo, em dias (default 90)."""
    cfg = ler_config()
    for k in ('ciclo de recompra em dias', 'ciclo de recompra', 'ciclo'):
        if k in cfg:
            try:
                return max(1, int(''.join(ch for ch in cfg[k] if ch.isdigit())))
            except ValueError:
                pass
    return 90

# ---------- parsing ----------

def parse_data(s):
    s = (s or '').strip()
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def parse_valor(s):
    """Aceita '1.234,56' (BR) e '1234.56'."""
    s = (s or '').strip().replace('R$', '').replace(' ', '')
    if not s:
        return 0.0
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    elif '.' in s:
        # so ponto: pode ser decimal (12.50) ou milhar BR (1.200 / 1.200.000).
        # se todo grupo depois de um ponto tem 3 digitos, e separador de milhar.
        partes = s.split('.')
        if len(partes) > 1 and all(len(p) == 3 for p in partes[1:]) and partes[0].isdigit():
            s = ''.join(partes)
    try:
        return float(s)
    except ValueError:
        return 0.0

def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# ---------- faixas de esfriamento ----------

FAIXAS = ['ativo', 'esfriando', 'dormindo', 'perdido']
EMOJI = {'ativo': '🟢', 'esfriando': '🟡', 'dormindo': '🟠', 'perdido': '🔴'}
ROTULO = {'ativo': 'Ativo', 'esfriando': 'Esfriando', 'dormindo': 'Dormindo', 'perdido': 'Perdido'}
# probabilidade heuristica de retorno por faixa (quem esfriou ha pouco volta mais facil)
PROB = {'ativo': 0.0, 'esfriando': 0.70, 'dormindo': 0.40, 'perdido': 0.15}

def faixa_de(dias, ciclo):
    if dias is None:
        return 'perdido'
    if dias < ciclo:
        return 'ativo'
    if dias < 2 * ciclo:
        return 'esfriando'
    if dias < 4 * ciclo:
        return 'dormindo'
    return 'perdido'

def carregar_clientes():
    if not os.path.exists(CLIENTES):
        return []
    with open(CLIENTES, encoding='utf-8') as f:
        return list(csv.DictReader(f))

def enriquecer(hoje=None):
    """Cada cliente ganha: dias (recencia), faixa, valor(float)."""
    hoje = hoje or date.today()
    ciclo = ciclo_dias()
    out = []
    for c in carregar_clientes():
        d = parse_data(c.get('ultimo_contato', ''))
        dias = (hoje - d).days if d else None
        c = dict(c)
        c['_dias'] = dias
        c['_faixa'] = faixa_de(dias, ciclo)
        c['_valor'] = parse_valor(c.get('valor_total', ''))
        out.append(c)
    return out, ciclo

# ---------- comandos ----------

def cmd_check(_):
    print('Aceno — verificacao do ambiente')
    print(f'  Raiz do projeto : {RAIZ}')
    print(f'  Pasta de dados  : {DIR}  ({"existe" if os.path.isdir(DIR) else "NAO existe"})')
    print(f'  Config          : {"ok" if os.path.exists(CONFIG) else "faltando — rode a primeira conversa"}')
    n = len(carregar_clientes())
    print(f'  Clientes na base: {n}')
    print(f'  Ciclo de recompra: {ciclo_dias()} dias')
    if n == 0:
        print('\n  A base esta vazia. Adicione clientes em .aceno/clientes.csv com o cabecalho:')
        print('  ' + ','.join(CAB_CLIENTES))

def cmd_termometro(_):
    clientes, ciclo = enriquecer()
    if not clientes:
        print('Base vazia. Preencha .aceno/clientes.csv antes de medir a temperatura da carteira.')
        return
    cont = {f: 0 for f in FAIXAS}
    valor = {f: 0.0 for f in FAIXAS}
    for c in clientes:
        cont[c['_faixa']] += 1
        valor[c['_faixa']] += c['_valor']
    total = len(clientes)
    print(f'TERMOMETRO DA CARTEIRA  ({total} clientes · ciclo de recompra {ciclo} dias)\n')
    print(f'{"Faixa":<22}{"Clientes":>10}{"%":>7}{"Valor na faixa":>20}')
    print('-' * 59)
    parado = 0.0
    for f in FAIXAS:
        pct = (cont[f] / total * 100) if total else 0
        print(f'{EMOJI[f]} {ROTULO[f]:<19}{cont[f]:>10}{pct:>6.0f}%{brl(valor[f]):>20}')
        if f != 'ativo':
            parado += valor[f]
    print('-' * 59)
    print(f'\n💰 Valor "parado" fora da faixa Ativa (potencial de resgate): {brl(parado)}')
    esf, dor = cont['esfriando'], cont['dormindo']
    if esf or dor:
        print(f'\n👉 Comece pelos {EMOJI["esfriando"]} Esfriando ({esf}) e {EMOJI["dormindo"]} Dormindo ({dor}): '
              'esfriaram ha pouco e voltam com menos esforco. Rode `fila` para a ordem de abordagem.')
    else:
        print('\n👉 Ninguem esfriando ou dormindo agora — carteira saudavel. Volte a medir depois do proximo ciclo.')

def _score(c):
    """Prioridade de abordagem = valor x probabilidade de voltar."""
    return c['_valor'] * PROB.get(c['_faixa'], 0.0)

def cmd_fila(args):
    clientes, ciclo = enriquecer()
    alvos = [c for c in clientes if c['_faixa'] in ('esfriando', 'dormindo', 'perdido')]
    if not alvos:
        print('Nenhum cliente fora da faixa Ativa. Nada a resgatar agora.')
        return
    alvos.sort(key=_score, reverse=True)
    top = alvos[:args.top]
    print(f'FILA DE RESGATE — {len(top)} de {len(alvos)} candidatos, do mais valioso-e-provavel ao menos\n')
    print(f'{"#":>2}  {"Cliente":<24}{"Faixa":<12}{"Sem contato":>12}{"Valor":>14}{"Prioridade":>12}')
    print('-' * 78)
    for i, c in enumerate(top, 1):
        dias = c['_dias']
        d = f'{dias}d' if dias is not None else 'sem data'
        print(f'{i:>2}  {(c.get("nome","?"))[:23]:<24}{EMOJI[c["_faixa"]]+" "+ROTULO[c["_faixa"]]:<12}'
              f'{d:>12}{brl(c["_valor"]):>14}{_score(c):>12.0f}')
    print('\nDica: aborde de cima para baixo. A prioridade pesa o valor do cliente pela '
          'chance de ele voltar (quem esfriou ha menos tempo volta mais facil).')

def cmd_registrar(args):
    if not os.path.isdir(DIR):
        os.makedirs(DIR, exist_ok=True)
    novo = not os.path.exists(RESGATES)
    with open(RESGATES, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if novo:
            w.writerow(CAB_RESGATES)
        w.writerow([date.today().isoformat(), args.nome, _strip(args.faixa), args.canal,
                    args.acao, _strip(args.resultado), parse_valor(str(args.valor))])
    print(f'✔ Registrado: {args.nome} · {args.faixa} · {args.acao} · resultado="{args.resultado}"')

def cmd_painel(_):
    clientes, ciclo = enriquecer()
    print('PAINEL DO ACENO\n')
    if clientes:
        cont = {f: 0 for f in FAIXAS}
        for c in clientes:
            cont[c['_faixa']] += 1
        linha = '  '.join(f'{EMOJI[f]} {cont[f]}' for f in FAIXAS)
        print(f'Carteira ({len(clientes)}):  {linha}')
    if not os.path.exists(RESGATES):
        print('\nNenhum resgate registrado ainda. Use `registrar` a cada aceno enviado para medir o retorno.')
        return
    with open(RESGATES, encoding='utf-8') as f:
        reg = list(csv.DictReader(f))
    abordados = {r['nome'] for r in reg}
    voltaram = [r for r in reg if _strip(r.get('resultado', '')) in ('voltou', 'resgatado', 'comprou')]
    recuperado = sum(parse_valor(r.get('valor_recuperado', '')) for r in voltaram)
    n_ab = len(abordados)
    taxa = (len({r['nome'] for r in voltaram}) / n_ab * 100) if n_ab else 0
    print(f'\nEsforco de resgate:')
    print(f'  Clientes abordados     : {n_ab}')
    print(f'  Voltaram               : {len({r["nome"] for r in voltaram})}')
    print(f'  Taxa de retorno        : {taxa:.0f}%')
    print(f'  Valor recuperado       : {brl(recuperado)}')
    pend = [r for r in reg if _strip(r.get('resultado', '')) == 'pendente']
    if pend:
        print(f'\n⏳ {len(pend)} aceno(s) aguardando resposta — hora do lembrete para quem nao respondeu.')

def main():
    p = argparse.ArgumentParser(description='Aceno — reativacao de clientes (win-back).')
    sub = p.add_subparsers(dest='cmd')
    sub.add_parser('check')
    sub.add_parser('termometro')
    fl = sub.add_parser('fila'); fl.add_argument('--top', type=int, default=10)
    rg = sub.add_parser('registrar')
    rg.add_argument('--nome', required=True); rg.add_argument('--faixa', default='dormindo')
    rg.add_argument('--canal', default='whatsapp'); rg.add_argument('--acao', default='1o aceno')
    rg.add_argument('--resultado', default='pendente'); rg.add_argument('--valor', default='0')
    sub.add_parser('painel')
    args = p.parse_args()
    fn = {'check': cmd_check, 'termometro': cmd_termometro, 'fila': cmd_fila,
          'registrar': cmd_registrar, 'painel': cmd_painel}.get(args.cmd)
    if not fn:
        p.print_help(); return
    fn(args)

if __name__ == '__main__':
    main()
