import re
from dataclasses import dataclass
from typing import List
from .parser import TranscriptSegment


@dataclass
class ActionItem:
    task: str
    assignee: str
    deadline: str
    source_timestamp: str


class ActionItemExtractor:
    """Matndan topshiriqlar, mas'ullar va muddatlarni ajratib oluvchi modul."""

    TASK_TRIGGERS = [
        re.compile(r"(?i)(vazifa|topshiriq|kerak|shart|qilishimiz kerak|tayyorlash kerak|yuborish kerak)[\s:]+(.*)"),
        re.compile(r"(?i)(todo|action item|task)[\s:]+(.*)"),
    ]

    ASSIGNEE_PATTERN = re.compile(r"(?:@([a-zA-Z0-9_]+)|(?:mas'ul|javobgar)[\s:]+([a-zA-Z\u0400-\u04FF]+))")
    DEADLINE_PATTERN = re.compile(r"(?i)(bugun|ertaga|dushanba|seshanba|chorshanba|payshanba|juma|shanba|yakshanba|hafta oxirigacha|\d{1,2}-[a-zA-Z\u0400-\u04FF]+)")

    @classmethod
    def extract_actions(cls, segments: List[TranscriptSegment]) -> List[ActionItem]:
        actions: List[ActionItem] = []

        for seg in segments:
            text = seg.text
            for trigger in cls.TASK_TRIGGERS:
                match = trigger.search(text)
                if match:
                    task_text = match.group(0).strip()
                    assignee = seg.speaker

                    # Mas'ul shaxsni aniqlash
                    assignee_match = cls.ASSIGNEE_PATTERN.search(text)
                    if assignee_match:
                        assignee = assignee_match.group(1) or assignee_match.group(2)

                    # Muddatni aniqlash
                    deadline = "Ko'rsatilmagan"
                    deadline_match = cls.DEADLINE_PATTERN.search(text)
                    if deadline_match:
                        deadline = deadline_match.group(0)

                    actions.append(
                        ActionItem(
                            task=task_text,
                            assignee=assignee,
                            deadline=deadline,
                            source_timestamp=seg.start_time,
                        )
                    )
                    break

        return actions
