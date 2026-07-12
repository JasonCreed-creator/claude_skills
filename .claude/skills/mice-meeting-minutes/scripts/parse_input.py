"""
parse_input.py — mice-meeting-minutes 입력 파서

4개 채널 입력을 표준 transcript 구조로 정규화한다.

채널:
  Ch1 — 클로바노트 export (화자 + 타임스탬프)
  Ch2 — Otter / Whisper / Zoom / Meet / Teams export
  Ch3 — 메모형 자유 텍스트
  Ch4 — 채팅창 직접 구두 보고

기능:
  - 채널 자동 감지
  - 화자 라벨 정규화
  - 타임스탬프 추출
  - 30분 단위 청크 분할
  - 화자 매핑 적용
  - 입력 검증
"""

import re
from dataclasses import dataclass, field, asdict
from typing import Optional
import json
import sys

# UTF-8 stdout/stderr 강제 (Windows cp949 환경 크래시 방지)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


# =====================================================================
# 데이터 구조
# =====================================================================

@dataclass
class Utterance:
    """단일 발화 단위"""
    speaker_raw: str
    speaker_mapped: Optional[str] = None
    timestamp: Optional[str] = None  # HH:MM:SS
    text: str = ""
    char_offset: int = 0
    chunk_id: int = 0
    redaction_hints: list[str] = field(default_factory=list)


@dataclass
class TranscriptMeta:
    """transcript 메타데이터"""
    channel: str  # ch1_clovanote / ch2_otter / ch2_whisper / ch2_zoom / ch2_meet / ch2_teams / ch3_memo / ch4_oral
    total_utterances: int = 0
    unique_speakers: int = 0
    estimated_duration_min: float = 0.0
    has_timestamps: bool = False
    chunks: int = 1
    language_mix: str = "ko"  # ko / en / mixed
    validation_warnings: list[str] = field(default_factory=list)


@dataclass
class ParsedTranscript:
    """파싱 결과"""
    meta: TranscriptMeta
    utterances: list[Utterance] = field(default_factory=list)
    speaker_map: dict[str, str] = field(default_factory=dict)


# =====================================================================
# 채널 감지
# =====================================================================

def detect_channel(raw: str) -> str:
    """입력 텍스트의 채널을 자동 감지"""
    sample = raw[:3000]

    # Ch2C — Zoom VTT
    if sample.lstrip().startswith("WEBVTT"):
        return "ch2_zoom"

    # Ch2B — Whisper + pyannote
    if re.search(r"^SPEAKER_\d+\s+\[\d{2}:\d{2}:\d{2}", sample, re.MULTILINE):
        return "ch2_whisper"

    # Ch2B — Whisper plain
    if re.search(r"^\[\d{2}:\d{2}:\d{2}\s+-->\s+\d{2}:\d{2}:\d{2}\]", sample, re.MULTILINE):
        return "ch2_whisper"

    # Ch2E — Teams (타임스탬프 + 콜론 + 발화)
    if re.search(r"^\[\d{2}:\d{2}(:\d{2})?\]\s+\S+:", sample, re.MULTILINE):
        return "ch2_teams"

    # Ch1 — 클로바노트 (한글 화자 + 타임스탬프)
    if re.search(r"^(참석자\s*\d+|[가-힣]+\s?[가-힣]*)\s+\d{2}:\d{2}:\d{2}\s*$",
                 sample, re.MULTILINE):
        return "ch1_clovanote"

    # Ch2A — Otter (영문 화자 + 타임스탬프)
    if re.search(r"^[A-Za-z][A-Za-z\s]{1,30}\s+\d{2}:\d{2}:\d{2}\s*$",
                 sample, re.MULTILINE):
        return "ch2_otter"

    # Ch2D — Google Meet (이름: 발화 형식, 타임스탬프 약함)
    if re.search(r"^[가-힣A-Za-z][\w가-힣]{0,30}:\s+\S+", sample, re.MULTILINE):
        meet_lines = len(re.findall(r"^[가-힣A-Za-z][\w가-힣]{0,30}:\s+\S+",
                                     sample, re.MULTILINE))
        if meet_lines >= 3:
            return "ch2_meet"

    # Ch3 — 메모형 (긴 텍스트, 화자 라벨 약함)
    if len(raw) > 200:
        return "ch3_memo"

    # Ch4 — 짧은 구두 보고
    return "ch4_oral"


# =====================================================================
# 채널별 파서
# =====================================================================

