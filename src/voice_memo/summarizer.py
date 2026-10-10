from typing import List
from .parser import TranscriptSegment
from .extractor import ActionItemExtractor, ActionItem


class MeetingSummarizer:
    """Yig'ilish bayonnomasi (meeting notes) va xulosasini shakllantirish."""

    @staticmethod
    def generate_markdown_summary(title: str, segments: List[TranscriptSegment], actions: List[ActionItem]) -> str:
        speakers = sorted(list(set(s.speaker for s in segments if s.speaker != "Noma'lum")))

        lines = [
            f"# 🎙 {title}",
            "",
            "## 👥 Ishtirokchilar",
        ]
        if speakers:
            for sp in speakers:
                lines.append(f"- {sp}")
        else:
            lines.append("- Umumiy ishtirokchilar")

        lines.extend([
            "",
            "## ✅ Belgilangan Vazifalar (Action Items)",
        ])

        if actions:
            for item in actions:
                lines.append(f"- [ ] **{item.task}**")
                lines.append(f"  - 👤 Mas'ul: `{item.assignee}`")
                lines.append(f"  - ⏱ Muddat: `{item.deadline}` (Vaqt tamg'asi: {item.source_timestamp})")
        else:
            lines.append("Aniq vazifalar belgilanmadi.")

        lines.extend([
            "",
            "## 📝 Suhbat Stenogrammasi (Asosiy qismlar)",
        ])

        for s in segments[:10]:
            lines.append(f"> **[{s.start_time}] {s.speaker}:** {s.text}")

        return "\n".join(lines)
