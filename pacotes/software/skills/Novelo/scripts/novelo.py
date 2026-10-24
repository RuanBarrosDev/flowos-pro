#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novelo — cartógrafo e desemaranhador de projetos.

Motor determinístico, só biblioteca padrão (stdlib), 100% offline.
Ele NÃO escreve nem reescreve o seu código: ele LÊ os arquivos que já
existem na sua máquina e monta o inventário, o grafo de conexões e a lista
de "nós" (bagunça) para a IA explicar em português e planejar a limpeza.

Regra de ouro do motor: nunca inventa arquivo, função ou conexão — só
reporta o que está de fato nos arquivos. Toda heurística incerta é marcada
como "possível — confirme". Segredo achado no código é sempre MASCARADO.

Comandos:
  setup       grava a configuração do projeto e se autodestrói
  mapear      inventaria os arquivos e gera o esqueleto do mapa (mapa.md)
  fios        monta o grafo de conexões (quem usa quem) + diagrama Mermaid
  nos         detecta a bagunça: código morto, duplicação, arquivo gigante,
              segredo no código, falta de teste, arquivo-mistério
  rumo        "onde eu mexo pra fazer X?" — aponta os arquivos prováveis
  plano       plano de limpeza em passos pequenos e seguros (plano.md)
  painel      resumo do estado: mapeado, nós em aberto, próximo passo
"""

import sys, os, re, csv, json, argparse, subprocess, unicodedata
from pathlib import Path
from datetime import datetime

# --------------------------------------------------------------------------
# Constantes
# --------------------------------------------------------------------------
IGNORE_DIRS = {
    '.git', '.hg', '.svn', '.venv', 'venv', 'env', '.env.d', 'node_modules',
    'dist', 'build', 'target', 'vendor', '__pycache__', '.novelo', '.claude',
    '.next', '.nuxt', 'out', 'coverage', '.idea', '.vscode', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'bower_components', '.cache', '.parcel-cache',
    '.gradle', 'Pods', '.terraform', '.expo', '.turbo', 'site-packages',
}
CODE_EXT = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.mjs', '.cjs', '.java', '.go', '.rb',
    '.php', '.rs', '.c', '.cc', '.cpp', '.h', '.hpp', '.cs', '.swift', '.kt',
    '.kts', '.vue', '.svelte', '.sql', '.sh', '.bash', '.html', '.css', '.scss',
    '.less', '.dart', '.scala', '.ex', '.exs', '.lua', '.r', '.pl', '.m',
}
NOTABLE_CONFIG = {
    'package.json', 'requirements.txt', 'pyproject.toml', 'setup.py', 'Cargo.toml',
    'go.mod', 'Gemfile', 'composer.json', 'docker-compose.yml', 'docker-compose.yaml',
    'Dockerfile', 'tsconfig.json', 'vite.config.js', 'vite.config.ts', 'webpack.config.js',
    'next.config.js', 'nuxt.config.js', 'Makefile', 'manage.py', 'wsgi.py', 'asgi.py',
    'app.py', 'main.py', 'index.js', 'index.ts', 'server.js', 'server.ts', '.env',
    '.env.example', 'README.md', 'CLAUDE.md',
}
ENTRY_NAMES = {
    'main.py', 'app.py', '__main__.py', 'manage.py', 'wsgi.py', 'asgi.py', 'run.py',
    'server.py', 'index.js', 'index.ts', 'main.js', 'main.ts', 'app.js', 'app.ts',
    'server.js', 'server.ts', 'main.go', 'main.rs', 'index.php', 'main.rb',
}
GIANT_LINES = 400          # arquivo "gigante" acima disso
DUP_MIN_LINES = 8          # linhas idênticas não-triviais para suspeitar de duplicação
MYSTERY_WORDS = {
    'untitled', 'semtitulo', 'temp', 'tmp', 'copy', 'copia', 'old', 'antigo',
    'backup', 'bkp', 'novo', 'new', 'final', 'final2', 'rascunho', 'draft',
    'asdf', 'xxx', 'delete', 'apagar', 'teste', 'test',
}
MYSTERY_VERSION = re.compile(r'^v?\d+$')


def is_mystery_name(name: str) -> bool:
    """Nome genérico/sobra? Tokeniza pelo separador (copy/old/temp/v2/test1…)."""
    stem = Path(name).stem.lower()
    tokens = [t for t in re.split(r'[_\-.\s]+', stem) if t]
    for t in tokens:
        if t in MYSTERY_WORDS or MYSTERY_VERSION.match(t):
            return True
        if re.match(r'^(test|teste)\d+$', t):
            return True
    return False

# Padrões de segredo (o VALOR nunca é impresso — só mascarado)
SECRET_PATTERNS = [
    ('OpenAI/Anthropic key', re.compile(r'\bsk-[A-Za-z0-9_\-]{16,}')),
    ('AWS access key',       re.compile(r'\bAKIA[0-9A-Z]{12,}')),
    ('GitHub token',         re.compile(r'\bgh[porsu]_[A-Za-z0-9]{20,}')),
    ('Google API key',       re.compile(r'\bAIza[0-9A-Za-z_\-]{30,}')),
    ('Slack token',          re.compile(r'\bxox[baprs]-[A-Za-z0-9\-]{10,}')),
    ('Private key block',    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ('Senha embutida',       re.compile(r'(?i)\b(password|senha|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*[\'"][^\'"\s]{6,}[\'"]')),
]
STOPWORDS_PT = {
    'a','o','e','de','da','do','em','no','na','os','as','um','uma','que','para','pra',
    'com','por','se','ao','aos','das','dos','ou','the','of','to','is','my','me','eu',
    'quero','preciso','fazer','faz','onde','como','mudar','mexer','arquivo','projeto',
    'novo','nova','adicionar','tirar','ajustar','favor','preciso','gostaria',
}

# --------------------------------------------------------------------------
# Ancoragem no projeto (onde vive o .novelo/)
# --------------------------------------------------------------------------
def project_root() -> Path:
    env = os.environ.get('CLAUDE_PROJECT_DIR')
    if env and Path(env).is_dir():
        return Path(env).resolve()
    p = Path.cwd().resolve()
    for cand in [p, *p.parents]:
        if (cand / '.git').exists() or (cand / '.claude').exists() or (cand / 'CLAUDE.md').exists():
            return cand
    return Path.cwd().resolve()

ROOT = project_root()
HOME = ROOT / '.novelo'
INV = HOME / 'inventario.json'
MAPA = HOME / 'mapa.md'
NOS_CSV = HOME / 'nos.csv'
MMD = HOME / 'diagrama.mmd'
PLANO = HOME / 'plano.md'
CONFIG = HOME / 'config.md'


def ensure_home():
    HOME.mkdir(parents=True, exist_ok=True)


def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return ''


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def human(n: int) -> str:
    for unit in ('B', 'KB', 'MB'):
        if n < 1024:
            return f'{n:.0f}{unit}'
        n /= 1024
    return f'{n:.0f}GB'


# --------------------------------------------------------------------------
# Varredura da árvore
# --------------------------------------------------------------------------
def walk_files():
    """Percorre o projeto ignorando pastas de dependências/artefatos."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.egg')]
        for fn in filenames:
            fp = Path(dirpath) / fn
            ext = fp.suffix.lower()
            if ext in CODE_EXT or fn in NOTABLE_CONFIG:
                yield fp, ext, fn


