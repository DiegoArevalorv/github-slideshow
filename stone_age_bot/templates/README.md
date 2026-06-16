# Template Images

Place cropped PNG screenshots of each UI element here.

| Filename | What to crop |
|---|---|
| `red_dot.png` | The small red notification dot (just the dot, ~20×20 px) |
| `golden_backpack.png` | The golden bag icon that appears during the event |
| `claim_all_btn.png` | The "Claim All" / "Reclamar Todo" button |
| `level_up_btn.png` | The "Level Up" / "Subir Nivel" button |
| `ok_button.png` | Any generic OK / Close button |
| `dismantle_all_btn.png` | The "Dismantle All" button inside the bag screen |
| `confirm_btn.png` | The confirmation button in the dismantle dialog |

## How to capture templates

1. Run `python calibrate.py` → choose `s` to save a screenshot.
2. Open `calibration_screen.png` in any image editor.
3. Crop the exact UI element (no padding if possible).
4. Save it here with the filename from the table above.

The more precise the crop, the more reliable the template matching.
