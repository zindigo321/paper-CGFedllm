#!/usr/bin/env python3
"""Refresh the repository directory tree, XMind index and SHA-256 list locally.

Uses Python 3 standard library only. Does not create paper metadata, read PDFs,
infer research directions, call Git or access the network.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
XMIND = ROOT / 'CG-FedLLM-Literature-Trees-v3.xmind'
REPO_URL = 'https://github.com/zindigo321/paper-CGFedllm'
CNS = 'urn:xmind:xmap:xmlns:content:2.0'
XLINK = 'http://www.w3.org/1999/xlink'
SHEET_ID = 'cgfedllm-repository-directory-index'
PAPER_SHEET_PREFIX = 'cgfedllm-paper-review-'
CATEGORIES = ('innovation1', 'innovation2')


def load_metadata():
    data = json.loads((ROOT / 'metadata/papers.json').read_text(encoding='utf-8'))
    papers = data['papers']
    ids, paths = set(), set()
    for paper in papers:
        pid, directory = paper['id'], paper['directory']
        if not isinstance(pid, int) or isinstance(pid, bool) or pid < 1:
            raise ValueError('Paper ID must be a positive integer')
        for field in ('version_year', 'pages', 'bytes'):
            value = paper.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f'Paper {pid}: fill in a real positive integer for {field}')
        for field in ('title_uploaded', 'uploaded_filename', 'uploaded_version', 'directory'):
            if not isinstance(paper.get(field), str) or not paper[field].strip():
                raise ValueError(f'Paper {pid}: missing {field}')
        if not re.fullmatch('[0-9a-fA-F]{64}', paper.get('sha256_uploaded', '')):
            raise ValueError(f'Paper {pid}: fill in measured SHA-256')
        if paper.get('full_text') is not True:
            raise ValueError(f'Paper {pid}: registry is for completed full-text reading, not drafts')
        if not isinstance(paper.get('public_pdf'), bool):
            raise ValueError(f'Paper {pid}: public_pdf must be true or false')
        if pid in ids or directory in paths:
            raise ValueError('Duplicate paper ID or directory: ' + str(pid))
        ids.add(pid)
        paths.add(directory)
        target = (ROOT / directory).resolve()
        if not target.is_relative_to((ROOT / 'papers').resolve()) or not directory.startswith('papers/'):
            raise ValueError('Paper directory must stay inside papers/: ' + directory)
        if '_template' in Path(directory).parts:
            raise ValueError('Templates must not be counted as papers')
        for filename in ('notes.md', 'source.md', 'citation.bib'):
            if not (target / filename).is_file():
                raise ValueError('Missing paper file: ' + directory + '/' + filename)
        if paper.get('public_pdf'):
            pdf = target / 'paper.pdf'
            if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
                raise ValueError('Missing or invalid public PDF: ' + directory)
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != paper['sha256_uploaded']:
                raise ValueError('Public PDF differs from recorded original: ' + directory)
        elif (target / 'paper.pdf').exists():
            raise ValueError('PDF exists but public_pdf is false: ' + directory)
        parts = Path(directory).parts
        if len(parts) > 1 and parts[1] in CATEGORIES and len(parts) != 3:
            raise ValueError('Use papers/innovationN/year-author-shortname: ' + directory)
    totals = {
        'paper_count': len(papers),
        'total_uploaded_pages': sum(p['pages'] for p in papers),
        'public_pdf_count': sum(bool(p.get('public_pdf')) for p in papers),
    }
    for field, value in totals.items():
        if data.get(field) != value:
            raise ValueError(f'Update metadata/papers.json {field} to {value} first')
    return data


def groups(papers):
    result = {'existing': [], 'innovation1': [], 'innovation2': []}
    for paper in papers:
        parts = Path(paper['directory']).parts
        group = parts[1] if len(parts) > 1 and parts[1] in CATEGORIES else 'existing'
        result[group].append(paper)
    return result


def markdown_tree(data):
    grouped = groups(data['papers'])
    lines = [
        '# Literature tree', '',
        '本页按仓库目录列出已入库论文，与 XMind 的“13 文献目录”工作表一致。',
        '`innovation1`、`innovation2` 仅作为分类名称，不记录创新点说明。',
        '原有论文路径与 XMind 的 12 张分析工作表保留；模板不计入论文数量。', '',
        f"当前：**{data['paper_count']} 篇独立论文 / {data['total_uploaded_pages']} 页 / {data['public_pdf_count']} 份公开 PDF**。", '',
        '[打开 XMind 文献树](CG-FedLLM-Literature-Trees-v3.xmind) · [自行上传说明](INNOVATION_UPLOAD.md)', '',
    ]
    for key, title in [('existing', '原有目录'), ('innovation1', 'innovation1'), ('innovation2', 'innovation2')]:
        lines += ['## ' + title, '']
        if key in CATEGORIES:
            lines += [f'[分类目录](papers/{key}/README.md) · [填写模板](papers/{key}/_template/notes.md)', '']
        if not grouped[key]:
            lines += ['暂无已入库论文。', '']
            continue
        lines += ['| 论文（阅读版本原题） | 阅读版年份 | 页数 | 中文笔记 | 来源 | 引用 | 全文 |', '| --- | --- | --- | --- | --- | --- | --- |']
        for p in grouped[key]:
            d = p['directory']
            title = p['title_uploaded'].replace('|', '\\|').replace('\n', ' ')
            full = f'[{"paper.pdf" if p.get("public_pdf") else "来源链接"}]({d}/{"paper.pdf" if p.get("public_pdf") else "source.md"})'
            lines.append(f'| {title} | {p["version_year"]} | {p["pages"]} | [notes.md]({d}/notes.md) | [source.md]({d}/source.md) | [citation.bib]({d}/citation.bib) | {full} |')
        lines.append('')
    lines += ['## 后续维护', '',
              '填完论文文档及 `metadata/papers.json` 后，在仓库根目录运行 `python tools/update_literature.py --refresh`。',
              '该操作更新此页、XMind 目录与 metadata/new-paper-outlines.json 中已整理的逐篇分析工作表，以及校验清单；论文笔记、引用、元数据、README 论文索引、comparison 和 NOTICE 仍需人工维护。', '',
              '[返回总览](README.md)', '']
    return '\n'.join(lines)


def uid(label):
    return hashlib.sha256(('cgfedllm-directory:' + label).encode()).hexdigest()[:24]


def topic(label, title, children=None, href=None, note=None, root=False):
    t = {'id': uid(label), 'class': 'topic', 'title': title,
         'structureClass': 'org.xmind.ui.logic.right', 'customWidth': 320 if root else 400}
    if children:
        t['children'] = {'attached': children}
    if href:
        t['href'] = href
    if note:
        t['notes'] = {'plain': {'content': note}}
    return t


def make_index(data):
    branches = []
    for key, papers in groups(data['papers']).items():
        children = []
        for p in papers:
            d = p['directory']
            files = [topic(d + '/' + fn, fn, href=REPO_URL + '/blob/main/' + quote(d + '/' + fn))
                     for fn in ('notes.md', 'source.md', 'citation.bib')]
            if p.get('public_pdf'):
                files.append(topic(d + '/paper.pdf', 'paper.pdf', href=REPO_URL + '/blob/main/' + quote(d + '/paper.pdf')))
            children.append(topic(d, p['title_uploaded'], files,
                                  href=REPO_URL + '/blob/main/' + quote(d + '/notes.md'),
                                  note=f"阅读版本：{p['uploaded_version']}；{p['pages']} 页。目录：{d}"))
        name = '原有目录' if key == 'existing' else key
        path = 'papers' if key == 'existing' else 'papers/' + key
        if not children:
            children = [topic(key + ':empty', '暂无已入库论文')]
        branches.append(topic(key, name + f'（{len(papers)} 篇）', children,
                              href=REPO_URL + '/tree/main/' + path))
    root = topic('root', 'paper-CGFedllm\n文献目录', branches, root=True,
                 note=f"共 {data['paper_count']} 篇 / {data['total_uploaded_pages']} 页。innovation1、innovation2 仅为分类名称。模板不计数。原分析工作表保留，不推断新论文结论。GitHub 链接在用户推送相应文件后可用。")
    return styled_sheet(SHEET_ID, '13 文献目录', root)


def styled_sheet(sheet_id, title, root):
    with zipfile.ZipFile(XMIND) as z:
        original = next(s for s in json.loads(z.read('content.json'))
                        if s['id'] != SHEET_ID and not s['id'].startswith(PAPER_SHEET_PREFIX))
    original_root = original['rootTopic']
    original_branch = original_root['children']['attached'][0]
    original_leaf = original_branch['children']['attached'][0]
    def style_topics(t, depth=0):
        source = original_root if depth == 0 else original_branch if depth == 1 else original_leaf
        if 'style' in source:
            t['style'] = copy.deepcopy(source['style'])
        for child in t.get('children', {}).get('attached', []):
            style_topics(child, depth + 1)
    style_topics(root)
    sheet = {'id': sheet_id, 'class': 'sheet', 'title': title, 'rootTopic': root}
    for key in ('theme', 'style'):
        if key in original:
            sheet[key] = copy.deepcopy(original[key])
    return sheet


def make_paper_sheets(data):
    path = ROOT / 'metadata/new-paper-outlines.json'
    if not path.exists():
        return []
    outlines = json.loads(path.read_text(encoding='utf-8'))['papers']
    papers = {p['id']: p for p in data['papers']}
    result, seen = [], set()
    for outline in sorted(outlines, key=lambda o: o['id']):
        pid = outline['id']
        if pid not in papers or pid in seen:
            raise ValueError('Outline ID missing from registry or duplicated: ' + str(pid))
        seen.add(pid)
        p = papers[pid]
        label = PAPER_SHEET_PREFIX + str(pid)
        branches = []
        for section in ('Abstract', 'Introduction', 'Method', 'Experiments', 'Limitation'):
            items = outline['xmind_sections'][section]
            if not isinstance(items, list) or not items or not all(isinstance(item, str) and item.strip() for item in items):
                raise ValueError(f'Paper {pid}: outline {section} is empty')
            leaves = [topic(label + ':' + section + ':' + str(i), item) for i, item in enumerate(items)]
            branches.append(topic(label + ':' + section, section, leaves))
        root = topic(label + ':root', outline['short_name'] + '\n论文解析', branches, root=True,
                     href=REPO_URL + '/blob/main/' + quote(p['directory'] + '/notes.md'),
                     note=p['title_uploaded'] + '\n阅读版本：' + p['uploaded_version'] +
                     f"；{p['pages']} 页。页码指实际附件物理页码。依据完整附件与核验的公开书目，不代表运行复现实验。")
        result.append(styled_sheet(label, f"{14 + len(result):02d} {outline['short_name']}", root))
    return result


def xml_topic(t):
    el = ET.Element('{' + CNS + '}topic', {'id': t['id'], 'structure-class': t['structureClass']})
    if t.get('href'):
        el.set('{' + XLINK + '}href', t['href'])
    if t.get('style'):
        el.set('style-id', t['style']['id'])
    ET.SubElement(el, '{' + CNS + '}title').text = t['title']
    if t.get('notes'):
        notes = ET.SubElement(el, '{' + CNS + '}notes')
        ET.SubElement(notes, '{' + CNS + '}plain').text = t['notes']['plain']['content']
    if t.get('children'):
        children = ET.SubElement(el, '{' + CNS + '}children')
        attached = ET.SubElement(children, '{' + CNS + '}topics', {'type': 'attached'})
        for child in t['children']['attached']:
            attached.append(xml_topic(child))
    return el


def refresh_xmind(index, paper_sheets):
    ET.register_namespace('', CNS)
    ET.register_namespace('xlink', XLINK)
    with zipfile.ZipFile(XMIND) as source:
        infos = source.infolist()
        entries = {info.filename: source.read(info.filename) for info in infos}
    sheets = json.loads(entries['content.json'])
    sheets = [s for s in sheets if s['id'] != SHEET_ID and not s['id'].startswith(PAPER_SHEET_PREFIX)] + [index] + paper_sheets
    xml = ET.fromstring(entries['content.xml'])
    for s in list(xml):
        if s.get('id') == SHEET_ID or s.get('id', '').startswith(PAPER_SHEET_PREFIX):
            xml.remove(s)
    for item in [index] + paper_sheets:
        sheet = ET.SubElement(xml, '{' + CNS + '}sheet', {'id': item['id']})
        ET.SubElement(sheet, '{' + CNS + '}title').text = item['title']
        sheet.append(xml_topic(item['rootTopic']))
    metadata = json.loads(entries['metadata.json'])
    metadata['activeSheetId'] = SHEET_ID
    entries['content.json'] = json.dumps(sheets, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    entries['content.xml'] = ET.tostring(xml, encoding='utf-8', xml_declaration=True)
    entries['metadata.json'] = json.dumps(metadata, ensure_ascii=False).encode('utf-8')
    temp = XMIND.with_suffix('.xmind.tmp')
    with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as dest:
        for info in infos:
            dest.writestr(info, entries[info.filename])
    temp.replace(XMIND)


def repository_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in {'.git', '__pycache__'} for part in p.relative_to(ROOT).parts)
                  and p.name != 'checksums.sha256' and not p.name.endswith('.tmp'))


def refresh_checksums():
    lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(ROOT).as_posix()
             for p in repository_files()]
    (ROOT / 'checksums.sha256').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def check_xmind(expected, expected_paper_sheets):
    with zipfile.ZipFile(XMIND) as z:
        if z.testzip():
            raise ValueError('XMind archive CRC error')
        sheets = json.loads(z.read('content.json'))
        xml = ET.fromstring(z.read('content.xml'))
        ET.fromstring(z.read('META-INF/manifest.xml'))
        manifest = json.loads(z.read('manifest.json'))
        if set(manifest['file-entries']) - set(z.namelist()):
            raise ValueError('XMind manifest references missing files')
    actual = [s for s in sheets if s['id'] == SHEET_ID]
    if actual != [expected]:
        raise ValueError('XMind index is stale; run --refresh')
    actual_paper_sheets = [s for s in sheets if s['id'].startswith(PAPER_SHEET_PREFIX)]
    if actual_paper_sheets != expected_paper_sheets:
        raise ValueError('XMind paper analyses are stale; run --refresh')
    json_nodes, xml_nodes = {}, {}
    def visit(t, parent, sheet_id, child_type='attached'):
        if t['id'] in json_nodes:
            raise ValueError('Duplicate XMind topic ID')
        json_nodes[t['id']] = (t['title'], t.get('href'), t.get('notes', {}).get('plain', {}).get('content'),
                               parent, sheet_id, child_type, t.get('structureClass'), t.get('style', {}).get('id'))
        for kind, children in t.get('children', {}).items():
            for child in children:
                visit(child, t['id'], sheet_id, kind)
    for s in sheets:
        visit(s['rootTopic'], None, s['id'])
    def visit_xml(el, parent, sheet_id, child_type='attached'):
        node_id = el.get('id')
        if node_id in xml_nodes:
            raise ValueError('Duplicate XML topic ID')
        xml_nodes[node_id] = (el.findtext('{' + CNS + '}title'),
                              el.get('{' + XLINK + '}href'), el.findtext('{' + CNS + '}notes/{' + CNS + '}plain'),
                              parent, sheet_id, child_type, el.get('structure-class'), el.get('style-id'))
        for group in el.findall('{' + CNS + '}children/{' + CNS + '}topics'):
            for child in group.findall('{' + CNS + '}topic'):
                visit_xml(child, node_id, sheet_id, group.get('type', 'attached'))
    for s in xml.findall('{' + CNS + '}sheet'):
        visit_xml(s.find('{' + CNS + '}topic'), None, s.get('id'))
    if [s['id'] for s in sheets] != [s.get('id') for s in xml.findall('{' + CNS + '}sheet')]:
        raise ValueError('XMind JSON/XML sheet order differs')
    if json_nodes != xml_nodes:
        raise ValueError('XMind JSON/XML topic contents differ')
    return len(sheets), len(json_nodes)


def check_all(data):
    if (ROOT / 'literature-tree.md').read_text(encoding='utf-8') != markdown_tree(data):
        raise ValueError('Markdown tree is stale; run --refresh')
    sheet_count, topic_count = check_xmind(make_index(data), make_paper_sheets(data))
    listed = {}
    for line in (ROOT / 'checksums.sha256').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in listed:
            raise ValueError('Duplicate checksum path: ' + name)
        listed[name] = digest
    actual = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in repository_files()}
    if set(listed) != set(actual):
        changed_paths = sorted(set(listed) ^ set(actual))
        raise ValueError('SHA-256 file list differs: ' + ', '.join(changed_paths) + '; review changes, then --refresh')
    different = [name for name in listed if listed[name] != actual[name]]
    if different:
        newline_only, other = [], []
        for name in different:
            path = ROOT / name
            if path.suffix in {'.md', '.json', '.bib', '.py'}:
                raw = path.read_bytes()
                lf = raw.replace(b'\r\n', b'\n')
                candidates = {hashlib.sha256(lf).hexdigest(), hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest()}
                if listed[name] in candidates:
                    newline_only.append(name)
                    continue
            other.append(name)
        details = ('\nOnly LF/CRLF differs: ' + ', '.join(newline_only)) if newline_only else ''
        if other:
            details += '\nContent mismatch: ' + ', '.join(other)
        raise ValueError('Local working-tree SHA-256 mismatch.' + details + '\nReview changes before rebuilding with --refresh. PDF bytes must match exactly.')
    broken = []
    for p in ROOT.rglob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', p.read_text(encoding='utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            target = unquote(link.split('#')[0])
            if target and not (p.parent / target).exists():
                broken.append(p.relative_to(ROOT).as_posix() + ': ' + link)
    if broken:
        raise ValueError('Broken relative links:\n' + '\n'.join(broken))
    print(f"PASS: {data['paper_count']} papers, {sheet_count} XMind sheets, {topic_count} topics, {len(actual)} SHA-256 entries; relative Markdown links resolve.")
    print('Local structure checks only; no GitHub upload or desktop XMind opening was performed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--refresh', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = load_metadata()
    if args.refresh:
        (ROOT / 'literature-tree.md').write_text(markdown_tree(data), encoding='utf-8')
        refresh_xmind(make_index(data), make_paper_sheets(data))
        refresh_checksums()
    check_all(data)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
