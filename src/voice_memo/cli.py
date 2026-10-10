import argparse
import sys
import os
from .parser import TranscriptParser
from .extractor import ActionItemExtractor
from .summarizer import MeetingSummarizer


def main():
    parser = argparse.ArgumentParser(description="Voice Memo Analyzer - Transkript tahlili va vazifalarni ajratish")
    parser.add_argument("file", help="VTT, SRT yoki matn fayli yo'li")
    parser.add_argument("--out", default="meeting_notes.md", help="Chiqish Markdown fayli")
    parser.add_argument("--title", default="Yig'ilish Bayonnomasi", help="Uchrashuv sarlavhasi")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Fayl topilmadi: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    segments = TranscriptParser.parse_vtt_or_srt(content)
    actions = ActionItemExtractor.extract_actions(segments)
    summary_md = MeetingSummarizer.generate_markdown_summary(args.title, segments, actions)

    with open(args.out, "w", encoding="utf-8") as out_f:
        out_f.write(summary_md)

    print(f"✅ Tahlil yakunlandi! {len(segments)} ta segment, {len(actions)} ta vazifa aniqlandi.")
    print(f"Hujjat saqlandi: {args.out}")


if __name__ == "__main__":
    main()