def detect_entry(fp: Path, fn: str, text: str) -> bool:
    if fn in ENTRY_NAMES:
        return True
    if re.search(r"if\s+__name__\s*==\s*['\"]__main__['\"]", text):
        return True
    if re.search(r'\bdef\s+main\s*\(', text):
        return True
    if re.search(r'(Flask|FastAPI|express|createServer|app\.listen|uvicorn\.run|Application\()', text):
        return True
    return False


DEF_PATTERNS = [
    re.compile(r'^\s*def\s+([A-Za-z_]\w*)', re.M),
    re.compile(r'^\s*(?:async\s+)?function\s+([A-Za-z_]\w*)', re.M),
    re.compile(r'^\s*class\s+([A-Za-z_]\w*)', re.M),
    re.compile(r'^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_]\w*)\s*=\s*(?:async\s*)?\(', re.M),
    re.compile(r'^\s*func\s+([A-Za-z_]\w*)', re.M),
    re.compile(r'^\s*(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+([A-Za-z_]\w*)\s*\(', re.M),
]

IMPORT_PATTERNS = [
    re.compile(r'^\s*from\s+([.\w]+)\s+import', re.M),           # py
    re.compile(r'^\s*import\s+([.\w]+)', re.M),                  # py / js bare
    re.compile(r'''require\(\s*['"]([^'"]+)['"]\s*\)''', re.M),  # node
    re.compile(r'''import\s+.*?from\s+['"]([^'"]+)['"]''', re.M),# es modules
    re.compile(r'''include(?:_once)?\s*\(?\s*['"]([^'"]+)['"]''', re.M),  # php
]


