import pytest
from voice_memo.parser import TranscriptParser
from voice_memo.extractor import ActionItemExtractor
from voice_memo.summarizer import MeetingSummarizer


def test_vtt_parsing():
    vtt = """WEBVTT

00:00:01.000 --> 00:00:05.000
<v Sardor>Salom hammaga, bugungi mitingni boshlaymiz.

00:00:06.000 --> 00:00:10.000
<v Nodir>Salom Sardor. Biz server konfiguratsiyasini tugatdik.
"""
    segments = TranscriptParser.parse_vtt_or_srt(vtt)
    assert len(segments) == 2
    assert segments[0].speaker == "Sardor"
    assert "mitingni boshlaymiz" in segments[0].text
    assert segments[1].speaker == "Nodir"


def test_action_item_extraction():
    plain = """
Ali: Biz bugun yangi landing page'ni deploy qilishimiz kerak.
Vali: Xo'p, topshiriq: @Bobur ertaga testlarni tekshirsin.
"""
    segments = TranscriptParser.parse_vtt_or_srt(plain)
    actions = ActionItemExtractor.extract_actions(segments)

    assert len(actions) >= 1
    # Bobur mas'ul etib topilgan bo'lishi kerak
    bobur_action = [a for a in actions if a.assignee == "Bobur"]
    assert len(bobur_action) == 1
    assert "ertaga" in bobur_action[0].deadline


def test_meeting_summary_generator():
    segments = TranscriptParser.parse_vtt_or_srt("Dilshod: Yangi release tayyor.")
    actions = ActionItemExtractor.extract_actions(segments)
    md = MeetingSummarizer.generate_markdown_summary("Haftalik Reja", segments, actions)

    assert "# 🎙 Haftalik Reja" in md
    assert "Dilshod" in md