def parse_clovanote(raw: str) -> list[Utterance]:
    """Ch1: 클로바노트 export 파서"""
    pattern = re.compile(
        r"^(참석자\s*\d+|[가-힣]+\s?[가-힣]*)\s+(\d{2}:\d{2}:\d{2})\s*$",
        re.MULTILINE
    )

    utterances: list[Utterance] = []
    matches = list(pattern.finditer(raw))

    for i, m in enumerate(matches):
        speaker = m.group(1).strip()
        timestamp = m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        text = raw[start:end].strip()

        if text:
            utterances.append(Utterance(
                speaker_raw=speaker,
                timestamp=timestamp,
                text=text,
                char_offset=m.start()
            ))

    return utterances


def parse_otter(raw: str) -> list[Utterance]:
    """Ch2A: Otter.ai export 파서"""
    pattern = re.compile(
        r"^([A-Za-z][A-Za-z\s]{1,30}|[가-힣\s]{2,15})\s+(\d{2}:\d{2}:\d{2})\s*$",
        re.MULTILINE
    )

    utterances: list[Utterance] = []
    matches = list(pattern.finditer(raw))

    for i, m in enumerate(matches):
        speaker = m.group(1).strip()
        timestamp = m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        text = raw[start:end].strip()

        if text:
            utterances.append(Utterance(
                speaker_raw=speaker,
                timestamp=timestamp,
                text=text,
                char_offset=m.start()
            ))

    return utterances


def parse_whisper(raw: str) -> list[Utterance]:
    """Ch2B: Whisper / Whisper+pyannote 파서"""
    # pyannote 결합 형식
    pattern_diarized = re.compile(
        r"^(SPEAKER_\d+)\s+\[(\d{2}:\d{2}:\d{2})\s+-->\s+\d{2}:\d{2}:\d{2}\]\s+(.+)$",
        re.MULTILINE
    )
    matches = list(pattern_diarized.finditer(raw))

    if matches:
        return [
            Utterance(
                speaker_raw=m.group(1),
                timestamp=m.group(2),
                text=m.group(3).strip(),
                char_offset=m.start()
            )
            for m in matches
        ]

    # plain Whisper (화자 분리 없음)
    pattern_plain = re.compile(
        r"^\[(\d{2}:\d{2}:\d{2})\s+-->\s+\d{2}:\d{2}:\d{2}\]\s+(.+)$",
        re.MULTILINE
    )
    return [
        Utterance(
            speaker_raw="UNKNOWN",
            timestamp=m.group(1),
            text=m.group(2).strip(),
            char_offset=m.start()
        )
        for m in pattern_plain.finditer(raw)
    ]


def parse_zoom_vtt(raw: str) -> list[Utterance]:
    """Ch2C: Zoom VTT 파서"""
    blocks = re.split(r"\n\s*\n", raw)
    utterances: list[Utterance] = []
    offset = 0

    for block in blocks:
        if "WEBVTT" in block:
            continue

        ts_match = re.search(r"(\d{2}:\d{2}:\d{2})\.\d+\s+-->", block)
        speech_match = re.search(r"^([^:]+):\s*(.+)$", block, re.MULTILINE)

        if ts_match and speech_match:
            utterances.append(Utterance(
                speaker_raw=speech_match.group(1).strip(),
                timestamp=ts_match.group(1),
                text=speech_match.group(2).strip(),
                char_offset=offset
            ))
        offset += len(block) + 2

    return utterances


def parse_teams(raw: str) -> list[Utterance]:
    """Ch2E: Microsoft Teams 파서"""
    pattern = re.compile(
        r"^\[(\d{2}:\d{2}(?::\d{2})?)\]\s+([^:]+):\s+(.+)$",
        re.MULTILINE
    )
    return [
        Utterance(
            speaker_raw=m.group(2).strip(),
            timestamp=m.group(1) if m.group(1).count(":") == 2
                     else f"00:{m.group(1)}",
            text=m.group(3).strip(),
            char_offset=m.start()
        )
        for m in pattern.finditer(raw)
    ]


def parse_meet(raw: str) -> list[Utterance]:
    """Ch2D: Google Meet 파서 (타임스탬프 약함)"""
    pattern = re.compile(
        r"^([가-힣A-Za-z][\w가-힣\s]{0,30}):\s+(.+)$",
        re.MULTILINE
    )
    return [
        Utterance(
            speaker_raw=m.group(1).strip(),
            timestamp=None,
            text=m.group(2).strip(),
            char_offset=m.start()
        )
        for m in pattern.finditer(raw)
    ]


def parse_memo(raw: str) -> list[Utterance]:
    """Ch3: 메모형 자유 텍스트 — 호스트 단일 화자로 처리"""
    lines = [ln.strip() for ln in raw.strip().splitlines() if ln.strip()]
    return [
        Utterance(
            speaker_raw="HOST",
            timestamp=None,
            text=line,
            char_offset=i
        )
        for i, line in enumerate(lines)
    ]


