# Voice Memo Analyzer

Ovozli xabarlar va video yig'ilishlar transkriptlaridan (VTT, SRT, TXT) muhim vazifalarni (action items), mas'ullarni va muddatlarni avtomatik ajratib oluvchi hamda GitHub Markdown bayonnoma tuzuvchi vosita.

## Xususiyatlari
- **Transkript Formatlari**: WebVTT, SubRip (SRT) va oddiy matnli dialoglarni o'qish va spikerlarni aniqlash.
- **Vazifalar va Mas'ullar**: `@username`, topshiriq kalit so'zlari va muddatlarni (`bugun`, `ertaga`, sana) avtomatik ajratib olish.
- **Chiroyli Bayonnoma**: Ishtirokchilar ro'yxati, checkbox vazifalar va stenogrammani GitHub Flavored Markdown formatida shakllantirish.
- **CLI vositasi**: Istalgan transkript faylini bitta buyruq bilan `meeting_notes.md` ga aylantirish.

## Foydalanish (Python)
```python
from voice_memo import TranscriptParser, ActionItemExtractor, MeetingSummarizer

content = open("meeting.vtt").read()
segments = TranscriptParser.parse_vtt_or_srt(content)
actions = ActionItemExtractor.extract_actions(segments)
summary = MeetingSummarizer.generate_markdown_summary("Sprint Rejasi", segments, actions)
print(summary)
```

## CLI
```bash
voice-memo meeting.vtt --out notes.md --title "Sprint Plan"
```

## Testlar
```bash
pytest tests/ -v
```

## Litsenziya
MIT
