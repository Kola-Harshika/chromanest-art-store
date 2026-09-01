# -*- coding: utf-8 -*-
"""
CHROMANEST - Procedural Art Asset Generator
Generates high-resolution, realistic, premium artwork visuals for all store products and pages.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'static', 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. CORE PROCEDURAL NOISE & TEXTURE UTILITIES
# -----------------------------------------------------------------------------

def generate_noise(w, h, scale=50.0, octaves=4, persistence=0.5, seed=42):
    """Generates multi-octave 2D fractal noise using smoothstep bilinear interpolation."""
    np.random.seed(seed)
    grid_w = max(2, int(w / scale))
    grid_h = max(2, int(h / scale))
    
    total = np.zeros((h, w), dtype=np.float32)
    amplitude = 1.0
    max_amp = 0.0
    
    for _ in range(octaves):
        rand_lattice = np.random.rand(grid_h + 2, grid_w + 2).astype(np.float32)
        
        y_coords = np.linspace(0, grid_h, h, endpoint=False)
        x_coords = np.linspace(0, grid_w, w, endpoint=False)
        
        y0 = y_coords.astype(int)
        y1 = y0 + 1
        x0 = x_coords.astype(int)
        x1 = x0 + 1
        
        dy = (y_coords - y0)[:, None]
        dx = (x_coords - x0)[None, :]
        
        sy = dy * dy * (3 - 2 * dy)
        sx = dx * dx * (3 - 2 * dx)
        
        c00 = rand_lattice[y0[:, None], x0[None, :]]
        c10 = rand_lattice[y1[:, None], x0[None, :]]
        c01 = rand_lattice[y0[:, None], x1[None, :]]
        c11 = rand_lattice[y1[:, None], x1[None, :]]
        
        top = c00 * (1 - sx) + c01 * sx
        bottom = c10 * (1 - sx) + c11 * sx
        layer = top * (1 - sy) + bottom * sy
        
        total += layer * amplitude
        max_amp += amplitude
        amplitude *= persistence
        grid_w *= 2
        grid_h *= 2
        
    return total / max_amp

def add_canvas_texture(image, intensity=0.06):
    """Applies realistic fine linen canvas weave grain."""
    w, h = image.size
    y_idx, x_idx = np.indices((h, w))
    weave = (np.sin(x_idx * 1.6) * 0.5 + np.sin(y_idx * 1.6) * 0.5) * 0.5 + 0.5
    noise = np.random.normal(0, 0.4, (h, w))
    grain = (weave * 0.5 + noise * 0.5) * intensity
    
    img_arr = np.array(image, dtype=np.float32) / 255.0
    if len(img_arr.shape) == 3:
        grain = grain[:, :, None]
    
    textured = np.clip(img_arr * (1.0 - grain + 0.5 * intensity), 0, 1)
    return Image.fromarray((textured * 255).astype(np.uint8))

def add_paper_texture(image, intensity=0.04):
    """Applies fine cotton rag archival paper mottling."""
    w, h = image.size
    noise = generate_noise(w, h, scale=14.0, octaves=3, seed=202)
    grain = (noise - 0.5) * intensity
    
    img_arr = np.array(image, dtype=np.float32) / 255.0
    if len(img_arr.shape) == 3:
        grain = grain[:, :, None]
        
    textured = np.clip(img_arr + grain, 0, 1)
    return Image.fromarray((textured * 255).astype(np.uint8))

def create_gold_foil_texture(w, h, seed=777):
    """Creates a shimmering 24K gold foil texture with micro-facets."""
    noise1 = generate_noise(w, h, scale=35.0, octaves=4, seed=seed)
    noise2 = generate_noise(w, h, scale=6.0, octaves=3, seed=seed+1)
    
    base_gold = np.array([214, 168, 48], dtype=np.float32)
    bright_gold = np.array([255, 238, 150], dtype=np.float32)
    deep_gold = np.array([162, 108, 20], dtype=np.float32)
    
    blend = (noise1 * 0.7 + noise2 * 0.3)[:, :, None]
    
    gold_arr = np.where(blend > 0.5,
                        base_gold + (bright_gold - base_gold) * ((blend - 0.5) * 2),
                        deep_gold + (base_gold - deep_gold) * (blend * 2))
    
    sparkle = np.random.rand(h, w, 1)
    gold_arr = np.where(sparkle > 0.965, np.minimum(255, gold_arr + 65), gold_arr)
    return Image.fromarray(np.clip(gold_arr, 0, 255).astype(np.uint8))

def draw_vignette(image, strength=0.22):
    """Soft atmospheric edge vignette."""
    w, h = image.size
    vignette = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(vignette)
    cx, cy = w / 2, h / 2
    max_radius = math.sqrt(cx**2 + cy**2)
    for r in range(int(max_radius), 0, -12):
        alpha = int(255 * (1 - (r / max_radius) ** 2))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=24))
    vig_arr = np.array(vignette, dtype=np.float32) / 255.0
    img_arr = np.array(image, dtype=np.float32)
    factor = 1.0 - (1.0 - vig_arr[:, :, None]) * strength
    return Image.fromarray(np.clip(img_arr * factor, 0, 255).astype(np.uint8))

# -----------------------------------------------------------------------------
# 2. INDIVIDUAL ARTWORK GENERATORS
# -----------------------------------------------------------------------------

def render_ethereal_whispers(w=800, h=800):
    """1. Ethereal Whispers - Abstract Oil & 24K Gold Leaf on Linen"""
    img = Image.new("RGB", (w, h), (245, 240, 235))
    
    # Layered fluid noise fields
    n1 = generate_noise(w, h, scale=180.0, octaves=5, seed=101)
    n2 = generate_noise(w, h, scale=90.0, octaves=4, seed=102)
    n3 = generate_noise(w, h, scale=40.0, octaves=3, seed=103)
    
    # Color palette
    plum = np.array([42, 28, 48], dtype=np.float32)       # Deep violet-plum
    mauve = np.array([142, 114, 138], dtype=np.float32)   # Dusty lavender
    blush = np.array([230, 195, 185], dtype=np.float32)   # Warm blush
    cream = np.array([250, 245, 238], dtype=np.float32)   # Linen cream
    amber = np.array([195, 135, 75], dtype=np.float32)    # Warm ochre
    
    # Compose organic fluid gradient fields
    field = n1 * 0.55 + n2 * 0.35 + n3 * 0.1
    y_grad = np.linspace(0, 1, h)[:, None]
    comp = field * 0.7 + y_grad * 0.3
    
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            val = comp[y, x]
            if val < 0.35:
                t = val / 0.35
                arr[y, x] = plum * (1 - t) + mauve * t
            elif val < 0.65:
                t = (val - 0.35) / 0.30
                arr[y, x] = mauve * (1 - t) + blush * t
            elif val < 0.85:
                t = (val - 0.65) / 0.20
                arr[y, x] = blush * (1 - t) + cream * t
            else:
                t = (val - 0.85) / 0.15
                arr[y, x] = cream * (1 - t) + amber * t
                
    base_img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    # Add fluid 24K Gold Leaf rivers
    gold_tex = create_gold_foil_texture(w, h, seed=888)
    gold_mask = Image.new("L", (w, h), 0)
    gdraw = ImageDraw.Draw(gold_mask)
    
    # Draw organic winding golden veins
    points = []
    x_cur, y_cur = w * 0.2, h * 0.85
    for i in range(25):
        points.append((x_cur, y_cur))
        x_cur += random.uniform(15, 35)
        y_cur -= random.uniform(20, 45) + math.sin(i * 0.5) * 15
        
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        width = int(6 + math.sin(i * 0.4) * 4 + random.uniform(0, 3))
        gdraw.line([p1, p2], fill=255, width=width)
        # Small branching gold flecks
        if i % 3 == 0:
            branch_end = (p1[0] + random.uniform(-40, 40), p1[1] + random.uniform(-30, 30))
            gdraw.line([p1, branch_end], fill=200, width=max(1, width - 3))
            
    # Gold spatter flecks
    for _ in range(80):
        fx = random.randint(int(w * 0.15), int(w * 0.85))
        fy = random.randint(int(h * 0.15), int(h * 0.85))
        fr = random.randint(1, 4)
        gdraw.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=random.randint(180, 255))
        
    gold_mask = gold_mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    base_img.paste(gold_tex, (0, 0), gold_mask)
    
    # Apply linen canvas texture and vignette
    result = add_canvas_texture(base_img, intensity=0.07)
    result = draw_vignette(result, strength=0.2)
    return result

def render_golden_horizon(w=800, h=800):
    """2. Golden Horizon - Textured Impasto Landscape on Gallery Canvas"""
    # Sunset sky gradient
    sky = np.zeros((h, w, 3), dtype=np.float32)
    indigo = np.array([28, 24, 45], dtype=np.float32)       # Dusk indigo
    sienna = np.array([178, 65, 32], dtype=np.float32)      # Burnt sienna
    gold = np.array([235, 165, 35], dtype=np.float32)       # Molten gold
    peach = np.array([250, 215, 175], dtype=np.float32)     # Peach mist
    
    n_sky = generate_noise(w, h, scale=120.0, octaves=4, seed=201)
    
    for y in range(h):
        t = (y / h)
        if t < 0.35:
            factor = t / 0.35
            base = indigo * (1 - factor) + sienna * factor
        elif t < 0.65:
            factor = (t - 0.35) / 0.30
            base = sienna * (1 - factor) + gold * factor
        else:
            factor = (t - 0.65) / 0.35
            base = gold * (1 - factor) + peach * factor
        sky[y, :] = base + (n_sky[y, :] - 0.5)[:, None] * 25
        
    img = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Glowing sun disc
    sun_x, sun_y = w * 0.55, h * 0.52
    for r in range(120, 0, -5):
        alpha = int(90 * (1 - (r / 120) ** 1.5))
        draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, 245, 200, alpha))
        
    # Layered mountain ridges with palette knife impasto
    ridges = [
        {"y_base": h * 0.58, "color": (85, 45, 40), "amp": 45, "freq": 0.006, "seed": 10},
        {"y_base": h * 0.68, "color": (50, 28, 32), "amp": 60, "freq": 0.008, "seed": 20},
        {"y_base": h * 0.78, "color": (25, 18, 28), "amp": 75, "freq": 0.010, "seed": 30}
    ]
    
    for ridge in ridges:
        r_pts = [(0, h)]
        n_r = generate_noise(w, 1, scale=50.0, octaves=3, seed=ridge["seed"])[0]
        for x in range(0, w + 10, 5):
            y_val = ridge["y_base"] - math.sin(x * ridge["freq"]) * ridge["amp"] - n_r[min(w-1, x)] * 35
            r_pts.append((x, y_val))
        r_pts.append((w, h))
        draw.polygon(r_pts, fill=ridge["color"] + (255,))
        
    # Shimmering golden lake reflection
    gold_foil = create_gold_foil_texture(w, h, seed=444)
    water_mask = Image.new("L", (w, h), 0)
    wdraw = ImageDraw.Draw(water_mask)
    for y_pos in range(int(h * 0.78), h, 4):
        len_bar = random.randint(int(w * 0.2), int(w * 0.7))
        start_x = int(w * 0.55 - len_bar / 2 + random.randint(-20, 20))
        wdraw.line([(start_x, y_pos), (start_x + len_bar, y_pos)], fill=random.randint(120, 240), width=random.randint(1, 3))
        
    img.paste(gold_foil, (0, 0), water_mask)
    result = add_canvas_texture(img, intensity=0.08)
    return draw_vignette(result, strength=0.25)

def render_serenade_indigo(w=800, h=800):
    """3. Serenade in Indigo - Deep Mineral Pigment Wash on Archival Rag Paper"""
    # Off-white deckled paper
    paper = Image.new("RGB", (w, h), (248, 246, 240))
    
    # Layered pigment bleed noise
    n_deep = generate_noise(w, h, scale=100.0, octaves=5, seed=301)
    n_mid = generate_noise(w, h, scale=50.0, octaves=4, seed=302)
    n_fine = generate_noise(w, h, scale=18.0, octaves=3, seed=303)
    
    lapis = np.array([12, 32, 68], dtype=np.float32)       # Lapis lazuli
    prussian = np.array([6, 18, 42], dtype=np.float32)     # Prussian blue
    cerulean = np.array([45, 95, 145], dtype=np.float32)   # Mist indigo
    mist = np.array([215, 225, 235], dtype=np.float32)     # Mineral mist
    paper_col = np.array([248, 246, 240], dtype=np.float32)
    
    cx, cy = w * 0.48, h * 0.52
    y_idx, x_idx = np.indices((h, w))
    dist = np.sqrt(((x_idx - cx) / (w * 0.42))**2 + ((y_idx - cy) / (h * 0.42))**2)
    
    bleed = (n_deep * 0.5 + n_mid * 0.35 + n_fine * 0.15) - (dist * 0.6)
    
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            b = bleed[y, x]
            if b > 0.45:
                t = min(1.0, (b - 0.45) / 0.3)
                arr[y, x] = lapis * (1 - t) + prussian * t
            elif b > 0.2:
                t = (b - 0.2) / 0.25
                arr[y, x] = cerulean * (1 - t) + lapis * t
            elif b > 0.0:
                t = b / 0.2
                arr[y, x] = mist * (1 - t) + cerulean * t
            elif b > -0.15:
                t = (b + 0.15) / 0.15
                arr[y, x] = paper_col * (1 - t) + mist * t
            else:
                arr[y, x] = paper_col
                
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    # Add celestial gold veins and mineral stardust
    gold_tex = create_gold_foil_texture(w, h, seed=909)
    gold_mask = Image.new("L", (w, h), 0)
    gdraw = ImageDraw.Draw(gold_mask)
    
    for _ in range(120):
        gx = random.randint(int(w * 0.25), int(w * 0.75))
        gy = random.randint(int(h * 0.25), int(h * 0.75))
        if bleed[gy, gx] > 0.1:
            gr = random.randint(1, 3)
            gdraw.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=random.randint(180, 255))
            
    base.paste(gold_tex, (0, 0), gold_mask)
    result = add_paper_texture(base, intensity=0.06)
    return draw_vignette(result, strength=0.18)

def render_wild_botanical_bloom(w=800, h=800):
    """4. Wild Botanical Bloom - Lush Moody Oil Floral Painting"""
    # Moody dark sage/forest canvas
    dark_sage = np.array([24, 38, 30], dtype=np.float32)
    forest = np.array([15, 24, 18], dtype=np.float32)
    n_bg = generate_noise(w, h, scale=90.0, octaves=4, seed=401)
    
    bg_arr = dark_sage[None, None, :] * n_bg[:, :, None] + forest[None, None, :] * (1 - n_bg[:, :, None])
    img = Image.fromarray(np.clip(bg_arr, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Draw deep botanical eucalyptus foliage
    for _ in range(16):
        lx = random.randint(int(w * 0.15), int(w * 0.85))
        ly = random.randint(int(h * 0.2), int(h * 0.8))
        lw = random.randint(40, 90)
        lh = random.randint(60, 130)
        angle = random.uniform(-45, 45)
        
        leaf = Image.new("RGBA", (lw * 2, lh * 2), (0, 0, 0, 0))
        ldraw = ImageDraw.Draw(leaf)
        ldraw.ellipse([lw // 2, 0, lw + lw // 2, lh * 2], fill=(60, 95, 75, 200))
        ldraw.line([(lw, 0), (lw, lh * 2)], fill=(40, 70, 52, 230), width=2)
        
        leaf_rot = leaf.rotate(angle, resample=Image.BICUBIC)
        img.paste(leaf_rot, (lx - lw, ly - lh), leaf_rot)
        
    # Paint soft peony and rose blooms
    flowers = [
        {"x": w * 0.48, "y": h * 0.48, "rad": 130, "petals": (242, 195, 205), "shadow": (195, 120, 140)},
        {"x": w * 0.32, "y": h * 0.38, "rad": 95, "petals": (250, 235, 220), "shadow": (210, 180, 160)},
        {"x": w * 0.65, "y": h * 0.58, "rad": 105, "petals": (230, 175, 185), "shadow": (180, 110, 125)},
        {"x": w * 0.38, "y": h * 0.68, "rad": 85, "petals": (252, 240, 230), "shadow": (205, 175, 155)}
    ]
    
    for fl in flowers:
        cx, cy, rad = fl["x"], fl["y"], fl["rad"]
        for layer in range(6, 0, -1):
            r = int(rad * (layer / 6.0))
            for a in range(0, 360, 45):
                rad_ang = math.radians(a + layer * 15)
                px = cx + math.cos(rad_ang) * (rad - r) * 0.4
                py = cy + math.sin(rad_ang) * (rad - r) * 0.4
                col = fl["shadow"] if layer <= 2 else fl["petals"]
                draw.ellipse([px - r, py - r, px + r, py + r], fill=col + (210,))
                
        # Golden pollen center
        for _ in range(30):
            sx = cx + random.uniform(-18, 18)
            sy = cy + random.uniform(-18, 18)
            draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(235, 185, 45, 240))
            
    result = add_canvas_texture(img, intensity=0.08)
    return draw_vignette(result, strength=0.25)

def render_oceanic_geode(w=800, h=800):
    """5. Oceanic Geode Flow - Multi-Layer Crystal Epoxy Resin Art"""
    # Luxury dark slate background
    slate = Image.new("RGB", (w, h), (18, 22, 26))
    
    # Concentric geode slices
    cx, cy = w // 2, h // 2
    y_idx, x_idx = np.indices((h, w))
    n_geo = generate_noise(w, h, scale=80.0, octaves=4, seed=501)
    
    dist = np.sqrt(((x_idx - cx) / (w * 0.45))**2 + ((y_idx - cy) / (h * 0.45))**2)
    dist_distorted = dist + (n_geo - 0.5) * 0.35
    
    teal_dark = np.array([4, 38, 48], dtype=np.float32)
    teal_med = np.array([12, 95, 108], dtype=np.float32)
    turquoise = np.array([25, 165, 175], dtype=np.float32)
    seafoam = np.array([140, 225, 215], dtype=np.float32)
    pearl = np.array([235, 248, 245], dtype=np.float32)
    bg_col = np.array([18, 22, 26], dtype=np.float32)
    
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            d = dist_distorted[y, x]
            if d > 1.05:
                arr[y, x] = bg_col
            elif d > 0.85:
                t = (d - 0.85) / 0.20
                arr[y, x] = teal_dark * (1 - t) + bg_col * t
            elif d > 0.65:
                t = (d - 0.65) / 0.20
                arr[y, x] = teal_med * (1 - t) + teal_dark * t
            elif d > 0.45:
                t = (d - 0.45) / 0.20
                arr[y, x] = turquoise * (1 - t) + teal_med * t
            elif d > 0.25:
                t = (d - 0.25) / 0.20
                arr[y, x] = seafoam * (1 - t) + turquoise * t
            elif d > 0.12:
                t = (d - 0.12) / 0.13
                arr[y, x] = pearl * (1 - t) + seafoam * t
            else:
                arr[y, x] = np.array([250, 252, 255], dtype=np.float32)
                
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(base, "RGBA")
    
    # Draw multifaceted crushed quartz crystal center
    for _ in range(45):
        qx = cx + random.uniform(-65, 65)
        qy = cy + random.uniform(-65, 65)
        rad = random.randint(8, 22)
        pts = [(qx + math.cos(math.radians(a)) * rad, qy + math.sin(math.radians(a)) * rad) for a in range(0, 360, 60)]
        alpha = random.randint(180, 255)
        draw.polygon(pts, fill=(255, 255, 255, alpha), outline=(210, 240, 245, 255))
        
    # Flowing 24K gold glitter rivers
    gold_tex = create_gold_foil_texture(w, h, seed=616)
    gold_mask = Image.new("L", (w, h), 0)
    gdraw = ImageDraw.Draw(gold_mask)
    
    for a in range(0, 360, 2):
        rad_ang = math.radians(a)
        r_dist = (0.55 + (n_geo[int(cy + math.sin(rad_ang)*200)%h, int(cx + math.cos(rad_ang)*200)%w] - 0.5) * 0.3) * (w * 0.45)
        gx = cx + math.cos(rad_ang) * r_dist
        gy = cy + math.sin(rad_ang) * r_dist
        gdraw.ellipse([gx-3, gy-3, gx+3, gy+3], fill=random.randint(180, 255))
        
    base.paste(gold_tex, (0, 0), gold_mask)
    
    # High-gloss resin glass reflection highlight
    draw.line([(w * 0.15, h * 0.2), (w * 0.85, h * 0.35)], fill=(255, 255, 255, 35), width=28)
    return draw_vignette(base, strength=0.2)

def render_emerald_nebula(w=800, h=800):
    """6. Emerald Nebula Tray - Handcrafted Luxury Serving Tray with Brass Handles"""
    # Marble tabletop background
    table = Image.new("RGB", (w, h), (242, 238, 232))
    tdraw = ImageDraw.Draw(table)
    
    # Tray drop shadow
    tx1, ty1, tx2, ty2 = int(w * 0.12), int(h * 0.18), int(w * 0.88), int(h * 0.82)
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([tx1 + 10, ty1 + 15, tx2 + 10, ty2 + 15], radius=24, fill=(0, 0, 0, 75))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16))
    table.paste(shadow, (0, 0), shadow)
    
    # Tray resin bed
    tray_w, tray_h = tx2 - tx1, ty2 - ty1
    n1 = generate_noise(tray_w, tray_h, scale=60.0, octaves=4, seed=601)
    n2 = generate_noise(tray_w, tray_h, scale=25.0, octaves=3, seed=602)
    
    em_dark = np.array([6, 42, 30], dtype=np.float32)
    em_vibrant = np.array([15, 95, 68], dtype=np.float32)
    malachite = np.array([32, 145, 105], dtype=np.float32)
    mint = np.array([165, 230, 195], dtype=np.float32)
    
    comp = n1 * 0.65 + n2 * 0.35
    t_arr = np.zeros((tray_h, tray_w, 3), dtype=np.float32)
    for y in range(tray_h):
        for x in range(tray_w):
            val = comp[y, x]
            if val < 0.35:
                t = val / 0.35
                t_arr[y, x] = em_dark * (1 - t) + em_vibrant * t
            elif val < 0.70:
                t = (val - 0.35) / 0.35
                t_arr[y, x] = em_vibrant * (1 - t) + malachite * t
            else:
                t = (val - 0.70) / 0.30
                t_arr[y, x] = malachite * (1 - t) + mint * t
                
    tray_img = Image.fromarray(np.clip(t_arr, 0, 255).astype(np.uint8))
    
    # Gold glitter rivers inside tray
    gold_t = create_gold_foil_texture(tray_w, tray_h, seed=603)
    g_mask = Image.new("L", (tray_w, tray_h), 0)
    g_draw = ImageDraw.Draw(g_mask)
    for i in range(tray_w):
        y_pos = int(tray_h * 0.5 + math.sin(i * 0.02) * 50 + (n1[int(tray_h*0.5)%tray_h, i] - 0.5) * 40)
        g_draw.ellipse([i-2, y_pos-2, i+2, y_pos+2], fill=random.randint(160, 255))
    tray_img.paste(gold_t, (0, 0), g_mask)
    
    # Mask rounded tray onto table
    mask = Image.new("L", (tray_w, tray_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, tray_w, tray_h], radius=24, fill=255)
    table.paste(tray_img, (tx1, ty1), mask)
    
    # Draw solid brushed brass handles on Left and Right
    draw = ImageDraw.Draw(table, "RGBA")
    # Tray brass rim
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=24, outline=(195, 155, 60, 255), width=4)
    
    # Left brass handle
    draw.rounded_rectangle([tx1 - 18, ty1 + tray_h // 4, tx1 - 4, ty2 - tray_h // 4], radius=6, fill=(215, 175, 65, 255), outline=(150, 110, 30, 255))
    draw.line([(tx1 - 11, ty1 + tray_h // 4 + 10), (tx1 - 11, ty2 - tray_h // 4 - 10)], fill=(255, 235, 150, 255), width=2)
    # Right brass handle
    draw.rounded_rectangle([tx2 + 4, ty1 + tray_h // 4, tx2 + 18, ty2 - tray_h // 4], radius=6, fill=(215, 175, 65, 255), outline=(150, 110, 30, 255))
    draw.line([(tx2 + 11, ty1 + tray_h // 4 + 10), (tx2 + 11, ty2 - tray_h // 4 - 10)], fill=(255, 235, 150, 255), width=2)
    
    return draw_vignette(table, strength=0.15)

def render_celestial_pearl(w=800, h=800):
    """7. Celestial Pearl Coasters - Suite of 4 Hand-Gilded Resin Coasters"""
    # Linen background
    bg = Image.new("RGB", (w, h), (246, 242, 236))
    bg = add_canvas_texture(bg, intensity=0.05)
    
    # Positions for 4 arranged hexagonal/round coasters
    coaster_configs = [
        {"cx": w * 0.36, "cy": h * 0.36, "r": 135, "seed": 701},
        {"cx": w * 0.64, "cy": h * 0.38, "r": 135, "seed": 702},
        {"cx": w * 0.35, "cy": h * 0.65, "r": 135, "seed": 703},
        {"cx": w * 0.65, "cy": h * 0.64, "r": 135, "seed": 704}
    ]
    
    for cfg in coaster_configs:
        cx, cy, rad, s = cfg["cx"], cfg["cy"], cfg["r"], cfg["seed"]
        
        # Coaster shadow
        shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.ellipse([cx - rad + 8, cy - rad + 12, cx + rad + 8, cy + rad + 12], fill=(0, 0, 0, 55))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=12))
        bg.paste(shadow, (0, 0), shadow)
        
        # Coaster resin pattern (lavender & pearl swirl)
        c_size = rad * 2
        cn = generate_noise(c_size, c_size, scale=35.0, octaves=4, seed=s)
        
        lavender = np.array([155, 130, 160], dtype=np.float32)
        smoky = np.array([195, 175, 200], dtype=np.float32)
        pearl = np.array([250, 245, 252], dtype=np.float32)
        
        c_arr = np.zeros((c_size, c_size, 3), dtype=np.float32)
        for y in range(c_size):
            for x in range(c_size):
                v = cn[y, x]
                if v < 0.4:
                    c_arr[y, x] = lavender * (1 - v/0.4) + smoky * (v/0.4)
                else:
                    t = (v - 0.4) / 0.6
                    c_arr[y, x] = smoky * (1 - t) + pearl * t
                    
        c_img = Image.fromarray(np.clip(c_arr, 0, 255).astype(np.uint8))
        
        # Round mask
        c_mask = Image.new("L", (c_size, c_size), 0)
        cm_draw = ImageDraw.Draw(c_mask)
        cm_draw.ellipse([0, 0, c_size, c_size], fill=255)
        
        bg.paste(c_img, (int(cx - rad), int(cy - rad)), c_mask)
        
        # Hand-gilded metallic gold leaf rim
        bdraw = ImageDraw.Draw(bg, "RGBA")
        bdraw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(220, 175, 55, 255), width=5)
        bdraw.ellipse([cx - rad + 1, cy - rad + 1, cx + rad - 1, cy + rad - 1], outline=(255, 235, 140, 200), width=2)
        
    return draw_vignette(bg, strength=0.15)

def render_textured_terracotta(w=800, h=800):
    """8. Textured Terracotta Arcs - Architectural 3D Plaster Relief"""
    # Create heightmap for concentric 3D plaster archways
    height = np.zeros((h, w), dtype=np.float32)
    cx, cy = w // 2, int(h * 0.75)
    
    y_idx, x_idx = np.indices((h, w))
    dist = np.sqrt((x_idx - cx)**2 + (y_idx - cy)**2)
    
    # Stepped architectural arcs
    for ring in range(7, 0, -1):
        r_inner = ring * 55
        r_outer = r_inner + 38
        in_arch = (dist >= r_inner) & (dist <= r_outer) & (y_idx <= cy)
        height[in_arch] = ring * 0.15
        
    # Vertical pillars below arches
    for ring in range(7, 0, -1):
        x_left = cx - (ring * 55 + 19)
        x_right = cx + (ring * 55 + 19)
        in_left_col = (np.abs(x_idx - x_left) <= 19) & (y_idx > cy)
        in_right_col = (np.abs(x_idx - x_right) <= 19) & (y_idx > cy)
        height[in_left_col | in_right_col] = ring * 0.15
        
    # Add plaster sand grain texture
    n_sand = generate_noise(w, h, scale=12.0, octaves=3, seed=801)
    height += (n_sand - 0.5) * 0.04
    
    # 3D Normal Lighting from Top-Left
    gx, gy = np.gradient(height)
    light_dir = np.array([-0.6, -0.7, 0.8], dtype=np.float32)
    light_dir /= np.linalg.norm(light_dir)
    
    normal = np.dstack((-gx * 6.0, -gy * 6.0, np.ones((h, w))))
    normal /= np.linalg.norm(normal, axis=2, keepdims=True)
    
    diffuse = np.clip(np.sum(normal * light_dir, axis=2), 0, 1)
    
    # Warm Terracotta Clay Palette
    terracotta = np.array([198, 112, 78], dtype=np.float32)
    sand = np.array([232, 195, 165], dtype=np.float32)
    shadow = np.array([115, 55, 38], dtype=np.float32)
    
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            d = diffuse[y, x]
            if d > 0.5:
                t = (d - 0.5) * 2
                arr[y, x] = terracotta * (1 - t) + sand * t
            else:
                t = d * 2
                arr[y, x] = shadow * (1 - t) + terracotta * t
                
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    result = add_canvas_texture(img, intensity=0.05)
    return draw_vignette(result, strength=0.2)

def render_monochrome_rhythm(w=800, h=800):
    """9. Monochrome Rhythm - Minimalist Wood Slat & Ash Wall Art"""
    # Raw natural off-white linen background
    bg = Image.new("RGB", (w, h), (238, 234, 226))
    bg = add_canvas_texture(bg, intensity=0.08)
    
    # Slat geometry definitions (Ash Black and Honey Oak)
    slats = [
        # (x1, y1, x2, y2, is_black)
        (w * 0.18, h * 0.15, w * 0.24, h * 0.85, True),
        (w * 0.28, h * 0.25, w * 0.34, h * 0.75, False),
        (w * 0.38, h * 0.10, w * 0.44, h * 0.90, True),
        (w * 0.48, h * 0.30, w * 0.54, h * 0.70, False),
        (w * 0.58, h * 0.15, w * 0.64, h * 0.85, True),
        (w * 0.68, h * 0.22, w * 0.74, h * 0.78, False),
        (w * 0.78, h * 0.12, w * 0.84, h * 0.88, True)
    ]
    
    # Cast shadows beneath slats
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    for x1, y1, x2, y2, _ in slats:
        sdraw.rectangle([x1 + 10, y1 + 12, x2 + 10, y2 + 12], fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    bg.paste(shadow, (0, 0), shadow)
    
    # Draw slats with wood grain
    draw = ImageDraw.Draw(bg)
    for x1, y1, x2, y2, is_black in slats:
        col = (28, 26, 28) if is_black else (186, 130, 72)
        draw.rectangle([x1, y1, x2, y2], fill=col)
        # Slat highlight on left edge
        hl_col = (55, 52, 58) if is_black else (225, 175, 115)
        draw.line([(x1 + 1, y1), (x1 + 1, y2)], fill=hl_col, width=2)
        
    return draw_vignette(bg, strength=0.22)

def render_gilded_botanical(w=800, h=800):
    """10. Gilded Botanical Relief - Hand-Carved Bas-Relief with Gold Patina"""
    # Warm ivory stone shadowbox
    stone = Image.new("RGB", (w, h), (242, 237, 226))
    
    # Sculpted bas-relief leaves heightmap
    hmap = np.zeros((h, w), dtype=np.float32)
    cx, cy = w // 2, h // 2
    
    for i in range(-5, 6):
        angle = math.radians(i * 14 - 90)
        for d in range(40, 280, 4):
            x = int(cx + math.cos(angle) * d + math.sin(d * 0.05) * 15)
            y = int(cy + math.sin(angle) * d)
            if 0 <= x < w and 0 <= y < h:
                rad = max(1, int(18 - d * 0.04))
                y0, y1 = max(0, y-rad), min(h, y+rad)
                x0, x1 = max(0, x-rad), min(w, x+rad)
                hmap[y0:y1, x0:x1] = np.maximum(hmap[y0:y1, x0:x1], 0.6 * (1 - d/300.0))
                
    # 3D Normal Lighting
    gx, gy = np.gradient(hmap)
    normal = np.dstack((-gx * 4.0, -gy * 4.0, np.ones((h, w))))
    normal /= np.linalg.norm(normal, axis=2, keepdims=True)
    light = np.array([-0.5, -0.6, 0.7], dtype=np.float32)
    light /= np.linalg.norm(light)
    diff = np.clip(np.sum(normal * light, axis=2), 0, 1)
    
    ivory = np.array([245, 240, 230], dtype=np.float32)
    stone_shadow = np.array([175, 165, 150], dtype=np.float32)
    
    arr = stone_shadow[None, None, :] * (1 - diff[:, :, None]) + ivory[None, None, :] * diff[:, :, None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    # Hand-applied antique gold patina on leaf veins
    gold_tex = create_gold_foil_texture(w, h, seed=911)
    g_mask = Image.new("L", (w, h), 0)
    g_draw = ImageDraw.Draw(g_mask)
    
    for i in range(-5, 6):
        angle = math.radians(i * 14 - 90)
        for d in range(60, 260, 8):
            x = int(cx + math.cos(angle) * d + math.sin(d * 0.05) * 15)
            y = int(cy + math.sin(angle) * d)
            if random.random() > 0.4:
                g_draw.ellipse([x-3, y-3, x+3, y+3], fill=random.randint(180, 255))
                
    img.paste(gold_tex, (0, 0), g_mask)
    return draw_vignette(img, strength=0.25)

def render_sculpted_clay_vase(w=800, h=800):
    """11. Sculpted Clay Muse Vase - Wheel-Thrown Studio Ceramic Vessel"""
    # Studio lighting backdrop
    bg = np.zeros((h, w, 3), dtype=np.float32)
    top_col = np.array([245, 240, 235], dtype=np.float32)
    bot_col = np.array([215, 205, 195], dtype=np.float32)
    for y in range(h):
        t = y / h
        bg[y, :] = top_col * (1 - t) + bot_col * t
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    
    # Cast ground pedestal shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([w * 0.28, h * 0.76, w * 0.72, h * 0.86], fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16))
    img.paste(shadow, (0, 0), shadow)
    
    # 3D Shaded Ceramic Amphora Vase Silhouette
    vase_h = int(h * 0.58)
    vase_w = int(w * 0.44)
    vx, vy = int(w * 0.28), int(h * 0.22)
    
    v_arr = np.zeros((vase_h, vase_w, 3), dtype=np.float32)
    terracotta = np.array([205, 125, 92], dtype=np.float32)
    sand_hl = np.array([245, 195, 168], dtype=np.float32)
    clay_sh = np.array([125, 65, 45], dtype=np.float32)
    
    for y in range(vase_h):
        t_y = y / vase_h
        # Amphora profile curve
        if t_y < 0.15:  # Lip & Neck
            radius = 0.28 + math.sin(t_y * math.pi / 0.15) * 0.05
        elif t_y < 0.75: # Wide body
            radius = 0.28 + math.sin((t_y - 0.15) * math.pi / 0.60) * 0.65
        else: # Tapered base
            radius = 0.55 - (t_y - 0.75) * 0.95
            
        r_px = int(vase_w * radius / 2)
        cx_v = vase_w // 2
        for x in range(max(0, cx_v - r_px), min(vase_w, cx_v + r_px)):
            t_x = (x - (cx_v - r_px)) / (2 * r_px)
            # Spherical 3D shading
            normal_x = (t_x - 0.5) * 2
            diff = max(0, -normal_x * 0.7 + math.sqrt(max(0, 1 - normal_x**2)) * 0.7)
            if diff > 0.5:
                v_arr[y, x] = terracotta * (1 - (diff-0.5)*2) + sand_hl * ((diff-0.5)*2)
            else:
                v_arr[y, x] = clay_sh * (1 - diff*2) + terracotta * (diff*2)
                
    v_img = Image.fromarray(np.clip(v_arr, 0, 255).astype(np.uint8))
    v_mask = Image.new("L", (vase_w, vase_h), 0)
    v_mask_arr = np.any(v_arr > 0, axis=2).astype(np.uint8) * 255
    v_mask = Image.fromarray(v_mask_arr)
    
    img.paste(v_img, (vx, vy), v_mask)
    
    # Sculpted handles on Left and Right
    draw = ImageDraw.Draw(img, "RGBA")
    draw.arc([vx - 28, vy + int(vase_h * 0.2), vx + 22, vy + int(vase_h * 0.55)], start=90, end=270, fill=(185, 105, 75, 255), width=10)
    draw.arc([vx + vase_w - 22, vy + int(vase_h * 0.2), vx + vase_w + 28, vy + int(vase_h * 0.55)], start=270, end=90, fill=(185, 105, 75, 255), width=10)
    
    result = add_canvas_texture(img, intensity=0.04)
    return draw_vignette(result, strength=0.18)

def render_artisan_ceramic_vessel(w=800, h=800):
    """12. Artisan Ceramic Vessel - Charcoal Studio Stoneware"""
    # Warm taupe spotlight background
    bg = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            d = math.sqrt(((x - w*0.5)/(w*0.5))**2 + ((y - h*0.5)/(h*0.5))**2)
            bg[y, x] = np.array([238, 232, 224]) * (1 - d*0.35)
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    
    # Pedestal shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([w * 0.30, h * 0.74, w * 0.70, h * 0.84], fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    img.paste(shadow, (0, 0), shadow)
    
    # Asymmetrical Charcoal Wabi-Sabi Silhouette
    vh, vw = int(h * 0.52), int(w * 0.42)
    vx, vy = int(w * 0.29), int(h * 0.26)
    v_arr = np.zeros((vh, vw, 3), dtype=np.float32)
    
    charcoal = np.array([45, 42, 46], dtype=np.float32)
    charcoal_hl = np.array([95, 90, 98], dtype=np.float32)
    deep_black = np.array([22, 20, 24], dtype=np.float32)
    
    for y in range(vh):
        t_y = y / vh
        # Fluted asymmetrical organic curve
        r_factor = 0.35 + math.sin(t_y * math.pi * 0.9) * 0.55 + math.sin(y * 0.08) * 0.02
        r_px = int(vw * r_factor / 2)
        cx_v = vw // 2
        for x in range(max(0, cx_v - r_px), min(vw, cx_v + r_px)):
            t_x = (x - (cx_v - r_px)) / (2 * r_px)
            diff = max(0, -(t_x - 0.5)*2 * 0.6 + 0.6)
            if diff > 0.5:
                v_arr[y, x] = charcoal * (1 - (diff-0.5)*2) + charcoal_hl * ((diff-0.5)*2)
            else:
                v_arr[y, x] = deep_black * (1 - diff*2) + charcoal * (diff*2)
                
    # Add speckled glaze dots
    speckle = np.random.rand(vh, vw)
    v_arr = np.where((speckle > 0.985)[:, :, None] & (v_arr > 0), v_arr + 65, v_arr)
    
    v_img = Image.fromarray(np.clip(v_arr, 0, 255).astype(np.uint8))
    v_mask = Image.fromarray((np.any(v_arr > 0, axis=2).astype(np.uint8) * 255))
    img.paste(v_img, (vx, vy), v_mask)
    
    return draw_vignette(img, strength=0.2)

def render_woven_tapestry_dune(w=800, h=800):
    """13. Handwoven Dune Tapestry - Fiber Art Wall Hanging"""
    # Wall background
    bg = Image.new("RGB", (w, h), (244, 240, 234))
    draw = ImageDraw.Draw(bg, "RGBA")
    
    # Hanging Brass Rod & Cord
    draw.line([(w * 0.5, h * 0.08), (w * 0.2, h * 0.18)], fill=(185, 145, 60, 255), width=3)
    draw.line([(w * 0.5, h * 0.08), (w * 0.8, h * 0.18)], fill=(185, 145, 60, 255), width=3)
    draw.rounded_rectangle([w * 0.15, h * 0.17, w * 0.85, h * 0.20], radius=5, fill=(215, 175, 65, 255), outline=(150, 110, 30, 255))
    
    # Tapestry woven rows
    tx1, ty1, tx2, ty2 = int(w * 0.24), int(h * 0.20), int(w * 0.76), int(h * 0.72)
    
    dune_colors = [
        (245, 240, 230), # Cream merino
        (215, 168, 120), # Warm dune ochre
        (185, 110, 80),  # Terracotta wool
        (48, 44, 46),    # Charcoal accent
        (245, 240, 230)  # Cream
    ]
    
    row_h = (ty2 - ty1) // len(dune_colors)
    for i, col in enumerate(dune_colors):
        ry1 = ty1 + i * row_h
        ry2 = ry1 + row_h
        draw.rectangle([tx1, ry1, tx2, ry2], fill=col)
        # Weave stitch texture
        for x_pos in range(tx1, tx2, 6):
            draw.line([(x_pos, ry1), (x_pos, ry2)], fill=(0, 0, 0, 25), width=1)
            
    # Fringe tassels at base
    for fx in range(tx1, tx2, 8):
        f_len = random.randint(55, 95)
        draw.line([(fx, ty2), (fx + random.randint(-4, 4), ty2 + f_len)], fill=(235, 228, 218, 240), width=3)
        
    result = add_canvas_texture(bg, intensity=0.08)
    return draw_vignette(result, strength=0.18)

def render_sunlit_olive_grove(w=800, h=800):
    """14. Sunlit Olive Grove - Archival Fine Art Giclée Print"""
    # Landscape giclée artwork
    img = Image.new("RGB", (w, h), (252, 250, 246))
    
    # Sky and rolling hills
    sky = np.zeros((h, w, 3), dtype=np.float32)
    sky_top = np.array([175, 210, 235], dtype=np.float32)
    sky_gold = np.array([255, 238, 185], dtype=np.float32)
    hills_col = np.array([165, 175, 120], dtype=np.float32)
    earth_col = np.array([195, 145, 85], dtype=np.float32)
    
    for y in range(h):
        t = y / h
        if t < 0.5:
            sky[y, :] = sky_top * (1 - t*2) + sky_gold * (t*2)
        else:
            sky[y, :] = hills_col * (1 - (t-0.5)*2) + earth_col * ((t-0.5)*2)
            
    art = Image.fromarray(np.clip(sky, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(art, "RGBA")
    
    # Silvery-green olive tree canopy & gnarly branches
    # Sun rays flare
    draw.ellipse([w * 0.65 - 80, h * 0.35 - 80, w * 0.65 + 80, h * 0.35 + 80], fill=(255, 250, 220, 140))
    
    for _ in range(8):
        tx = random.randint(int(w * 0.2), int(w * 0.8))
        ty = random.randint(int(h * 0.45), int(h * 0.75))
        # Trunk
        draw.line([(tx, ty + 120), (tx, ty)], fill=(75, 55, 42, 255), width=14)
        # Foliage clouds
        for _ in range(12):
            fx = tx + random.randint(-65, 65)
            fy = ty + random.randint(-55, 15)
            draw.ellipse([fx-35, fy-25, fx+35, fy+25], fill=(135, 160, 125, 190))
            
    # White archival museum mat border
    border_w = int(w * 0.08)
    draw.rectangle([0, 0, w, border_w], fill=(252, 250, 246, 255))
    draw.rectangle([0, h - border_w, w, h], fill=(252, 250, 246, 255))
    draw.rectangle([0, 0, border_w, h], fill=(252, 250, 246, 255))
    draw.rectangle([w - border_w, 0, w, h], fill=(252, 250, 246, 255))
    
    # Embossed atelier seal stamp
    draw.ellipse([w - border_w - 45, h - border_w - 45, w - border_w - 15, h - border_w - 15], outline=(195, 175, 140, 200), width=2)
    
    return add_paper_texture(art, intensity=0.05)

def render_abstract_fluidity(w=800, h=800):
    """15. Abstract Fluidity No. 4 - Fine Art Lithograph on Textured Velvet Paper"""
    paper = Image.new("RGB", (w, h), (248, 245, 238))
    draw = ImageDraw.Draw(paper, "RGBA")
    
    # Modernist organic shapes in mauve, terracotta, ochre & sage
    shapes = [
        {"pts": [w*0.25, h*0.2, w*0.65, h*0.22, w*0.55, h*0.65, w*0.2, h*0.5], "col": (168, 115, 138, 220)},
        {"pts": [w*0.45, h*0.35, w*0.82, h*0.4, w*0.75, h*0.82, w*0.38, h*0.75], "col": (212, 125, 88, 210)},
        {"pts": [w*0.18, h*0.45, w*0.48, h*0.48, w*0.42, h*0.85, w*0.15, h*0.78], "col": (125, 145, 120, 200)},
        {"pts": [w*0.35, h*0.15, w*0.55, h*0.18, w*0.5, h*0.42, w*0.32, h*0.38], "col": (225, 175, 65, 230)}
    ]
    
    for sh in shapes:
        draw.polygon(sh["pts"], fill=sh["col"])
        
    # Black line accent
    draw.arc([w * 0.2, h * 0.25, w * 0.8, h * 0.75], start=45, end=225, fill=(35, 32, 36, 255), width=4)
    
    # Pencil signature & edition stamp
    # Simulated typography mark
    draw.line([(w * 0.15, h * 0.9), (w * 0.28, h * 0.9)], fill=(120, 115, 110, 255), width=1)
    draw.line([(w * 0.72, h * 0.9), (w * 0.85, h * 0.9)], fill=(120, 115, 110, 255), width=1)
    
    return add_paper_texture(paper, intensity=0.06)

def render_midnight_flora(w=800, h=800):
    """16. Midnight Flora Lithograph - Metallic Embossed Botanical Print"""
    # Velvet midnight navy background
    navy = Image.new("RGB", (w, h), (12, 18, 34))
    draw = ImageDraw.Draw(navy, "RGBA")
    
    # Metallic Silver & Gold Botanical Silhouettes
    for i in range(14):
        bx = int(w * 0.5 + math.sin(i * 0.5) * 180)
        by = int(h * 0.15 + i * 45)
        blen = random.randint(60, 130)
        angle = math.radians(random.uniform(-40, 40) + (180 if i % 2 == 0 else 0))
        
        ex = bx + math.cos(angle) * blen
        ey = by + math.sin(angle) * blen
        col = (235, 238, 245, 220) if i % 3 != 0 else (235, 185, 65, 240)
        draw.line([(bx, by), (ex, ey)], fill=col, width=3)
        
        # Leaflets
        for step in range(5):
            lx = bx + (ex - bx) * (step / 5.0)
            ly = by + (ey - by) * (step / 5.0)
            draw.ellipse([lx - 12, ly - 6, lx + 12, ly + 6], fill=col)
            
    return add_paper_texture(navy, intensity=0.04)

def render_custom_watercolor_gift(w=800, h=800):
    """17. Bespoke Couple Watercolor - Customized Romantic Portrait Gift"""
    paper = Image.new("RGB", (w, h), (250, 247, 242))
    
    # Sunset watercolor wash
    n_w = generate_noise(w, h, scale=90.0, octaves=4, seed=771)
    peach = np.array([255, 215, 185], dtype=np.float32)
    lavender = np.array([205, 185, 215], dtype=np.float32)
    ocean = np.array([125, 175, 205], dtype=np.float32)
    
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        t = y / h
        if t < 0.45:
            arr[y, :] = peach * (1 - t/0.45) + lavender * (t/0.45)
        else:
            arr[y, :] = lavender * (1 - (t-0.45)/0.55) + ocean * ((t-0.45)/0.55)
            
    arr += (n_w[:, :, None] - 0.5) * 35
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Coastal cliff silhouette
    draw.polygon([(0, h), (0, h * 0.65), (w * 0.45, h * 0.62), (w * 0.65, h * 0.78), (w, h * 0.72), (w, h)], fill=(45, 38, 48, 255))
    
    # Romantic Couple Silhouette
    cx, cy = w * 0.38, h * 0.56
    # Person 1
    draw.ellipse([cx - 15, cy - 45, cx + 5, cy - 25], fill=(32, 26, 35, 255))
    draw.polygon([(cx - 18, cy - 25), (cx + 8, cy - 25), (cx + 12, cy + 20), (cx - 22, cy + 20)], fill=(32, 26, 35, 255))
    # Person 2
    draw.ellipse([cx + 2, cy - 42, cx + 22, cy - 22], fill=(32, 26, 35, 255))
    draw.polygon([(cx, cy - 22), (cx + 25, cy - 22), (cx + 32, cy + 20), (cx - 5, cy + 20)], fill=(32, 26, 35, 255))
    
    # Gold Calligraphy Inscription Line
    draw.line([(w * 0.25, h * 0.88), (w * 0.75, h * 0.88)], fill=(215, 168, 55, 220), width=2)
    return add_paper_texture(img, intensity=0.05)

def render_custom_resin_plaque(w=800, h=800):
    """18. Personalized Resin Plaque - Botanical Pressed Floral Resin Gift"""
    # Natural wood tabletop background
    table = Image.new("RGB", (w, h), (235, 222, 205))
    
    # Easel & Plaque shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rectangle([w * 0.22, h * 0.22, w * 0.82, h * 0.82], fill=(0, 0, 0, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    table.paste(shadow, (0, 0), shadow)
    
    # Crystal clear resin plaque with pressed botanicals
    pw1, ph1, pw2, ph2 = int(w * 0.20), int(h * 0.18), int(w * 0.80), int(h * 0.78)
    draw = ImageDraw.Draw(table, "RGBA")
    
    # Resin glass surface
    draw.rounded_rectangle([pw1, ph1, pw2, ph2], radius=16, fill=(255, 255, 255, 225), outline=(220, 225, 230, 255), width=3)
    
    # Embedded pressed hydrangeas & fern fronds
    for _ in range(24):
        bx = random.randint(pw1 + 25, pw2 - 25)
        by = random.randint(ph1 + 25, ph2 - 25)
        brad = random.randint(12, 28)
        col = random.choice([
            (145, 175, 215, 190), # Blue hydrangea
            (235, 185, 195, 190), # Pink petal
            (120, 165, 125, 200), # Fern green
            (240, 235, 225, 210)  # Baby's breath
        ])
        draw.ellipse([bx-brad, by-brad, bx+brad, by+brad], fill=col)
        
    # Gold leaf flakes inside plaque
    for _ in range(35):
        gx = random.randint(pw1 + 20, pw2 - 20)
        gy = random.randint(ph1 + 20, ph2 - 20)
        draw.ellipse([gx-3, gy-3, gx+3, gy+3], fill=(235, 185, 45, 255))
        
    # Gilded personalized inscription & frame line
    draw.rounded_rectangle([pw1 + 35, ph1 + 35, pw2 - 35, ph2 - 35], radius=8, outline=(215, 168, 55, 230), width=2)
    draw.line([(w * 0.35, h * 0.48), (w * 0.65, h * 0.48)], fill=(215, 168, 55, 255), width=3)
    
    # Wooden display easel legs
    draw.polygon([(w * 0.15, h * 0.82), (w * 0.22, ph1), (w * 0.26, ph1), (w * 0.19, h * 0.82)], fill=(185, 130, 75, 255))
    draw.polygon([(w * 0.85, h * 0.82), (w * 0.78, ph1), (w * 0.74, ph1), (w * 0.81, h * 0.82)], fill=(185, 130, 75, 255))
    
    return draw_vignette(table, strength=0.18)

def render_hero_art(w=1200, h=800):
    """19. Hero Masterpiece - Grand Panoramic Atelier Showcase Artwork"""
    # Luxurious wide panoramic canvas
    n1 = generate_noise(w, h, scale=220.0, octaves=5, seed=1001)
    n2 = generate_noise(w, h, scale=90.0, octaves=4, seed=1002)
    
    ocean_teal = np.array([8, 48, 58], dtype=np.float32)
    midnight_plum = np.array([45, 25, 48], dtype=np.float32)
    warm_blush = np.array([238, 198, 185], dtype=np.float32)
    gold_ochre = np.array([215, 155, 55], dtype=np.float32)
    cream = np.array([252, 248, 242], dtype=np.float32)
    
    comp = n1 * 0.6 + n2 * 0.4
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            v = comp[y, x]
            if v < 0.3:
                arr[y, x] = ocean_teal * (1 - v/0.3) + midnight_plum * (v/0.3)
            elif v < 0.6:
                arr[y, x] = midnight_plum * (1 - (v-0.3)/0.3) + warm_blush * ((v-0.3)/0.3)
            elif v < 0.8:
                arr[y, x] = warm_blush * (1 - (v-0.6)/0.2) + gold_ochre * ((v-0.6)/0.2)
            else:
                arr[y, x] = gold_ochre * (1 - (v-0.8)/0.2) + cream * ((v-0.8)/0.2)
                
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    # Flowing 24K Gold River through panorama
    gold_tex = create_gold_foil_texture(w, h, seed=1003)
    g_mask = Image.new("L", (w, h), 0)
    g_draw = ImageDraw.Draw(g_mask)
    
    for x_pos in range(0, w, 6):
        y_pos = int(h * 0.6 + math.sin(x_pos * 0.008) * 120 + (n1[int(h*0.5)%h, x_pos] - 0.5) * 80)
        g_draw.ellipse([x_pos-8, y_pos-8, x_pos+8, y_pos+8], fill=random.randint(180, 255))
        
    base.paste(gold_tex, (0, 0), g_mask)
    result = add_canvas_texture(base, intensity=0.08)
    return draw_vignette(result, strength=0.25)

def render_about_artist(w=800, h=900):
    """20. About Artist - Elena Moreau in Sunlit Atelier Loft"""
    # Sunlit loft studio interior with artist easel and pottery
    loft = Image.new("RGB", (w, h), (245, 238, 228))
    draw = ImageDraw.Draw(loft, "RGBA")
    
    # Large loft window light beams
    draw.polygon([(0, 0), (w * 0.7, 0), (w, h), (0, h)], fill=(255, 252, 245, 120))
    
    # Studio easel and large canvas
    draw.rectangle([w * 0.15, h * 0.2, w * 0.58, h * 0.75], fill=(238, 228, 218), outline=(165, 125, 75), width=6)
    # Paint strokes on canvas
    draw.arc([w * 0.2, h * 0.25, w * 0.52, h * 0.65], start=30, end=210, fill=(185, 110, 85, 240), width=18)
    draw.arc([w * 0.25, h * 0.35, w * 0.55, h * 0.7], start=120, end=300, fill=(215, 165, 55, 240), width=12)
    
    # Artist Silhouette in front of canvas
    cx, cy = w * 0.68, h * 0.58
    # Head & hair
    draw.ellipse([cx - 28, cy - 140, cx + 28, cy - 80], fill=(42, 35, 32, 255))
    # Torso & linen apron
    draw.polygon([(cx - 45, cy - 80), (cx + 45, cy - 80), (cx + 65, cy + 180), (cx - 65, cy + 180)], fill=(225, 218, 208, 255))
    draw.polygon([(cx - 30, cy - 65), (cx + 30, cy - 65), (cx + 40, cy + 120), (cx - 40, cy + 120)], fill=(125, 95, 75, 255))
    
    # Shelves with studio ceramic vessels on left
    draw.rectangle([w * 0.05, h * 0.15, w * 0.14, h * 0.85], fill=(165, 135, 105, 255))
    for sy in range(int(h * 0.25), int(h * 0.8), 120):
        draw.ellipse([w * 0.06, sy - 30, w * 0.13, sy], fill=(195, 125, 85, 255))
        
    return draw_vignette(loft, strength=0.22)

def render_studio_process(w=1000, h=650):
    """21. Studio Process - Artisanal Pigment Mixing & Workbench Flat-Lay"""
    # Rustic oak workbench table
    bench = Image.new("RGB", (w, h), (185, 145, 105))
    bdraw = ImageDraw.Draw(bench, "RGBA")
    
    # Wood grain planks
    for x in range(0, w, 180):
        bdraw.line([(x, 0), (x, h)], fill=(145, 105, 70, 255), width=2)
        
    # Ceramic pigment bowls (Lapis, Terracotta, Ochre, Sage)
    bowls = [
        {"x": w * 0.22, "y": h * 0.35, "r": 65, "pigment": (15, 45, 95)},   # Lapis
        {"x": w * 0.42, "y": h * 0.28, "r": 55, "pigment": (195, 85, 45)},  # Terracotta
        {"x": w * 0.28, "y": h * 0.68, "r": 60, "pigment": (225, 175, 45)}, # Ochre
        {"x": w * 0.48, "y": h * 0.65, "r": 50, "pigment": (75, 115, 85)}   # Sage
    ]
    
    for b in bowls:
        bx, by, br = b["x"], b["y"], b["r"]
        # Ceramic rim
        bdraw.ellipse([bx - br, by - br, bx + br, by + br], fill=(245, 240, 232, 255), outline=(210, 205, 195, 255), width=5)
        # Raw powdered pigment
        bdraw.ellipse([bx - br + 8, by - br + 8, bx + br - 8, by + br - 8], fill=b["pigment"] + (255,))
        
    # Gold leaf foil sheets on right
    gold_tex = create_gold_foil_texture(240, 240, seed=1212)
    bench.paste(gold_tex, (int(w * 0.68), int(h * 0.22)))
    bdraw.rectangle([w * 0.68, h * 0.22, w * 0.68 + 240, h * 0.22 + 240], outline=(180, 135, 45, 255), width=3)
    
    # Palette knives
    bdraw.polygon([(w * 0.60, h * 0.70), (w * 0.65, h * 0.62), (w * 0.72, h * 0.78), (w * 0.67, h * 0.85)], fill=(225, 228, 232, 255))
    bdraw.line([(w * 0.60, h * 0.70), (w * 0.52, h * 0.82)], fill=(125, 75, 45, 255), width=10)
    
    return draw_vignette(bench, strength=0.2)

def render_testimonial_1(w=400, h=400):
    """22. Testimonial 1 - Elena Rostova, Art Collector"""
    img = Image.new("RGB", (w, h), (235, 228, 220))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse([w*0.1, h*0.1, w*0.9, h*0.9], fill=(248, 242, 235, 255))
    # Elegant portrait silhouette
    cx, cy = w // 2, int(h * 0.45)
    draw.ellipse([cx - 55, cy - 75, cx + 55, cy + 45], fill=(75, 62, 70, 255))
    draw.ellipse([cx - 45, cy - 65, cx + 45, cy + 30], fill=(238, 205, 192, 255))
    draw.polygon([(cx - 85, h), (cx - 45, cy + 50), (cx + 45, cy + 50), (cx + 85, h)], fill=(142, 114, 138, 255))
    return draw_vignette(img, strength=0.15)

def render_testimonial_2(w=400, h=400):
    """23. Testimonial 2 - Marcus Vance, Principal Designer"""
    img = Image.new("RGB", (w, h), (225, 230, 226))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse([w*0.1, h*0.1, w*0.9, h*0.9], fill=(242, 246, 244, 255))
    cx, cy = w // 2, int(h * 0.45)
    draw.ellipse([cx - 50, cy - 70, cx + 50, cy + 40], fill=(48, 55, 50, 255))
    draw.ellipse([cx - 42, cy - 60, cx + 42, cy + 28], fill=(232, 202, 185, 255))
    draw.polygon([(cx - 85, h), (cx - 45, cy + 50), (cx + 45, cy + 50), (cx + 85, h)], fill=(45, 62, 54, 255))
    return draw_vignette(img, strength=0.15)

def render_testimonial_3(w=400, h=400):
    """24. Testimonial 3 - Aria Tanaka, Curator"""
    img = Image.new("RGB", (w, h), (232, 226, 235))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.ellipse([w*0.1, h*0.1, w*0.9, h*0.9], fill=(246, 242, 248, 255))
    cx, cy = w // 2, int(h * 0.45)
    draw.ellipse([cx - 52, cy - 72, cx + 52, cy + 42], fill=(38, 32, 42, 255))
    draw.ellipse([cx - 42, cy - 62, cx + 42, cy + 28], fill=(242, 212, 198, 255))
    draw.polygon([(cx - 85, h), (cx - 45, cy + 50), (cx + 45, cy + 50), (cx + 85, h)], fill=(115, 88, 110, 255))
    return draw_vignette(img, strength=0.15)

# -----------------------------------------------------------------------------
# 3. BATCH GENERATION CONTROLLER
# -----------------------------------------------------------------------------

GENERATORS = [
    ("ethereal-whispers.jpg", render_ethereal_whispers),
    ("golden-horizon.jpg", render_golden_horizon),
    ("serenade-indigo.jpg", render_serenade_indigo),
    ("wild-botanical-bloom.jpg", render_wild_botanical_bloom),
    ("oceanic-geode.jpg", render_oceanic_geode),
    ("emerald-nebula.jpg", render_emerald_nebula),
    ("celestial-pearl.jpg", render_celestial_pearl),
    ("textured-terracotta.jpg", render_textured_terracotta),
    ("monochrome-rhythm.jpg", render_monochrome_rhythm),
    ("gilded-botanical.jpg", render_gilded_botanical),
    ("sculpted-clay-vase.jpg", render_sculpted_clay_vase),
    ("artisan-ceramic-vessel.jpg", render_artisan_ceramic_vessel),
    ("woven-tapestry-dune.jpg", render_woven_tapestry_dune),
    ("sunlit-olive-grove.jpg", render_sunlit_olive_grove),
    ("abstract-fluidity.jpg", render_abstract_fluidity),
    ("midnight-flora.jpg", render_midnight_flora),
    ("custom-watercolor-gift.jpg", render_custom_watercolor_gift),
    ("custom-resin-plaque.jpg", render_custom_resin_plaque),
    ("hero-art.jpg", render_hero_art),
    ("about-artist.jpg", render_about_artist),
    ("studio-process.jpg", render_studio_process),
    ("testimonial-1.jpg", render_testimonial_1),
    ("testimonial-2.jpg", render_testimonial_2),
    ("testimonial-3.jpg", render_testimonial_3)
]

def generate_all():
    print("==================================================")
    print("[*] CHROMANEST Procedural Art Asset Generation")
    print(f"[*] Target Output: {OUTPUT_DIR}")
    print("==================================================")
    
    for filename, generator_func in GENERATORS:
        target_path = os.path.join(OUTPUT_DIR, filename)
        print(f"Generating {filename}...", end=" ", flush=True)
        img = generator_func()
        img.save(target_path, "JPEG", quality=95)
        size_kb = os.path.getsize(target_path) / 1024.0
        print(f"DONE ({img.size[0]}x{img.size[1]}, {size_kb:.1f} KB)")
        
    print("==================================================")
    print(f"Successfully generated all {len(GENERATORS)} artwork assets!")
    print("==================================================")

if __name__ == "__main__":
    generate_all()

