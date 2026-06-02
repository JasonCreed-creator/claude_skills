#!/usr/bin/env python3
"""
parse_rfp.py - RFP 파일 텍스트 추출 모듈

Supports:
- PDF (.pdf)         : pypdf or pdfplumber
- DOCX (.docx)       : python-docx
- HWP (.hwp)         : olefile (Korean legacy format)
- HWPX (.hwpx)       : zipfile + XML parsing (Korean modern format)

사용:
    from parse_rfp import parse_rfp
    text, metadata = parse_rfp("/path/to/rfp.pdf")
"""

import os
import sys
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple, Dict, List

# Windows 콘솔 한글 출력 안정화 (UTF-8 강제, Sprint 5 BL-S2 패턴)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


# =====================================================================
# 1. PDF 파서
# =====================================================================
def parse_pdf(filepath: str) -> Tuple[str, Dict]:
    """
    PDF에서 텍스트 + 페이지별 메타데이터 추출.
    pdfplumber 우선 사용 (표·레이아웃 보존), 실패 시 pypdf 폴백.
    """
    metadata = {"format": "pdf", "pages": [], "total_pages": 0}
    text_chunks = []

    # 1차 시도: pdfplumber (표·레이아웃 우수)
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            metadata["total_pages"] = len(pdf.pages)
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                tables = page.extract_tables() or []
                text_chunks.append(f"\n===== [페이지 {i}] =====\n{page_text}")
                # 표가 있으면 별도 표기
                for t_idx, table in enumerate(tables, start=1):
                    text_chunks.append(f"\n[표 {i}-{t_idx}]")
                    for row in table:
                        text_chunks.append(" | ".join([c or "" for c in row]))
                metadata["pages"].append({
                    "page": i,
                    "char_count": len(page_text),
                    "table_count": len(tables)
                })
        return "\n".join(text_chunks), metadata
    except ImportError:
        pass
    except Exception as e:
        print(f"[parse_pdf] pdfplumber 실패: {e}, pypdf로 폴백")

    # 2차 시도: pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        metadata["total_pages"] = len(reader.pages)
        for i, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            text_chunks.append(f"\n===== [페이지 {i}] =====\n{page_text}")
            metadata["pages"].append({"page": i, "char_count": len(page_text)})
        return "\n".join(text_chunks), metadata
    except ImportError:
        raise ImportError("PDF 파싱을 위해 pdfplumber 또는 pypdf 설치 필요")


# =====================================================================
# 2. DOCX 파서
# =====================================================================
def parse_docx(filepath: str) -> Tuple[str, Dict]:
    """
    DOCX에서 본문 + 표 텍스트 추출.
    """
    from docx import Document

    metadata = {"format": "docx", "paragraphs": 0, "tables": 0}
    text_chunks = []

    doc = Document(filepath)

    # 1) 본문 단락
    for para in doc.paragraphs:
        if para.text.strip():
            text_chunks.append(para.text)
            metadata["paragraphs"] += 1

    # 2) 표
    for t_idx, table in enumerate(doc.tables, start=1):
        text_chunks.append(f"\n[표 {t_idx}]")
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            text_chunks.append(" | ".join(cells))
        metadata["tables"] += 1

    return "\n".join(text_chunks), metadata


# =====================================================================
# 3. HWPX 파서 (한글 모던 포맷, ZIP+XML 구조)
# =====================================================================
def parse_hwpx(filepath: str) -> Tuple[str, Dict]:
    """
    HWPX는 ZIP 컨테이너 안에 OWPML XML 형식.
    Contents/section*.xml 의 <hp:t> 태그에서 텍스트 추출.
    """
    metadata = {"format": "hwpx", "sections": 0}
    text_chunks = []

    with zipfile.ZipFile(filepath, "r") as z:
        # section*.xml 파일들 정렬해서 순회
        section_files = sorted([
            n for n in z.namelist()
            if n.startswith("Contents/section") and n.endswith(".xml")
        ])
        metadata["sections"] = len(section_files)

        for section in section_files:
            with z.open(section) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                # 네임스페이스 무시하고 't' 태그 모두 수집
                for elem in root.iter():
                    tag_local = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                    if tag_local == "t" and elem.text:
                        text_chunks.append(elem.text)

    return "\n".join(text_chunks), metadata