def extract_defs(text: str):
    names = set()
    for pat in DEF_PATTERNS:
        for m in pat.finditer(text):
            nm = m.group(1)
            if nm and len(nm) > 2 and nm not in ('main', 'self'):
                names.add(nm)
    return names


def extract_imports(text: str):
    mods = set()
    for pat in IMPORT_PATTERNS:
        for m in pat.finditer(text):
            mods.add(m.group(1))
    return mods


# --------------------------------------------------------------------------
# setup
# --------------------------------------------------------------------------
def cmd_setup(args):
    ensure_home()
    def ask(prompt, flag):
        if flag:
            return flag
        try:
            return input(prompt).strip()
        except EOFError:
            return ''

    print('\n=== Novelo — primeira conversa (configuração) ===\n')
    projeto = ask('Como você chama esse projeto? ', args.projeto) or 'Meu projeto'
    o_que_e = ask('Em uma frase, o que ele faz / deveria fazer? ', args.o_que_e) or '[a preencher]'
    linguagem = ask('Qual a linguagem/tecnologia principal? (ex.: Python, Node, PHP, "não sei") ', args.linguagem) or 'não sei'
    rodar = ask('Como você roda/abre esse projeto hoje? (comando ou "não sei") ', args.rodar) or 'não sei'

    config_txt = (
        f"# Configuração do Novelo\n\n"
        f"- **Projeto:** {projeto}\n"
        f"- **O que é:** {o_que_e}\n"
        f"- **Linguagem principal:** {linguagem}\n"
        f"- **Como rodar:** {rodar}\n"
        f"- **Raiz do projeto:** {ROOT}\n"
        f"- **Configurado em:** {datetime.now():%d/%m/%Y %H:%M}\n"
    )
    CONFIG.write_text(config_txt, encoding='utf-8')

    # protege o .gitignore
    gi = ROOT / '.gitignore'
    lines = gi.read_text(encoding='utf-8', errors='replace').splitlines() if gi.exists() else []
    if '.novelo/' not in [l.strip() for l in lines]:
        with gi.open('a', encoding='utf-8') as f:
            if lines and lines[-1].strip():
                f.write('\n')
            f.write('# Novelo (mapa e configuração locais)\n.novelo/\n')
        print('✓ Adicionei ".novelo/" ao seu .gitignore (o mapa fica só na sua máquina).')

    print('\n✓ Configuração salva em .novelo/config.md')

    # autodestruição da pasta setup/
    setup_dir = Path(__file__).resolve().parent.parent / 'setup'
    removed = []
    if setup_dir.is_dir():
        import shutil
        try:
            shutil.rmtree(setup_dir)
            removed.append('setup/')
        except Exception as e:
            print(f'(aviso: não consegui remover setup/: {e})')
    if removed:
        print(f'✓ Removi os arquivos de primeira execução ({", ".join(removed)}).')
    print('\nPronto! Agora peça pro Novelo: "desembola esse projeto" para começar o mapa.\n')


# --------------------------------------------------------------------------
# mapear
# --------------------------------------------------------------------------
def build_inventory(delta_since=None):
    inv = []
    for fp, ext, fn in walk_files():
        try:
            st = fp.stat()
        except Exception:
            continue
        if delta_since is not None and st.st_mtime <= delta_since:
            # ainda inclui no inventário, mas marca como não-alterado
            changed = False
        else:
            changed = True
        text = read_text(fp)
        nlines = text.count('\n') + (1 if text and not text.endswith('\n') else 0)
        inv.append({
            'path': rel(fp),
            'ext': ext,
            'name': fn,
            'bytes': st.st_size,
            'lines': nlines,
            'tokens_aprox': st.st_size // 4,
            'mtime': st.st_mtime,
            'entry': detect_entry(fp, fn, text),
            'defs': sorted(extract_defs(text)),
            'imports': sorted(extract_imports(text)),
            'changed': changed,
        })
    inv.sort(key=lambda r: (r['path'].count('/'), r['path']))
    return inv


