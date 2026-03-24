# XBoxCoverForge 🎮

A Python tool that takes flat Xbox game cover scans and renders them as realistic 3D box art. Batch process your entire collection in seconds!

The name is a nod to Halo's Forge mode — and fittingly, Halo was one of the test cases that helped forge this tool into shape.

---

## Features

- Renders flat cover scans into perspective-correct 3D box art
- Interactive spine alignment tool for fine-tuning per cover
- Batch processes entire cover folders automatically
- Optional gloss/lighting map support for realistic sheen
- Handles covers with pure black artwork correctly (no bleedthrough)

---

## Requirements

Python 3 with the following packages:

```bash
pip install opencv-python numpy
```

---

## Folder Structure

```
XBoxCoverForge/
├── 3d.py               # Main script
├── template.png        # 3D box template image
├── gloss_map.png       # Optional lighting/gloss overlay
├── covers/             # Drop your flat cover scans here
│   └── yourgame.jpg
└── output/             # Rendered 3D boxes saved here
```

---

## Usage

1. Drop your flat cover scans into the `covers/` folder (JPG or PNG)
2. Run the script:

```bash
python 3d.py
```

3. An interactive preview window will open with your first cover
4. Use the **arrow keys** to nudge the spine split left or right until aligned
5. Press **Enter** or **Space** to confirm — all covers in the folder will then be batch processed
6. Press **Escape** to cancel

Rendered 3D boxes are saved to the `output/` folder.

---

## Template

The `template.png` is a pre-made 3D Xbox case shell with transparent areas where the cover art is mapped onto. The `gloss_map.png` is an optional greyscale lighting map applied as a multiply layer to add a realistic gloss effect.

---

## Tuning for Other Console Cases

The key constants at the top of `3d.py` can be adjusted to support other console case formats:

```python
REF_W = 3250          # Reference width all covers are resized to
REF_H = 2148          # Reference height all covers are resized to
SPINE_X_BASE = 1514   # Pixel position where spine meets front cover
SPINE_W = 171         # Width of the spine in pixels
```

The perspective projection points can also be adjusted to match a different template's 3D angle:

```python
pts_spine_dst = np.array([[0, 33], [42, 23], [42, 857], [0, 847]], dtype="float32")
pts_front_dst = np.array([[42, 23], [545, 67], [545, 832], [42, 857]], dtype="float32")
```

---

## Controls

| Key | Action |
|-----|--------|
| ← → Arrow Keys | Nudge spine split left/right |
| Enter / Space | Confirm and batch process |
| Escape | Cancel and exit |

---

## Notes

- Input images can be any resolution — they are automatically resized to the reference dimensions before processing
- The interactive alignment window uses your first cover as a preview — the confirmed offset is then applied to all covers in the batch
- For covers sourced from eBay auction photos or other angled shots, manual perspective correction in an image editor is recommended before running through the tool

---

## License

Do whatever you want with it. 😄