def parse_oral(raw: str) -> list[Utterance]:
    """Ch4: 채팅창 직접 구두 보고 — 단일 발화로 처리"""
    return [
        Utterance(
            speaker_raw="HOST",
            timestamp=None,
            text=raw.strip(),
            char_offset=0
        )
    ]


# 채널별 파서 매핑
CHANNEL_PARSERS = {
    "ch1_clovanote": parse_clovanote,
    "ch2_otter": parse_otter,
    "ch2_whisper": parse_whisper,
    "ch2_zoom": parse_zoom_vtt,
    "ch2_teams": parse_teams,
    "ch2_meet": parse_meet,
    "ch3_memo": parse_memo,
    "ch4_oral": parse_oral,
}


# =====================================================================
# 청크 분할
# =====================================================================

def assign_chunks(utterances: list[Utterance],
                  chunk_minutes: int = 30) -> int:
    """30분 단위로 청크 ID 부여. 청크 개수 반환."""
    if not utterances:
        return 0

    # 타임스탬프 있는 경우 — 시간 기반 분할
    if utterances[0].timestamp:
        for u in utterances:
            if u.timestamp:
                hh, mm, _ = u.timestamp.split(":")
                total_min = int(hh) * 60 + int(mm)
                u.chunk_id = total_min // chunk_minutes

        return max(u.chunk_id for u in utterances) + 1

    # 타임스탬프 없는 경우 — 분량 기반 균등 분할
    total_chars = sum(len(u.text) for u in utterances)
    if total_chars < 5000:  # 짧은 입력 — 단일 청크
        for u in utterances:
            u.chunk_id = 0
        return 1

    # 약 5000자 = 30분 가정으로 분할
    target_per_chunk = 5000
    accumulated = 0
    chunk_id = 0
    for u in utterances:
        u.chunk_id = chunk_id
        accumulated += len(u.text)
        if accumulated >= target_per_chunk:
            chunk_id += 1
            accumulated = 0

    return chunk_id + 1