def cmd_mapear(args):
    ensure_home()
    delta_since = None
    if args.delta and INV.exists():
        try:
            prev = json.loads(INV.read_text(encoding='utf-8'))
            delta_since = prev.get('_scanned_at', 0)
        except Exception:
            delta_since = None

    inv = build_inventory(delta_since)
    total_files = len(inv)
    total_lines = sum(r['lines'] for r in inv)
    total_tokens = sum(r['tokens_aprox'] for r in inv)
    entries = [r for r in inv if r['entry']]

    INV.write_text(json.dumps({
        '_scanned_at': datetime.now().timestamp(),
        '_root': str(ROOT),
        'files': inv,
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    # esqueleto do mapa.md agrupado por pasta
    by_folder = {}
    for r in inv:
        folder = str(Path(r['path']).parent)
        by_folder.setdefault(folder, []).append(r)

    out = []
    out.append('# Mapa do projeto — Novelo\n')
    out.append(f'> Inventário automático de {total_files} arquivos '
               f'({total_lines} linhas, ~{total_tokens:,} tokens). '
               f'Gerado em {datetime.now():%d/%m/%Y %H:%M}.\n')
    out.append('> A IA preenche o PROPÓSITO de cada arquivo em português, '
               'lendo o conteúdo — nunca chuta.\n')
    out.append('\n## Visão geral\n')
    out.append('_[A IA escreve aqui, em 3 frases simples: o que esse projeto é, '
               'para quem serve e como ele funciona por cima.]_\n')
    if entries:
        out.append('\n## Portas de entrada (por onde o projeto começa a rodar)\n')
        for r in entries:
            out.append(f"- `{r['path']}` — _[a IA explica o que dispara aqui]_")
    out.append('\n')
    for folder in sorted(by_folder):
        label = folder if folder != '.' else '(raiz)'
        out.append(f'\n## {label}/\n')
        for r in sorted(by_folder[folder], key=lambda x: x['name']):
            tag = ' · 🚪 porta de entrada' if r['entry'] else ''
            defs = f" · define: {', '.join(r['defs'][:4])}" if r['defs'] else ''
            out.append(f"- `{r['name']}` ({r['lines']} linhas · ~{r['tokens_aprox']} tokens){tag}"
                       f"\n  - PROPÓSITO: _[a IA preenche numa frase]_{defs}")
    MAPA.write_text('\n'.join(out) + '\n', encoding='utf-8')

    print(f'\n📖 Mapa gerado: {rel(MAPA)}')
    print(f'   {total_files} arquivos · {total_lines} linhas · ~{total_tokens:,} tokens estimados')
    if entries:
        print(f'   Portas de entrada detectadas: {", ".join(r["path"] for r in entries[:6])}')
    else:
        print('   Nenhuma porta de entrada óbvia detectada — a IA vai investigar.')
    print('\n➡  Próximo: a IA lê os arquivos e preenche o PROPÓSITO de cada um no mapa.md,')
    print('   depois rode "fios" para ver como eles se conectam.\n')


# --------------------------------------------------------------------------
# fios — grafo de conexões
# --------------------------------------------------------------------------
def resolve_import_to_file(mod: str, inv_by_stem: dict):
    """Tenta casar um import com um arquivo do próprio projeto (por nome-base).
    Lida com módulos pontilhados do Python (src.db -> db) e caminhos JS (./utils/x)."""
    mod = mod.strip()
    parts = [p for p in re.split(r'[./\\]', mod) if p and p != '..']
    stem = parts[-1] if parts else mod
    return inv_by_stem.get(stem)


def cmd_fios(args):
    ensure_home()
    if not INV.exists():
        print('⚠  Rode "mapear" primeiro (ainda não há inventário).')
        return
    files = json.loads(INV.read_text(encoding='utf-8'))['files']
    by_stem = {}
    for r in files:
        stem = Path(r['name']).stem
        by_stem.setdefault(stem, r['path'])

    edges = set()      # (origem, destino)
    for r in files:
        src = r['path']
        for mod in r['imports']:
            tgt = resolve_import_to_file(mod, by_stem)
            if tgt and tgt != src:
                edges.add((src, tgt))

    # centralidade por grau de entrada (quantos importam este)
    indeg, outdeg = {}, {}
    for a, b in edges:
        outdeg[a] = outdeg.get(a, 0) + 1
        indeg[b] = indeg.get(b, 0) + 1

    # órfãos: sem aresta de entrada nem de saída (e não é porta de entrada/config)
    connected = {a for a, _ in edges} | {b for _, b in edges}
    orphans = [r['path'] for r in files
               if r['path'] not in connected and not r['entry']
               and r['ext'] in CODE_EXT and r['name'] not in NOTABLE_CONFIG]

    # ciclos (DFS simples)
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
    cycles = []
    WHITE, GREY, BLACK = 0, 1, 2
    color = {}
    stack = []

    def dfs(u):
        color[u] = GREY
        stack.append(u)
        for v in adj.get(u, []):
            if color.get(v, WHITE) == GREY:
                if v in stack:
                    i = stack.index(v)
                    cyc = stack[i:] + [v]
                    if len(cyc) > 2:
                        cycles.append(cyc)
            elif color.get(v, WHITE) == WHITE:
                dfs(v)
        stack.pop()
        color[u] = BLACK

    for r in files:
        if color.get(r['path'], WHITE) == WHITE and r['path'] in adj:
            dfs(r['path'])

    # Mermaid (limita a 45 arestas para não virar borrão)
    def mid(p):
        return 'n_' + re.sub(r'[^A-Za-z0-9]', '_', p)[:40]
    lines = ['graph LR']
    shown = list(edges)[:45]
    for a, b in shown:
        lines.append(f'  {mid(a)}["{Path(a).name}"] --> {mid(b)}["{Path(b).name}"]')
    if len(edges) > 45:
        lines.append(f'  %% ... e mais {len(edges)-45} conexões (resumidas)')
    MMD.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'\n🧵 Fios do projeto — {len(edges)} conexões entre {len(connected)} arquivos')
    print(f'   Diagrama Mermaid salvo em {rel(MMD)}')
    top = sorted(indeg.items(), key=lambda x: -x[1])[:6]
    if top:
        print('\n   Arquivos mais CENTRAIS (mexer aqui afeta muita coisa):')
        for p, d in top:
            print(f'     • {p}  ← usado por {d} arquivo(s)')
    if cycles:
        print(f'\n   ⚠  {len(cycles)} ciclo(s) de dependência (A usa B que volta em A) — '
              'costuma ser sinal de emaranhado:')
        for cyc in cycles[:3]:
            print('     ↻ ' + ' → '.join(Path(c).name for c in cyc))
    if orphans:
        print(f'\n   Possíveis ilhas (ninguém importa e não são porta de entrada) — '
              f'confirme se ainda servem:')
        for p in orphans[:8]:
            print(f'     ? {p}')
    print('\n➡  Próximo: rode "nos" para achar a bagunça (código morto, duplicação, riscos).\n')


# --------------------------------------------------------------------------
# nos — detector de bagunça
# --------------------------------------------------------------------------
def git_tracked_env():
    if not (ROOT / '.git').exists():
        return []
    try:
        out = subprocess.run(['git', 'ls-files'], cwd=str(ROOT),
                             capture_output=True, text=True, timeout=15)
        return [l for l in out.stdout.splitlines()
                if l == '.env' or l.endswith('/.env') or l.startswith('.env')]
    except Exception:
        return []


def mask(s: str) -> str:
    s = s.strip().strip('\'"')
    if len(s) <= 8:
        return s[:2] + '****'
    return s[:4] + '****' + s[-2:]


def cmd_nos(args):
    ensure_home()
    if not INV.exists():
        print('⚠  Rode "mapear" primeiro.')
        return
    files = json.loads(INV.read_text(encoding='utf-8'))['files']
    rows = []  # (tipo, severidade, arquivo, detalhe, confianca)

    # 1) segredo no código
    for r in files:
        fp = ROOT / r['path']
        text = read_text(fp)
        for label, pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                ln = text[:m.start()].count('\n') + 1
                rows.append(('segredo-no-codigo', 'ALTA', f"{r['path']}:{ln}",
                             f"{label} exposto (mascarado: {mask(m.group(0))})", 'alta'))
                break  # um por padrão por arquivo já basta pra alertar

    # 2) .env versionado
    for env in git_tracked_env():
        rows.append(('env-versionado', 'ALTA', env,
                     'arquivo .env está no Git — segredos podem ter vazado no histórico', 'alta'))

    # 3) arquivo gigante
    for r in files:
        if r['ext'] in CODE_EXT and r['lines'] > GIANT_LINES:
            rows.append(('arquivo-gigante', 'MEDIA', r['path'],
                         f"{r['lines']} linhas — difícil de entender e mexer sem quebrar", 'alta'))

    # 4) arquivo-mistério (nome genérico / muito curto / sem função)
    for r in files:
        if r['ext'] not in CODE_EXT:
            continue
        if is_mystery_name(r['name']):
            rows.append(('arquivo-misterio', 'BAIXA', r['path'],
                         'nome genérico (copy/old/temp/v2…) — talvez seja sobra; confirme', 'media'))
        elif r['lines'] <= 4 and not r['defs'] and not r['entry']:
            rows.append(('arquivo-misterio', 'BAIXA', r['path'],
                         'arquivo quase vazio, sem função definida — confirme se serve', 'media'))

    # 5) possível órfão (basename nunca referenciado por outro arquivo)
    # constrói um índice de menções: para cada arquivo, quais outros basenames aparecem no texto
    stems = {Path(r['name']).stem: r['path'] for r in files}
    referenced = set()
    all_text = {}
    for r in files:
        all_text[r['path']] = read_text(ROOT / r['path'])
    for r in files:
        txt = all_text[r['path']]
        for stem, owner in stems.items():
            if owner == r['path']:
                continue
            if re.search(r'\b' + re.escape(stem) + r'\b', txt):
                referenced.add(owner)
    for r in files:
        if (r['ext'] in CODE_EXT and r['path'] not in referenced
                and not r['entry'] and r['name'] not in NOTABLE_CONFIG
                and r['lines'] >= 3):
            rows.append(('possivel-codigo-morto', 'BAIXA', r['path'],
                         'ninguém parece usar este arquivo — possível código morto; confirme antes de apagar', 'media'))

    # 6) possível duplicação (pares com >= DUP_MIN_LINES linhas idênticas não-triviais)
    sig = {}
    for r in files:
        if r['ext'] not in CODE_EXT:
            continue
        lines_nontrivial = [l.strip() for l in all_text[r['path']].splitlines()
                            if len(l.strip()) > 20 and not l.strip().startswith(('#', '//', '*', 'import', 'from'))]
        sig[r['path']] = set(lines_nontrivial)
    paths = list(sig.keys())
    seen_pairs = set()
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            a, b = paths[i], paths[j]
            common = sig[a] & sig[b]
            if len(common) >= DUP_MIN_LINES:
                key = tuple(sorted((a, b)))
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                rows.append(('possivel-duplicacao', 'MEDIA', f'{a}  ⟷  {b}',
                             f'{len(common)} linhas iguais — possível lógica repetida; confirme e unifique', 'media'))

    # 7) falta de teste (projeto inteiro)
    has_test = any(re.search(r'(^|/)(tests?|spec)(/|$)', r['path']) or
                   re.search(r'(test_|_test|\.test\.|\.spec\.)', r['name'])
                   for r in files)
    if not has_test and files:
        rows.append(('sem-teste', 'BAIXA', '(projeto todo)',
                     'nenhum teste automático encontrado — mexer no código fica mais arriscado', 'alta'))

    # grava CSV
    with NOS_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['tipo', 'severidade', 'arquivo', 'detalhe', 'confianca'])
        w.writerows(rows)

    order = {'ALTA': 0, 'MEDIA': 1, 'BAIXA': 2}
    rows.sort(key=lambda x: (order.get(x[1], 3), x[0]))
    icon = {'ALTA': '🔴', 'MEDIA': '🟡', 'BAIXA': '⚪'}
    print(f'\n🪢 Nós encontrados: {len(rows)}  (salvos em {rel(NOS_CSV)})\n')
    cur = None
    for tipo, sev, arq, det, conf in rows:
        if sev != cur:
            cur = sev
            print(f'{icon.get(sev,"")} {sev}')
        conf_tag = '' if conf == 'alta' else '  (possível — confirme)'
        print(f'   • [{tipo}] {arq}\n     {det}{conf_tag}')
    if not rows:
        print('   ✓ Nenhum nó óbvio detectado. Projeto relativamente arrumado!')
    print('\n➡  Próximo: rode "plano" para o roteiro de limpeza em passos pequenos e seguros.')
    print('   (Segredos aparecem SEMPRE mascarados — o Novelo nunca imprime o valor real.)\n')


# --------------------------------------------------------------------------
# rumo — "onde eu mexo pra fazer X?"
# --------------------------------------------------------------------------
def cmd_rumo(args):
    ensure_home()
    if not INV.exists():
        print('⚠  Rode "mapear" primeiro.')
        return
    tarefa = (args.tarefa or '').strip()
    if not tarefa:
        print('Uso: rumo --tarefa "o que você quer mudar/adicionar"')
        return
    files = json.loads(INV.read_text(encoding='utf-8'))['files']
    terms = [strip_accents(t.lower()) for t in re.findall(r'\w+', tarefa)
             if len(t) > 2 and strip_accents(t.lower()) not in STOPWORDS_PT]
    terms = list(dict.fromkeys(terms))

    scored = []
    for r in files:
        name_norm = strip_accents(r['path'].lower())
        text = strip_accents(read_text(ROOT / r['path']).lower())
        score, hits = 0, []
        for t in terms:
            in_name = name_norm.count(t)
            in_body = text.count(t)
            if in_name:
                score += in_name * 5
                hits.append(f'{t}(nome)')
            if in_body:
                score += min(in_body, 8)
                if f'{t}(nome)' not in hits:
                    hits.append(t)
        if score > 0:
            scored.append((score, r, hits))
    scored.sort(key=lambda x: -x[0])

    print(f'\n🧭 Rumo para: "{tarefa}"\n')
    if not scored:
        print('   Não achei arquivos com essas palavras. Tente descrever com outros termos,')
        print('   ou peça pro Novelo "desembola o projeto" antes para entender o todo.\n')
        return
    print('   Provavelmente você mexe AQUI (do mais provável ao menos):')
    for score, r, hits in scored[:8]:
        print(f'     • {r["path"]}  ·  bateu: {", ".join(hits[:5])}')
    # cuidado
    central = [r['path'] for r in files if r['entry']]
    if central:
        print('\n   ⚠  Cuidado ao encostar (portas de entrada / base do projeto):')
        for p in central[:5]:
            print(f'     ! {p}')
    print('\n   (Heurística por palavras — a IA confirma lendo os arquivos antes de mexer.)\n')


# --------------------------------------------------------------------------
# plano — roteiro de limpeza
# --------------------------------------------------------------------------
CLEANUP_ORDER = [
    ('segredo-no-codigo', 'ALTA', 'Tirar segredos de dentro do código',
     'Mover cada chave/senha para uma variável de ambiente (.env) e trocar a chave exposta por uma nova. '
     'O valor antigo já pode ter vazado.',
     'Rode o projeto e confirme que ele ainda conecta com a chave nova.'),
    ('env-versionado', 'ALTA', 'Tirar o .env do Git',
     'Adicionar `.env` ao `.gitignore` e remover do controle de versão. Trocar as chaves que estavam nele.',
     'Confirme com `git status` que o .env não aparece mais como versionado.'),
    ('arquivo-misterio', 'BAIXA', 'Confirmar os arquivos-mistério',
     'Abrir cada arquivo de nome genérico (copy/old/temp/v2). Se não serve mais, apagar; se serve, renomear com um nome claro.',
     'Depois de apagar um, rode o projeto e veja se nada quebrou.'),
    ('possivel-codigo-morto', 'BAIXA', 'Remover código morto (com cuidado)',
     'Um de cada vez: confirmar que ninguém usa, apagar, e testar. Nunca apagar vários de uma vez.',
     'Após cada remoção, rode o projeto/teste — se quebrou, volte o arquivo.'),
    ('possivel-duplicacao', 'MEDIA', 'Unificar a lógica repetida',
     'Escolher UMA das versões como boa, extrair para um único lugar e fazer as duas pontas usarem ela.',
     'Rode as duas telas/fluxos que usavam o código repetido e veja se continuam iguais.'),
    ('arquivo-gigante', 'MEDIA', 'Dividir os arquivos gigantes',
     'Quebrar o arquivo em pedaços por assunto (uma parte por responsabilidade). Mover um pedaço por vez.',
     'Depois de cada pedaço movido, rode o projeto e confirme que a função continua igual.'),
    ('sem-teste', 'BAIXA', 'Criar um teste de fumaça',
     'Um teste simples que só abre o projeto e checa que a tela/rota principal responde. É a sua rede de segurança.',
     'Rode o teste — deve passar verde antes de você começar a limpeza pesada.'),
]


def cmd_plano(args):
    ensure_home()
    if not NOS_CSV.exists():
        print('⚠  Rode "nos" primeiro (preciso da lista de bagunça).')
        return
    present = {}
    with NOS_CSV.open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            present.setdefault(row['tipo'], []).append(row['arquivo'])

    out = ['# Plano de desemaranhado — Novelo\n']
    out.append(f'> Passos do MENOR e mais SEGURO para o maior. Faça um por vez e confira '
               f'antes de seguir. Gerado em {datetime.now():%d/%m/%Y %H:%M}.\n')
    out.append('\n**Regra de ouro:** nunca reescreva tudo de uma vez. Cada passo é pequeno, '
               'e cada passo tem um jeito de conferir que nada quebrou.\n')
    n = 0
    for tipo, sev, titulo, comofazer, comoconferir in CLEANUP_ORDER:
        if tipo not in present:
            continue
        n += 1
        alvos = present[tipo]
        out.append(f'\n## Passo {n} — {titulo}  ({sev})\n')
        out.append(f'**O que fazer:** {comofazer}\n')
        out.append('**Onde:**')
        for a in alvos[:12]:
            out.append(f'- `{a}`')
        if len(alvos) > 12:
            out.append(f'- … e mais {len(alvos)-12}')
        out.append(f'\n**Como conferir que não quebrou:** {comoconferir}\n')
    if n == 0:
        out.append('\n_Nenhum nó pendente — nada a limpar por ora. 🎉_\n')
    PLANO.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'\n🗺  Plano de limpeza salvo em {rel(PLANO)} — {n} passo(s), do mais seguro ao mais pesado.')
    print('   A IA vai te guiar passo a passo, um de cada vez, sempre com a conferência no fim.\n')


