#!/usr/bin/env python3
"""
Update README with comments and KI responses from comment_here.md
"""

import re
import json
import os
from datetime import datetime
import requests

# Hugging Face API endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def get_ai_response(question, tags, hf_token):
    """
    Get response from Hugging Face KI
    """
    if not hf_token:
        print("⚠️  HUGGING_FACE_TOKEN nicht gesetzt, überspringen KI-Antwort")
        return None
    
    try:
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Prompt basierend auf Tags
        system_prompt = "Du bist ein hilfreicher KI-Assistent für das Blue Blocker ESP32 Projekt. Antworte kurz und prägnant (max 2-3 Sätze)."
        
        if "@python" in tags:
            system_prompt += " Konzentriere dich auf Python-Lösungen."
        if "@c++" in tags:
            system_prompt += " Konzentriere dich auf C++-Lösungen."
        if "@hardware" in tags:
            system_prompt += " Konzentriere dich auf Hardware-Aspekte."
        if "@nrf24" in tags:
            system_prompt += " Du sprichst speziell über das NRF24-Modul."
        if "@esp32" in tags:
            system_prompt += " Du sprichst speziell über ESP32."
        
        prompt = f"{system_prompt}\n\nFrage: {question}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                # Extrahiere nur die Antwort (nach dem Prompt)
                if "Frage:" in text:
                    answer = text.split("Frage:")[1].strip()
                else:
                    answer = text.strip()
                return answer[:200]  # Max 200 Zeichen
        else:
            print(f"⚠️  HF API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ KI-Fehler: {e}")
        return None

def extract_comments_from_file():
    """
    Extract comments from comment_here.md
    """
    comments_data = {}
    
    try:
        with open("comment_here.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ comment_here.md nicht gefunden")
        return comments_data
    
    # Pattern: ### [TAG_NAME] oder ### [tag]
    section_pattern = r"###\s*\[([^\]]+)\]"
    # Pattern für Kommentare: - **@username** (DATUM): "text" `tags: ...`
    comment_pattern = r"-\s*\*\*@([^*]+)\*\*\s*\(([^)]+)\):\s*\"([^\"]+)\"\s*`tags:\s*([^`]+)`"
    
    sections = re.split(section_pattern, content)
    
    for i in range(1, len(sections), 2):
        tag_name = sections[i]
        section_content = sections[i+1] if i+1 < len(sections) else ""
        
        if tag_name not in comments_data:
            comments_data[tag_name] = []
        
        # Finde alle Kommentare in diesem Abschnitt
        matches = re.finditer(comment_pattern, section_content)
        for match in matches:
            username = match.group(1)
            date = match.group(2)
            comment_text = match.group(3)
            tags_str = match.group(4)
            
            comments_data[tag_name].append({
                "username": username,
                "date": date,
                "comment": comment_text,
                "tags": [t.strip() for t in tags_str.split(",")]
            })
    
    return comments_data

def generate_readme(comments_data, hf_token):
    """
    Generate README with comments and KI responses
    """
    readme_content = """# 🔵 Blue Blocker - ESP32 Bluetooth Jammer Test Bench

## 📋 Project Overview

...[rest of your README]...

---

## 💬 Community Feedback & KI-Responses

"""
    
    for tag_name, comments in comments_data.items():
        if comments:  # Nur wenn Kommentare vorhanden sind
            readme_content += f"\n### [{tag_name.upper()}]\n\n"
            
            for comment in comments:
                readme_content += f"**@{comment['username']}** ({comment['date']}):\n"
                readme_content += f"> {comment['comment']}\n\n"
                
                # Wenn @git_ai Tag vorhanden, KI-Antwort holen
                if "@git_ai" in comment["tags"]:
                    print(f"🤖 Getting KI response for @{comment['username']}...")
                    ai_response = get_ai_response(comment["comment"], comment["tags"], hf_token)
                    
                    if ai_response:
                        readme_content += f"🤖 **KI-Antwort:** _{ai_response}_\n\n"
                    else:
                        readme_content += f"🤖 **KI-Antwort:** _[KI antwortet in Kürze...]_\n\n"
                
                readme_content += "---\n\n"
    
    return readme_content

def update_readme_file(new_feedback_section):
    """
    Update README.md with new feedback section
    """
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme = f.read()
    except FileNotFoundError:
        print("❌ README.md nicht gefunden")
        return False
    
    # Finde den Feedback-Bereich oder füge ihn am Ende ein
    if "## 💬 Community Feedback" in readme:
        # Ersetze existierenden Feedback-Bereich
        pattern = r"## 💬 Community Feedback.*?(?=\n## |\Z)"
        readme = re.sub(pattern, new_feedback_section.rstrip() + "\n", readme, flags=re.DOTALL)
    else:
        # Füge am Ende ein
        readme += f"\n{new_feedback_section}"
    
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        print("✅ README.md aktualisiert!")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Schreiben von README.md: {e}")
        return False

def main():
    print("🚀 Starte Comment Update System...\n")
    
    # Get HuggingFace Token from environment
    hf_token = os.getenv("HUGGING_FACE_TOKEN")
    
    # Extract comments
    print("📖 Lese Kommentare aus comment_here.md...")
    comments_data = extract_comments_from_file()
    
    if not comments_data:
        print("⚠️  Keine Kommentare gefunden")
        return
    
    print(f"✅ {sum(len(c) for c in comments_data.values())} Kommentare gefunden\n")
    
    # Generate README section
    print("📝 Generiere README-Sektion...")
    feedback_section = generate_readme(comments_data, hf_token)
    
    # Update README
    print("💾 Speichere README.md...")
    update_readme_file(feedback_section)
    
    print("\n✨ Fertig!")

if __name__ == "__main__":
    main()
