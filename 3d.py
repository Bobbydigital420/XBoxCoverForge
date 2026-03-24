import cv2
import numpy as np
import os
import glob

# --- REFERENCE CONSTANTS ---
REF_W = 3250
REF_H = 2148
SPINE_X_BASE = 1514
SPINE_W = 171

def render_3d_box(input_path, template_path, output_path, offset=0):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    raw_scan = cv2.imread(input_path)
    if raw_scan is None or template is None: return

    full_scan = cv2.resize(raw_scan, (REF_W, REF_H), interpolation=cv2.INTER_LANCZOS4)

    actual_x = SPINE_X_BASE + offset
    # Extract with precise boundaries
    spine_img = full_scan[:, actual_x : (actual_x + SPINE_W)]
    front_img = full_scan[:, (actual_x + SPINE_W) :]

    # --- DEFINITIVE PROJECTION POINTS ---
    # These coordinates map the spine/front to the template's perspective precisely.
    pts_spine_dst = np.array([[0, 38], [42, 23], [42, 857], [0, 847]], dtype="float32")
    pts_front_dst = np.array([[42, 23], [545, 67], [545, 832], [42, 857]], dtype="float32")

    def warp_it(img, dst_pts):
        h, w = img.shape[:2]
        src_pts = np.array([[0,0], [w,0], [w,h], [0,h]], dtype="float32")
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(img, matrix, (template.shape[1], template.shape[0]), flags=cv2.INTER_CUBIC)
        # Create mask by warping a solid white rectangle - gets exact region regardless of pixel color
        white = np.ones((h, w), dtype=np.uint8) * 255
        mask = cv2.warpPerspective(white, matrix, (template.shape[1], template.shape[0]))
        return warped, mask

    # Warp and Composite
    warped_f, mask_f = warp_it(front_img, pts_front_dst)
    warped_s, mask_s = warp_it(spine_img, pts_spine_dst)

    final = template.copy()
    # Apply front first, then spine on top using their exact warp masks
    for part, mask in [(warped_f, mask_f), (warped_s, mask_s)]:
        m = mask > 0
        final[m, :3] = part[m, :3]

    # Apply Lighting Map (Multiply)
    gloss_file = "gloss_map.png"
    if os.path.exists(gloss_file):
        l_map = cv2.imread(gloss_file, cv2.IMREAD_GRAYSCALE)
        if l_map is not None:
            l_map = cv2.resize(l_map, (final.shape[1], final.shape[0]))
            norm_map = l_map.astype(float) / 255.0
            for c in range(3):
                final[:, :, c] = (final[:, :, c] * norm_map).astype(np.uint8)

    cv2.imwrite(output_path, final)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir: os.chdir(script_dir)
    
    if not os.path.exists("output"): os.makedirs("output")
        
    exts = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    cover_files = [f for ext in exts for f in glob.glob(os.path.join("covers", ext))]

    if not cover_files:
        print("Error: No images found in 'covers/' folder.")
        exit()

    # Interactive Tool
    win_name = "ADJUST SPINE: [Arrows] Nudge | [Enter] Confirm"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 800, 1000)
    
    offset = 0
    while True:
        render_3d_box(cover_files[0], "template.png", "preview_temp.png", offset)
        preview = cv2.imread("preview_temp.png")
        if preview is not None:
            cv2.imshow(win_name, preview)
        
        key = cv2.waitKey(0)
        if key in [81, 2, 63234]: offset -= 1
        elif key in [83, 3, 63235]: offset += 1
        elif key in [13, 32]: break
        elif key == 27: 
            cv2.destroyAllWindows()
            exit()
    
    cv2.destroyAllWindows()
    if os.path.exists("preview_temp.png"): os.remove("preview_temp.png")

    for f in cover_files:
        filename = os.path.basename(f)
        if "template.png" in filename.lower(): continue
        out_path = os.path.join("output", os.path.splitext(filename)[0] + ".png")
        render_3d_box(f, "template.png", out_path, offset)
        print(f"SUCCESS: {filename}")