# --------------------------------------------------------------------------
# painel
# --------------------------------------------------------------------------
def cmd_painel(args):
    ensure_home()
    print('\n╭─ Painel do Novelo ─────────────────────────────╮')
    if CONFIG.exists():
        for line in CONFIG.read_text(encoding='utf-8').splitlines():
            if line.startswith('- **Projeto:'):
                print('│ ' + line.replace('- **Projeto:**', 'Projeto:').strip().ljust(46)[:46] + ' │')
    if INV.exists():
        data = json.loads(INV.read_text(encoding='utf-8'))
        files = data['files']
        print(f'│ Arquivos mapeados: {str(len(files)).ljust(28)} │')
        if MAPA.exists():
            mp = MAPA.read_text(encoding='utf-8')
            pend = mp.count('[a IA preenche')
            filled = len(files) - pend
            print(f'│ Propósitos preenchidos: {(str(max(filled,0))+"/"+str(len(files))).ljust(23)} │')
    else:
        print('│ Ainda não mapeado — rode "mapear".             │')
    if NOS_CSV.exists():
        with NOS_CSV.open(encoding='utf-8') as f:
            rr = list(csv.DictReader(f))
        alta = sum(1 for r in rr if r['severidade'] == 'ALTA')
        media = sum(1 for r in rr if r['severidade'] == 'MEDIA')
        baixa = sum(1 for r in rr if r['severidade'] == 'BAIXA')
        print(f'│ Nós: {alta} altos · {media} médios · {baixa} baixos'.ljust(49) + '│')
    print('╰────────────────────────────────────────────────╯')
    # sugere próximo passo
    if not INV.exists():
        nxt = 'mapear o projeto ("desembola esse projeto")'
    elif MAPA.exists() and MAPA.read_text(encoding='utf-8').count('[a IA preenche') > 0:
        nxt = 'preencher os propósitos no mapa.md (a IA lê os arquivos)'
    elif not NOS_CSV.exists():
        nxt = 'rodar "nos" para achar a bagunça'
    elif not PLANO.exists():
        nxt = 'rodar "plano" para o roteiro de limpeza'
    else:
        nxt = 'seguir o plano.md, um passo por vez'
    print(f'➡  Próximo passo sugerido: {nxt}\n')


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(prog='novelo', description='Cartógrafo e desemaranhador de projetos.')
    sub = ap.add_subparsers(dest='cmd')

    s = sub.add_parser('setup')
    s.add_argument('--projeto'); s.add_argument('--o-que-e', dest='o_que_e')
    s.add_argument('--linguagem'); s.add_argument('--rodar')
    s.set_defaults(func=cmd_setup)

    s = sub.add_parser('mapear'); s.add_argument('--delta', action='store_true')
    s.set_defaults(func=cmd_mapear)

    s = sub.add_parser('fios'); s.set_defaults(func=cmd_fios)
    s = sub.add_parser('nos'); s.set_defaults(func=cmd_nos)

    s = sub.add_parser('rumo'); s.add_argument('--tarefa', required=False)
    s.set_defaults(func=cmd_rumo)

    s = sub.add_parser('plano'); s.set_defaults(func=cmd_plano)
    s = sub.add_parser('painel'); s.set_defaults(func=cmd_painel)

    args = ap.parse_args()
    if not getattr(args, 'cmd', None):
        ap.print_help()
        return
    args.func(args)


if __name__ == '__main__':
    main()
