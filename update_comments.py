#!/usr/bin/env python3
"""
Blue Blocker - Kommentar-Management System
Dieses Skript liest Kommentare aus comment_here.md und aktualisiert die README
"""

import json
import re
from datetime import datetime
from pathlib import Path

def read_comments_from_md():
    """Liest Kommentare aus comment_here.md"""
    comment_file = Path("comment_here.md")
    
    if not comment_file.exists():
        print("❌ comment_here.md nicht gefunden!")
        return []
    
    with open(comment_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex zum Extrahieren von Kommentaren: ### [TAG] - **@username** (DATE): "comment"
    pattern = r'### \[(\w+)\]\s*\n- \*\*@(\w+)\*\* \((\d{2}\.\d{2}\.\d{4})\): "(.+?)"'
    matches = re.findall(pattern, content)
    
    comments = []
    for tag, username, date, comment_text in matches:
        comments.append({
            "tag": tag,
            "author": username,
            "date": date,
            "content": comment_text
        })
    
    return comments

def update_readme(comments):
    """Aktualisiert die README mit Kommentaren"""
    readme_file = Path("README.md")
    
    if not readme_file.exists():
        print("❌ README.md nicht gefunden!")
        return
    
    with open(readme_file, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # Erstelle Feedback-Sektion
    feedback_section = generate_feedback_section(comments)
    
    # Wenn Feedback-Sektion bereits existiert, ersetze sie
    if "## 💬 Was halten andere von Blue Blocker?" in readme_content:
        pattern = r"## 💬 Was halten andere von Blue Blocker\?.*?(?=\n## |\Z)"
        readme_content = re.sub(pattern, feedback_section.rstrip(), readme_content, flags=re.DOTALL)
    else:
        # Füge vor dem letzten "---" oder am Ende ein
        readme_content = readme_content.rstrip() + "\n\n" + feedback_section
    
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.md aktualisiert!")

def generate_feedback_section(comments):
    """Generiert die Feedback-Sektion für README"""
    section = "## 💬 Was halten andere von Blue Blocker?\n\n"
    
    if not comments:
        section += "Noch keine Kommentare. Sei der erste! 🎉\n"
        return section
    
    # Gruppiere Kommentare nach Tag
    tags_dict = {}
    for comment in comments:
        tag = comment["tag"]
        if tag not in tags_dict:
            tags_dict[tag] = []
        tags_dict[tag].append(comment)
    
    # Erstelle formatierte Ausgabe
    for tag, tag_comments in sorted(tags_dict.items()):
        section += f"### 🏷️ {tag.upper()}\n"
        for comment in tag_comments:
            section += f"- **@{comment['author']}** ({comment['date']}): \"{comment['content']}\"\n"
        section += "\n"
    
    return section

def save_to_json(comments):
    """Speichert Kommentare als JSON"""
    json_file = Path("comments.json")
    
    data = {
        "last_updated": datetime.now().isoformat(),
        "total_comments": len(comments),
        "comments": comments,
        "tags": ["performance", "design", "features", "documentation", "security", "speed", "bug", "improvement"]
    }
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(comments)} Kommentare in comments.json gespeichert!")

def main():
    """Hauptfunktion"""
    print("🔄 Blue Blocker - Kommentar-System wird aktualisiert...")
    print()
    
    # Lese Kommentare
    comments = read_comments_from_md()
    print(f"📖 {len(comments)} Kommentare gelesen")
    
    # Speichere als JSON
    save_to_json(comments)
    
    # Aktualisiere README
    update_readme(comments)
    
    print()
    print("✨ Fertig! Kommentare wurden aktualisiert!")

if __name__ == "__main__":
    main()
