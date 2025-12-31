# CharacterRebuilder: Rigify, Mixamo & DAZ zu Second Life/Opensim How-To

Mit diesem Leitfaden wandelst du ein Rigify-, Mixamo- oder DAZ-Rig in Blender 5 mit dem CharacterRebuilder-Addon in ein Second Life (SL) oder OpenSim-kompatibles Rig um.

## Voraussetzungen

- Blender 5.x
- Addon "CharacterRebuilder" installiert und aktiviert
- Ein Charakter mit Rigify-, Mixamo- oder DAZ-Armature

## Aufgaben (7 Schritte)

1. [x] Addon aktivieren
2. [x] Armature auswählen
3. [x] CharacterRebuilder-Panel öffnen
4. [x] Preset auswählen
5. [x] Knochen umbenennen
6. [x] Gewichte anpassen
7. [x] Einstellungen/Preset speichern (optional)

## Schritt-für-Schritt-Anleitung

### 1. Addon aktivieren

- Öffne Blender und gehe zu **Edit > Preferences > Add-ons**.
- Suche nach "CharacterRebuilder" und aktiviere das Addon.
- Beim Speichern oder Laden muss der Pfad aber jeweils manuell gewählt werden.

### 2. Armature auswählen

- Wähle im 3D-View das Armature-Objekt deines Charakters aus (z.B. "rig", "Armature", "mixamo_armature" oder ähnlich).

### 3. CharacterRebuilder-Panel öffnen

- Wechsle zu den **Objekt-Eigenschaften** (Properties-Fenster, Reiter mit dem gelben Würfel).
- Scrolle nach unten zum Bereich **Character Rebuilder**.

### 4. Preset auswählen

- Wähle im Dropdown-Menü das passende Preset:
  - **Rigify Default** für Rigify-Rigs
  - **Mixamo Default** für Mixamo-Rigs
  - **DAZ Default** für DAZ-Rigs

### 5. Knochen umbenennen

- Klicke auf **Knochen umbenennen**. Das Addon benennt die wichtigsten Bones nach dem SL/OpenSim-Bento-Standard um.
- Prüfe die Liste "Bone-Mapping anzeigen" für nicht gemappte Bones (Warnung bei fehlenden Zuordnungen).

### 6. Gewichte anpassen

- Klicke auf **Knochen gewichten**. Das Addon sorgt dafür, dass alle Vertex Groups zu den neuen Namen passen.

### 7. Einstellungen/Preset speichern (optional)

- Du kannst die aktuelle Zuordnung als Preset speichern (**Eigenes Preset speichern**).
- Einstellungen (inkl. Knochenpositionen und Gewichte) lassen sich als .crc-Datei exportieren und später wieder laden.

## Beispiele für Mixamo und DAZ

### Mixamo-Workflow

1. Importiere dein Mixamo-Charakter (FBX) in Blender.
2. Wähle die Mixamo-Armature (meist "Armature" oder "mixamo_armature").
3. Wähle im CharacterRebuilder-Panel das Preset **Mixamo Default**.
4. Klicke auf **Knochen umbenennen** und dann auf **Knochen gewichten**.
5. Prüfe das Mapping und passe ggf. das Preset an, falls Bones fehlen.

### DAZ-Workflow

1. Importiere dein DAZ-Charakter (z.B. als Collada oder FBX) in Blender.
2. Wähle die DAZ-Armature (meist "Armature" oder "Genesis...").
3. Wähle im CharacterRebuilder-Panel das Preset **DAZ Default**.
4. Klicke auf **Knochen umbenennen** und dann auf **Knochen gewichten**.
5. Prüfe das Mapping und passe ggf. das Preset an, falls Bones fehlen.

## Hinweise & Tipps

- **Backup:** Erstelle vor dem Umbenennen ein Backup deiner Datei.
- **Nicht gemappte Bones:** Manche Bones werden nicht automatisch gemappt. Diese müssen ggf. manuell zugeordnet werden (Preset erweitern).
- **Meshes:** Stelle sicher, dass alle Meshes mit dem Armature Modifier auf das gewählte Rig zeigen.
- **Kompatibilität:** Das Addon orientiert sich am Bento-Standard von Second Life/OpenSim.

## Fehlerbehebung

- **Buttons fehlen:** Blender neu starten und Addon erneut aktivieren.
- **Warnungen zu nicht gemappten Bones:** Preset anpassen oder Mapping-Liste erweitern.
- **Addon-Einstellungen:** Unter Edit > Preferences > Add-ons > CharacterRebuilder findest du den .crc-Pfad.

---

Viel Erfolg beim Konvertieren deines Rigs für Second Life & OpenSim!
