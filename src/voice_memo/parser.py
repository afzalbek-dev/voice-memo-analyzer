import re
from dataclasses import dataclass
from typing import List


@dataclass
class TranscriptSegment:
    start_time: str
    end_time: str
    speaker: str
    text: str


class TranscriptParser:
    """VTT, SRT yoki oddiy matnli transkriptlarni segmentlarga ajratish."""

    @staticmethod
    def parse_vtt_or_srt(content: str) -> List[TranscriptSegment]:
        segments: List[TranscriptSegment] = []
        # VTT/SRT vaqt tamg'alari: 00:01:23.456 --> 00:01:28.000 yoki 00:01:23,456 --> 00:01:28,000
        pattern = re.compile(
            r"(\d{2}:\d{2}(?::\d{2})?[.,]\d{3})\s*-->\s*(\d{2}:\d{2}(?::\d{2})?[.,]\d{3})\s*\n(?:<v\s+([^>]+)>)?([^\n]+(?:\n[^\n]+)*)",
            re.MULTILINE,
        )

        for match in pattern.finditer(content):
            start = match.group(1).replace(",", ".")
            end = match.group(2).replace(",", ".")
            vtt_speaker = match.group(3) or ""
            raw_text = match.group(4).strip()

            speaker = vtt_speaker
            # "Ali: Salom hammaga" formatini tekshirish
            sp_match = re.match(r"^([A-Z\u0410-\u042f][a-zA-Z\u0400-\u04FF\s_0-9]{1,20}):\s*(.*)", raw_text)
            if sp_match and not speaker:
                speaker = sp_match.group(1).strip()
                clean_text = sp_match.group(2).strip()
            else:
                clean_text = raw_text

            segments.append(
                TranscriptSegment(
                    start_time=start,
                    end_time=end,
                    speaker=speaker or "Noma'lum",
                    text=clean_text,
                )
            )

        if not segments:
            # Agar VTT format bo'lmasa, oddiy satrlardan parsing
            lines = [l.strip() for l in content.split("\n") if l.strip()]
            for i, line in enumerate(lines):
                sp_match = re.match(r"^([A-Z\u0410-\u042f][a-zA-Z\u0400-\u04FF\s_0-9]{1,20}):\s*(.*)", line)
                if sp_match:
                    speaker = sp_match.group(1).strip()
                    txt = sp_match.group(2).strip()
                else:
                    speaker = "Noma'lum"
                    txt = line
                segments.append(
                    TranscriptSegment(
                        start_time=f"00:{i:02d}:00",
                        end_time=f"00:{i:02d}:30",
                        speaker=speaker,
                        text=txt,
                    )
                )

        return segments