# =====================================================================
# 4. HWP 파서 (한글 레거시 포맷, OLE 구조)
# =====================================================================
def parse_hwp(filepath: str) -> Tuple[str, Dict]:
    """
    HWP는 OLE Compound Document. 본문은 PrvText 또는 BodyText 스트림에 압축 저장.
    pyhwpx 패키지가 있으면 사용, 없으면 olefile로 raw 추출 시도.
    """
    metadata = {"format": "hwp", "method": ""}

    # 1차: pyhwpx (별도 의존성)
    try:
        from pyhwpx import Hwp
        hwp = Hwp()
        hwp.open(filepath)
        text = hwp.get_text()
        hwp.quit()
        metadata["method"] = "pyhwpx"
        return text, metadata
    except ImportError:
        pass
    except Exception as e:
        print(f"[parse_hwp] pyhwpx 실패: {e}, olefile로 폴백")

    # 2차: olefile (raw 스트림 추출, 정확도 제한적)
    try:
        import olefile
        f = olefile.OleFileIO(filepath)
        # PrvText 스트림 우선 (요약 텍스트, UTF-16LE)
        if f.exists("PrvText"):
            with f.openstream("PrvText") as stream:
                raw = stream.read()
                text = raw.decode("utf-16le", errors="ignore")
                metadata["method"] = "olefile/PrvText"
                f.close()
                return text, metadata
        f.close()
        raise RuntimeError("PrvText 스트림 없음")
    except ImportError:
        raise ImportError(
            "HWP 파싱을 위해 pyhwpx 또는 olefile 설치 필요. "
            "권장: HWP 파일을 PDF로 변환 후 재업로드"
        )


# =====================================================================
# 5. 메인 디스패처
# =====================================================================
def parse_rfp(filepath: str) -> Tuple[str, Dict]:
    """
    RFP 파일 형식 자동 감지 후 적절한 파서 호출.
    
    Args:
        filepath: RFP 파일 경로
    
    Returns:
        (extracted_text, metadata)
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"파일 없음: {filepath}")

    ext = Path(filepath).suffix.lower()

    if ext == ".pdf":
        return parse_pdf(filepath)
    elif ext == ".docx":
        return parse_docx(filepath)
    elif ext == ".hwpx":
        return parse_hwpx(filepath)
    elif ext == ".hwp":
        return parse_hwp(filepath)
    else:
        raise ValueError(
            f"지원하지 않는 형식: {ext}. "
            f"지원 형식: .pdf, .docx, .hwp, .hwpx"
        )


# =====================================================================
# 6. 보조 추출 함수 (공통 패턴)
# =====================================================================
def extract_dates(text: str) -> List[str]:
    """텍스트에서 날짜 패턴 추출 (YYYY-MM-DD, YYYY.MM.DD, YYYY년 MM월 DD일)"""
    patterns = [
        r"\d{4}[-./]\s?\d{1,2}[-./]\s?\d{1,2}",
        r"\d{4}년\s?\d{1,2}월\s?\d{1,2}일",
    ]
    dates = []
    for p in patterns:
        dates.extend(re.findall(p, text))
    return list(set(dates))


def extract_money(text: str) -> List[str]:
    """텍스트에서 금액 패턴 추출 (XXX,XXX,XXX원, X억 X천만원 등)"""
    patterns = [
        r"[\d,]+\s?원",
        r"\d+\s?억\s?(?:\d+\s?천)?(?:\d+\s?백)?(?:\d+\s?만)?\s?원?",
        r"[\d,]+\s?만\s?원",
    ]
    money = []
    for p in patterns:
        money.extend(re.findall(p, text))
    return list(set(money))


def extract_keywords_with_context(
    text: str,
    keywords: List[str],
    context_chars: int = 100
) -> List[Dict]:
    """
    키워드 매칭 + 전후 문맥 추출.
    리스크 패턴 매칭 등에 활용.
    """
    matches = []
    for kw in keywords:
        for m in re.finditer(re.escape(kw), text):
            start = max(0, m.start() - context_chars)
            end = min(len(text), m.end() + context_chars)
            matches.append({
                "keyword": kw,
                "context": text[start:end],
                "position": m.start()
            })
    return matches


# =====================================================================
# 7. CLI 진입점 (단독 실행 시)
# =====================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_rfp.py <rfp_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    text, meta = parse_rfp(filepath)
    print("===== METADATA =====")
    print(meta)
    print("\n===== TEXT (first 1000 chars) =====")
    print(text[:1000])
    print(f"\n[총 {len(text):,} 글자 추출]")
