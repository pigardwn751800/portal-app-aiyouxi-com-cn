from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class KeywordNote:
    """A single keyword note with related metadata."""
    keyword: str
    note: str
    source_url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def formatted_entry(self) -> str:
        """Return a human-readable formatted string for this note."""
        lines = [
            f"Keyword: {self.keyword}",
            f"Note:    {self.note}",
            f"Source:  {self.source_url}",
            f"Tags:    {', '.join(self.tags) if self.tags else '(none)'}",
            f"Created: {self.created_at}",
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Convert to a plain dictionary."""
        return asdict(self)


@dataclass
class KeywordNotesCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def add_notes(self, *notes: KeywordNote) -> None:
        for n in notes:
            self.notes.append(n)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all(self) -> str:
        """Return a formatted string of all notes in the collection."""
        if not self.notes:
            return "No notes in collection."
        parts = []
        for i, note in enumerate(self.notes, 1):
            parts.append(f"--- Note {i} ---")
            parts.append(note.formatted_entry())
        return "\n".join(parts)

    def summary_report(self) -> str:
        """Return a short summary count and top keywords."""
        if not self.notes:
            return "No notes."
        keyword_counts = {}
        for n in self.notes:
            keyword_counts[n.keyword] = keyword_counts.get(n.keyword, 0) + 1
        top_keyword = max(keyword_counts, key=keyword_counts.get)
        return (
            f"Total notes: {len(self.notes)}\n"
            f"Unique keywords: {len(keyword_counts)}\n"
            f"Most frequent keyword: '{top_keyword}' ({keyword_counts[top_keyword]} occurrences)"
        )


def create_sample_collection() -> KeywordNotesCollection:
    """Create and return a sample keyword notes collection."""
    collection = KeywordNotesCollection()
    collection.add_notes(
        KeywordNote(
            keyword="爱游戏",
            note="用户对游戏平台的关注和喜爱",
            source_url="https://portal-app-aiyouxi.com.cn",
            tags=["游戏", "用户", "情感"],
        ),
        KeywordNote(
            keyword="爱游戏",
            note="游戏社区活跃度分析",
            source_url="https://portal-app-aiyouxi.com.cn/community",
            tags=["游戏", "社区", "数据"],
        ),
        KeywordNote(
            keyword="游戏推荐",
            note="基于用户偏好的游戏推荐系统",
            source_url="https://portal-app-aiyouxi.com.cn/recommend",
            tags=["推荐", "算法"],
        ),
        KeywordNote(
            keyword="爱游戏",
            note="平台日活跃用户增长趋势",
            source_url="https://portal-app-aiyouxi.com.cn/stats",
            tags=["游戏", "增长", "统计"],
        ),
        KeywordNote(
            keyword="用户反馈",
            note="收集用户对游戏体验的反馈",
            source_url="https://portal-app-aiyouxi.com.cn/feedback",
            tags=["反馈", "UX"],
        ),
    )
    return collection


def main():
    """Run a quick demo of the keyword notes module."""
    collection = create_sample_collection()

    print("=== All Notes ===")
    print(collection.format_all())
    print()

    print("=== Summary ===")
    print(collection.summary_report())
    print()

    print("=== Notes for keyword '爱游戏' ===")
    for note in collection.find_by_keyword("爱游戏"):
        print(note.formatted_entry())
        print()

    print("=== Notes with tag '反馈' ===")
    for note in collection.find_by_tag("反馈"):
        print(note.formatted_entry())
        print()


if __name__ == "__main__":
    main()