def estimate_duration(utterances: list[Utterance]) -> float:
    """미팅 추정 분량(분)"""
    if not utterances:
        return 0.0

    # 타임스탬프 있으면 마지막 - 첫번째
    timestamped = [u for u in utterances if u.timestamp]
    if len(timestamped) >= 2:
        first = timestamped[0].timestamp
        last = timestamped[-1].timestamp

        def to_seconds(ts: str) -> int:
            parts = ts.split(":")
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + int(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + int(s)
            return 0

        return (to_seconds(last) - to_seconds(first)) / 60.0

    # 분량 기반 추정 (약 200자/분 한국어 발화)
    total_chars = sum(len(u.text) for u in utterances)
    return total_chars / 200.0


# =====================================================================
# 화자 매핑
# =====================================================================

def apply_speaker_mapping(utterances: list[Utterance],
                          mapping: dict[str, str]) -> None:
    """사용자 매핑 적용"""
    for u in utterances:
        if u.speaker_raw in mapping:
            u.speaker_mapped = mapping[u.speaker_raw]
        else:
            # 부분 매칭 시도 (대소문자·공백 정규화)
            normalized = re.sub(r"\s+", "", u.speaker_raw).lower()
            for key, value in mapping.items():
                if re.sub(r"\s+", "", key).lower() == normalized:
                    u.speaker_mapped = value
                    break


def parse_mapping_string(mapping_str: str) -> dict[str, str]:
    """
    사용자 매핑 문자열 파싱.

    예시:
        '참석자 1 = 호스트, 참석자 2 = 김부장 (고객사A)'
        '참석자 1 = 호스트\n참석자 2 = 김부장'
    """
    mapping = {}
    items = re.split(r"[,\n;]", mapping_str)

    for item in items:
        if "=" in item:
            key, value = item.split("=", 1)
            mapping[key.strip()] = value.strip()

    return mapping


# =====================================================================
# Redaction 사전 표시
# =====================================================================

REDACTION_HINTS = {
    "sensitive": [
        r"솔직히\s*말하면",
        r"오프\s*더\s*레코드",
        r"비공식이지만",
        r"여기서만\s*하는\s*얘긴데",
        r"공식\s*기록\s*아니",
    ],
    "financial_informal": [
        r"예산이?\s*\d+[억만천백]",
        r"마진\s*\d+\s*%",
        r"원가가?\s*\d+",
    ],
    "schedule_internal": [
        r"사장\s*결재",
        r"이사회",
        r"임원\s*회의",
        r"본사\s*결재",
        r"내부\s*보고",
    ],
    "political": [
        r"비방",
        r"압력",
        r"인맥",
        r"정치",
    ],
}


def tag_redaction_hints(utterances: list[Utterance]) -> None:
    """발화에 redaction 힌트 태그 부착"""
    for u in utterances:
        for category, patterns in REDACTION_HINTS.items():
            for p in patterns:
                if re.search(p, u.text):
                    if category not in u.redaction_hints:
                        u.redaction_hints.append(category)


# =====================================================================
# 언어 비율 추정
# =====================================================================

def estimate_language_mix(utterances: list[Utterance]) -> str:
    """ko / en / mixed 추정"""
    if not utterances:
        return "ko"

    total_text = " ".join(u.text for u in utterances)
    ko_chars = len(re.findall(r"[가-힣]", total_text))
    en_chars = len(re.findall(r"[A-Za-z]", total_text))
    total = ko_chars + en_chars

    if total == 0:
        return "ko"

    ko_ratio = ko_chars / total

    if ko_ratio > 0.85:
        return "ko"
    elif ko_ratio < 0.15:
        return "en"
    else:
        return "mixed"


# =====================================================================
# 검증
# =====================================================================

def validate(utterances: list[Utterance], meta: TranscriptMeta) -> list[str]:
    """입력 검증"""
    warnings = []

    if not utterances:
        warnings.append("발화가 추출되지 않음 — 입력 형식 재확인 필요")
        return warnings

    total_chars = sum(len(u.text) for u in utterances)
    if total_chars < 100:
        warnings.append("입력이 너무 짧음 — 추가 정보 권장")

    speakers = set(u.speaker_raw for u in utterances)
    if len(speakers) == 1 and meta.channel not in ("ch3_memo", "ch4_oral"):
        warnings.append("단일 화자 transcript — 메모형으로 처리하는 것이 적절할 수 있음")

    # 발화 비율 편중 체크
    if len(speakers) >= 2:
        speaker_counts = {}
        for u in utterances:
            speaker_counts[u.speaker_raw] = speaker_counts.get(u.speaker_raw, 0) + len(u.text)

        max_speaker = max(speaker_counts.values())
        total = sum(speaker_counts.values())
        if total > 0 and max_speaker / total > 0.8:
            warnings.append("한 화자가 80% 이상 발화 — Type B 단방향 보고 가능성")

    if meta.language_mix == "mixed":
        warnings.append("한·영 혼용 transcript — Otter·Whisper 등 영어 강점 도구 활용 권장")

    return warnings


# =====================================================================
# 메인 진입점
# =====================================================================

def parse_transcript(raw: str,
                     mapping_str: Optional[str] = None,
                     channel_override: Optional[str] = None) -> ParsedTranscript:
    """
    raw transcript를 파싱하여 ParsedTranscript 반환.

    Args:
        raw: 입력 텍스트
        mapping_str: 화자 매핑 문자열 (예: '참석자 1 = 호스트')
        channel_override: 채널 강제 지정 (자동 감지 무시)
    """
    # 1. 채널 감지
    channel = channel_override or detect_channel(raw)

    # 2. 채널별 파싱
    parser = CHANNEL_PARSERS.get(channel, parse_memo)
    utterances = parser(raw)

    # 3. 청크 분할
    chunks = assign_chunks(utterances)

    # 4. 화자 매핑
    speaker_map = {}
    if mapping_str:
        speaker_map = parse_mapping_string(mapping_str)
        apply_speaker_mapping(utterances, speaker_map)

    # 5. Redaction 힌트
    tag_redaction_hints(utterances)

    # 6. 메타데이터
    duration = estimate_duration(utterances)
    speakers = set(u.speaker_raw for u in utterances)
    lang_mix = estimate_language_mix(utterances)

    meta = TranscriptMeta(
        channel=channel,
        total_utterances=len(utterances),
        unique_speakers=len(speakers),
        estimated_duration_min=round(duration, 1),
        has_timestamps=any(u.timestamp for u in utterances),
        chunks=chunks,
        language_mix=lang_mix
    )

    # 7. 검증
    meta.validation_warnings = validate(utterances, meta)

    return ParsedTranscript(
        meta=meta,
        utterances=utterances,
        speaker_map=speaker_map
    )


def to_json(parsed: ParsedTranscript) -> str:
    """JSON 직렬화"""
    return json.dumps(asdict(parsed), ensure_ascii=False, indent=2)


# =====================================================================
# CLI
# =====================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_input.py <transcript_file> [--mapping='참석자 1 = 호스트']")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        raw_text = f.read()

    mapping_arg = None
    for arg in sys.argv[2:]:
        if arg.startswith("--mapping="):
            mapping_arg = arg.split("=", 1)[1]

    result = parse_transcript(raw_text, mapping_str=mapping_arg)
    print(to_json(result))
