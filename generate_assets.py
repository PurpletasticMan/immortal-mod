"""Generates everything that is not hand-written Java: fabric.mod.json, the client entrypoint,
and all textures, models, recipes, tags and language files.
Run from the repo root:  python3 generate_assets.py   (needs: pip install pillow)
The GitHub workflow runs this before every build."""
import json, os, random
from PIL import Image, ImageDraw

_EXTRA = {
    "src/main/resources/fabric.mod.json": '{\n\t"schemaVersion": 1,\n\t"id": "immortal",\n\t"version": "${version}",\n\t"name": "Immortal & Godly",\n\t"description": "Golden food, a bedrock pickaxe, unbreakable Immortal and Godly gear, hearts, flight armour, enchantable sword blocks and purple superhero armour.",\n\t"authors": ["You"],\n\t"license": "CC0-1.0",\n\t"icon": "assets/immortal/icon.png",\n\t"environment": "*",\n\t"entrypoints": {\n\t\t"main": ["com.immortalmod.ImmortalMod"],\n\t\t"client": ["com.immortalmod.client.ImmortalModClient"]\n\t},\n\t"depends": {\n\t\t"fabricloader": ">=0.20.1",\n\t\t"minecraft": "~26.3",\n\t\t"java": ">=25",\n\t\t"fabric-api": "*"\n\t}\n}\n',
    "src/client/java/com/immortalmod/client/ImmortalModClient.java": 'package com.immortalmod.client;\n\nimport net.fabricmc.api.ClientModInitializer;\n\npublic class ImmortalModClient implements ClientModInitializer {\n\t@Override\n\tpublic void onInitializeClient() {\n\t\t// Nothing needed on the client: models, textures and names are all resource-pack driven.\n\t}\n}\n',
}
for _p, _t in _EXTRA.items():
    os.makedirs(os.path.dirname(_p), exist_ok=True)
    with open(_p, "w") as _f:
        _f.write(_t)

ROOT = os.path.join(os.getcwd(), "src", "main", "resources")
A = f"{ROOT}/assets/immortal"
D = f"{ROOT}/data"
NS = "immortal"

def w(path, data, raw=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(data if raw else json.dumps(data, indent=2))

# ------------------------------------------------------------ palettes
PAL = {
    "iron":      dict(main=(205,205,210), dark=(120,120,128), light=(240,240,245)),
    "diamond":   dict(main=(70,225,215),  dark=(20,130,150),  light=(190,255,250)),
    "netherite": dict(main=(78,70,82),    dark=(35,30,40),    light=(130,120,138)),
    "bedrock":   dict(main=(95,95,95),    dark=(30,30,30),    light=(160,160,160)),
    "galaxy":    dict(main=(60,70,190),   dark=(14,12,60),    light=(140,175,255)),
    "immortal":  dict(main=(150,60,225),  dark=(45,10,95),    light=(235,170,255)),
    "godly":     dict(main=(246,247,255), dark=(165,185,225), light=(255,255,255)),
    "purple":    dict(main=(150,70,200),  dark=(80,30,120),   light=(215,170,245)),
    "gold":      dict(main=(250,200,50),  dark=(185,120,20),  light=(255,245,160)),
}
OUT = (20, 14, 24)
WOOD = (130, 90, 45)
WOOD_D = (85, 55, 25)

def canvas():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def outline(img):
    px = img.load()
    out = img.copy()
    po = out.load()
    for y in range(16):
        for x in range(16):
            if px[x, y][3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < 16 and 0 <= ny < 16 and px[nx, ny][3] > 0:
                        po[x, y] = OUT + (255,)
                        break
    return out

def line(img, pts, color):
    ImageDraw.Draw(img).line(pts, fill=color + (255,))

def px(img, pts, color):
    p = img.load()
    for x, y in pts:
        if 0 <= x < 16 and 0 <= y < 16:
            p[x, y] = color + (255,)

# ------------------------------------------------------------ item icons
def sword(c):
    im = canvas()
    line(im, [(3,12),(11,4)], c["main"]); line(im, [(4,12),(12,4)], c["main"]); line(im, [(3,11),(10,4)], c["light"])
    px(im, [(12,3),(13,2),(12,2),(13,3)], c["light"])
    line(im, [(3,9),(7,13)], c["dark"]); line(im, [(4,9),(7,12)], (190,160,60))
    line(im, [(1,14),(3,12)], WOOD); px(im, [(1,15),(0,14)], WOOD_D)
    return outline(im)

def pickaxe(c):
    im = canvas()
    line(im, [(2,14),(10,6)], WOOD); line(im, [(3,14),(10,7)], WOOD_D)
    for p in [(4,6),(5,4),(7,3),(9,3),(11,4),(12,6),(13,8)]:
        px(im, [p], c["main"]); px(im, [(p[0], p[1]+1)], c["dark"])
    px(im, [(7,2),(8,2),(10,3)], c["light"])
    return outline(im)

def axe(c):
    im = canvas()
    line(im, [(3,14),(11,5)], WOOD); line(im, [(4,14),(11,6)], WOOD_D)
    for (x, y) in [(8,2),(9,2),(10,2),(7,3),(8,3),(9,3),(10,3),(11,3),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(8,5),(9,5),(10,5),(12,5)]:
        px(im, [(x, y)], c["main"])
    px(im, [(8,2),(9,2),(7,3),(8,3)], c["light"]); px(im, [(12,4),(12,5),(10,5),(11,4)], c["dark"])
    return outline(im)

def spear(c):
    im = canvas()
    line(im, [(1,14),(12,3)], WOOD); line(im, [(2,14),(12,4)], WOOD_D)
    for p in [(13,2),(14,1),(13,1),(14,2),(12,1),(14,3),(12,2),(13,3),(11,2),(14,0),(15,0)]:
        px(im, [p], c["main"])
    px(im, [(13,2),(14,1),(12,2)], c["light"]); px(im, [(14,3),(13,3),(11,2)], c["dark"])
    return outline(im)

def helmet(c):
    im = canvas()
    for y, (a, b) in zip(range(3, 12), [(5,10),(4,11),(3,12),(3,12),(3,12),(3,12),(3,4),(11,12),(3,4)]):
        for x in range(a, b+1): px(im, [(x, y)], c["main"])
    for x in range(3, 13): px(im, [(x, 4)], c["light"])
    for x in (3,4,11,12): px(im, [(x, 10)], c["dark"]); px(im, [(x, 9)], c["dark"])
    for x in range(5, 11): px(im, [(x, 8)], c["dark"])
    return outline(im)

def chestplate(c):
    im = canvas()
    for y in range(2, 14):
        if y < 5: xs = list(range(1, 5)) + list(range(11, 15))
        else: xs = list(range(3, 13))
        for x in xs: px(im, [(x, y)], c["main"])
    for y in range(5, 14): px(im, [(3, y)], c["light"]); px(im, [(12, y)], c["dark"])
    px(im, [(6,5),(9,5),(7,6),(8,6),(7,8),(8,8),(7,10),(8,10)], c["dark"])
    for x in range(1, 5): px(im, [(x, 2)], c["light"])
    return outline(im)

def leggings(c):
    im = canvas()
    for y in range(2, 14):
        for x in range(3, 13):
            if y > 6 and x in (7, 8): continue
            px(im, [(x, y)], c["main"])
    for y in range(2, 14): px(im, [(3, y)], c["light"]); px(im, [(12, y)], c["dark"])
    for x in range(3, 13): px(im, [(x, 3)], c["dark"])
    return outline(im)

def boots(c):
    im = canvas()
    for y in range(6, 13):
        for x in list(range(2, 6)) + list(range(10, 14)): px(im, [(x, y)], c["main"])
    for x in list(range(2, 7)) + list(range(9, 14)): px(im, [(x, 12)], c["main"]); px(im, [(x, 13)], c["dark"])
    for y in range(6, 13): px(im, [(2, y)], c["light"]); px(im, [(10, y)], c["light"])
    return outline(im)

def pearl(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 13, 13], fill=c["main"] + (255,))
    d.ellipse([4, 4, 11, 11], fill=c["dark"] + (255,))
    d.ellipse([3, 3, 7, 7], fill=c["light"] + (255,))
    px(im, [(5,5)], (255,255,255)); px(im, [(10,9),(9,10),(10,10)], c["main"])
    return outline(im)

def totem(c):
    im = canvas()
    for y, (a, b) in zip(range(1, 15), [(5,10),(4,11),(3,12),(3,12),(4,11),(5,10),(3,12),(2,13),(5,10),(5,10),(6,9),(6,9),(5,10),(5,10)]):
        for x in range(a, b+1): px(im, [(x, y)], c["main"])
    px(im, [(5,4),(10,4)], (30,30,30)); px(im, [(6,6),(7,6),(8,6),(9,6)], (30,30,30))
    for y in range(1, 15): px(im, [(5, y)], c["light"]) if y in (1,2,7,8) else None
    px(im, [(6,9),(9,9),(7,12),(8,12)], c["dark"])
    return outline(im)

HEART_MASK = ["..XX....XX..", ".XXXX..XXXX.", "XXXXXXXXXXXX", "XXXXXXXXXXXX", "XXXXXXXXXXXX", ".XXXXXXXXXX.", "..XXXXXXXX..", "...XXXXXX...", "....XXXX....", ".....XX....."]
def heart(c):
    im = canvas()
    for y, row in enumerate(HEART_MASK):
        for x, ch in enumerate(row):
            if ch == "X":
                col = c["main"]
                if y < 3 and x < 6: col = c["light"]
                if y > 6: col = c["dark"]
                px(im, [(x + 2, y + 3)], col)
    px(im, [(4,5),(5,5)], (255,255,255))
    return outline(im)

def ingot(c):
    im = canvas()
    for y in range(5, 12):
        for x in range(2 + (11 - y) // 2, 11 + (11 - y) // 2 + 1):
            px(im, [(x, y)], c["main"])
    for x in range(5, 14): px(im, [(x, 5)], c["light"])
    for y in range(6, 12): px(im, [(2 + (11 - y)//2, y)], c["light"])
    for x in range(2, 11): px(im, [(x, 11)], c["dark"])
    px(im, [(8,8),(9,7)], (255,255,255))
    return outline(im)

def apple(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 14], fill=c["main"] + (255,))
    d.ellipse([3, 5, 7, 9], fill=c["light"] + (255,))
    d.ellipse([9, 9, 13, 14], fill=c["dark"] + (255,))
    px(im, [(8,3),(8,2),(9,1),(10,1),(10,2)], (60,160,60)); px(im, [(7,4),(8,4)], (90,60,30))
    px(im, [(5,6)], (255,255,255))
    return outline(im)

def food_steak(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([1, 3, 14, 13], fill=c["main"] + (255,))
    d.ellipse([3, 5, 12, 11], fill=c["dark"] + (255,))
    d.ellipse([5, 6, 9, 8], fill=c["light"] + (255,))
    px(im, [(12,5),(4,10),(10,10)], c["light"])
    return outline(im)

def food_chop(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 14, 13], fill=c["main"] + (255,))
    d.ellipse([4, 6, 11, 11], fill=c["dark"] + (255,))
    px(im, [(2,13),(1,14),(2,14),(3,14)], c["light"]); px(im, [(6,7),(7,7),(5,8)], c["light"])
    return outline(im)

def food_chicken(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 11, 10], fill=c["main"] + (255,))
    d.ellipse([4, 4, 9, 8], fill=c["dark"] + (255,))
    line(im, [(9,9),(13,13)], c["light"]); px(im, [(13,13),(14,13),(13,14),(14,14)], c["light"])
    px(im, [(4,3),(5,3)], c["light"])
    return outline(im)

def food_fish(c):
    im = canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 12, 11], fill=c["main"] + (255,))
    d.polygon([(11,7),(15,3),(15,12)], fill=c["dark"] + (255,))
    d.ellipse([4, 6, 7, 9], fill=c["light"] + (255,))
    px(im, [(5,6)], (20,20,20)); px(im, [(8,7),(8,8),(9,8)], c["dark"])
    return outline(im)

def food_potato(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 13], fill=c["main"] + (255,))
    d.ellipse([4, 6, 11, 11], fill=c["light"] + (255,))
    px(im, [(5,5),(10,5),(12,9),(3,10)], c["dark"])
    return outline(im)

def food_bread(c):
    im = canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 5, 14, 12], radius=3, fill=c["main"] + (255,))
    d.rounded_rectangle([2, 6, 13, 9], radius=2, fill=c["light"] + (255,))
    for x in (4, 7, 10): line(im, [(x, 6), (x + 1, 9)], c["dark"])
    return outline(im)

ICONS = {}
def add(name, fn, pal): ICONS[name] = fn(PAL[pal])

# food
add("golden_steak", food_steak, "gold"); add("golden_porkchop", food_chop, "gold")
add("golden_chicken", food_chicken, "gold"); add("golden_mutton", food_chop, "gold")
add("golden_rabbit", food_chicken, "gold"); add("golden_cod", food_fish, "gold")
add("golden_salmon", food_fish, "gold"); add("golden_baked_potato", food_potato, "gold")
add("golden_bread", food_bread, "gold")
add("immortal_apple", apple, "immortal"); add("godly_apple", apple, "godly")
add("immortal_ingot", ingot, "immortal"); add("godly_ingot", ingot, "godly")
add("bedrock_pickaxe", pickaxe, "bedrock")
for tier in ("immortal", "godly"):
    add(f"{tier}_pickaxe", pickaxe, tier); add(f"{tier}_axe", axe, tier)
    add(f"{tier}_sword", sword, tier); add(f"{tier}_spear", spear, tier)
    add(f"{tier}_helmet", helmet, tier); add(f"{tier}_chestplate", chestplate, tier)
    add(f"{tier}_leggings", leggings, tier); add(f"{tier}_boots", boots, tier)
    add(f"{tier}_ender_pearl", pearl, tier); add(f"{tier}_totem", totem, tier)
    add(f"{tier}_heart", heart, tier)
add("heart", heart, "purple" if False else "gold")
ICONS["heart"] = heart(dict(main=(225,40,50), dark=(150,15,35), light=(255,130,130)))
add("purple_hero_helmet", helmet, "purple"); add("purple_hero_chestplate", chestplate, "purple")
add("purple_hero_leggings", leggings, "purple"); add("purple_hero_boots", boots, "purple")

STAR = {"galaxy": [(255,255,255),(170,200,255)], "immortal": [(255,255,255),(255,180,255),(120,240,255)], "godly": [(255,225,110),(255,245,170)]}
def sparkle(img, tier, name):
    rnd = random.Random(tier + name)
    p = img.load()
    cells = [(x, y) for y in range(16) for x in range(16) if p[x, y][3] > 0 and p[x, y][:3] != OUT]
    for x, y in rnd.sample(cells, min(len(cells), max(3, len(cells) // 9))):
        p[x, y] = rnd.choice(STAR[tier]) + (255,)

for tier in ("galaxy",):
    add(f"{tier}_pickaxe", pickaxe, tier); add(f"{tier}_axe", axe, tier); add(f"{tier}_sword", sword, tier)
    add(f"{tier}_helmet", helmet, tier); add(f"{tier}_chestplate", chestplate, tier)
    add(f"{tier}_leggings", leggings, tier); add(f"{tier}_boots", boots, tier)
add("galaxy_ingot", ingot, "galaxy")
for _n, _img in ICONS.items():
    for _t in STAR:
        if _n.startswith(_t + "_"):
            sparkle(_img, _t, _n)

HANDHELD = {n for n in ICONS if n.endswith(("_pickaxe", "_axe", "_sword", "_spear"))}

# sword blocks
SWORD_BLOCKS = {"iron": "iron", "diamond": "diamond", "netherite": "netherite", "immortal": "immortal", "godly": "godly"}
def block_texture(tier):
    c = PAL[tier]
    rnd = random.Random(tier)
    base = Image.new("RGBA", (16, 16))
    p = base.load()
    for y in range(16):
        for x in range(16):
            j = rnd.randint(-10, 10)
            col = tuple(max(0, min(255, v + j)) for v in c["dark"])
            p[x, y] = col + (255,)
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, 15, 15], outline=c["main"] + (255,))
    d.rectangle([1, 1, 14, 14], outline=tuple(int(v*0.7) for v in c["dark"]) + (255,))
    s = sword(c)
    base.alpha_composite(s)
    if tier in STAR:
        pp = base.load()
        for _ in range(10):
            pp[rnd.randint(1, 14), rnd.randint(1, 14)] = rnd.choice(STAR[tier]) + (255,)
    return base

# ------------------------------------------------------------ armour layer textures (64x32)
def armour_layer(tier, layer):
    c = PAL[tier]
    rnd = random.Random(tier + str(layer))
    im = Image.new("RGBA", (64, 32))
    p = im.load()
    for y in range(32):
        for x in range(64):
            band = (x // 4 + y // 4 + layer) % 3
            col = [c["main"], c["dark"], c["light"]][band] if (x + y) % 7 == 0 else c["main"]
            if band == 1: col = tuple(int(v * 0.85) for v in c["main"])
            j = rnd.randint(-8, 8)
            p[x, y] = tuple(max(0, min(255, v + j)) for v in col) + (255,)
    d = ImageDraw.Draw(im)
    for yy in range(0, 32, 8):
        d.line([(0, yy), (63, yy)], fill=(c["dark"] if tier != "godly" else (255, 225, 120)) + (255,))
    if tier in STAR:
        for _ in range(70):
            p[rnd.randint(0, 63), rnd.randint(0, 31)] = rnd.choice(STAR[tier]) + (255,)
    return im

# ------------------------------------------------------------ write textures + models
for name, img in ICONS.items():
    os.makedirs(f"{A}/textures/item", exist_ok=True)
    img.save(f"{A}/textures/item/{name}.png")
    parent = "minecraft:item/handheld" if name in HANDHELD else "minecraft:item/generated"
    w(f"{A}/models/item/{name}.json", {"parent": parent, "textures": {"layer0": f"{NS}:item/{name}"}})
    w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})

for tier in SWORD_BLOCKS:
    name = f"{tier}_sword_block"
    os.makedirs(f"{A}/textures/block", exist_ok=True)
    block_texture(tier).save(f"{A}/textures/block/{name}.png")
    w(f"{A}/models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{name}"}})
    w(f"{A}/blockstates/{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
    w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:block/{name}"}})
    w(f"{D}/{NS}/loot_table/blocks/{name}.json", {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{name}"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}]})

for tier in ("galaxy", "immortal", "godly", "purple"):
    key = "purple_hero" if tier == "purple" else tier
    w(f"{A}/equipment/{key}.json", {"layers": {
        "humanoid": [{"texture": f"{NS}:{key}"}],
        "humanoid_leggings": [{"texture": f"{NS}:{key}"}]}})
    os.makedirs(f"{A}/textures/entity/equipment/humanoid", exist_ok=True)
    os.makedirs(f"{A}/textures/entity/equipment/humanoid_leggings", exist_ok=True)
    armour_layer(tier, 1).save(f"{A}/textures/entity/equipment/humanoid/{key}.png")
    armour_layer(tier, 2).save(f"{A}/textures/entity/equipment/humanoid_leggings/{key}.png")

# mod icon
icon = Image.new("RGBA", (128, 128), (20, 10, 40, 255))
big = sword(PAL["godly"]).resize((128, 128), Image.NEAREST)
icon.alpha_composite(big)
icon.save(f"{A}/icon.png")

# ------------------------------------------------------------ recipes
def shaped(name, pattern, key, result, count=1):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": pattern, "key": key, "result": {"id": result, "count": count}})
def shapeless(name, ings, result):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": ings, "result": {"id": result, "count": 1}})
def stonecut(name, ing, result):
    w(f"{D}/{NS}/recipe/{name}.json", {"type": "minecraft:stonecutting", "ingredient": ing, "result": {"id": result, "count": 1}})

m = lambda n: f"minecraft:{n}"
i = lambda n: f"{NS}:{n}"

# golden food: 8 gold nuggets around the cooked item
for g, base in [("golden_steak","cooked_beef"),("golden_porkchop","cooked_porkchop"),("golden_chicken","cooked_chicken"),
                ("golden_mutton","cooked_mutton"),("golden_rabbit","cooked_rabbit"),("golden_cod","cooked_cod"),
                ("golden_salmon","cooked_salmon"),("golden_baked_potato","baked_potato"),("golden_bread","bread")]:
    shaped(g, ["###", "#X#", "###"], {"#": m("gold_nugget"), "X": m(base)}, i(g))

# ingots
shaped("galaxy_ingot", ["ALA", "LDL", "ALA"], {"A": m("amethyst_block"), "L": m("lapis_block"), "D": m("diamond")}, i("galaxy_ingot"))
shaped("galaxy_pickaxe", ["III", " S ", " S "], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_pickaxe"))
shaped("galaxy_axe", ["II", "IS", " S"], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_axe"))
shaped("galaxy_sword", ["I", "I", "S"], {"I": i("galaxy_ingot"), "S": m("stick")}, i("galaxy_sword"))
shaped("galaxy_helmet", ["III", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_helmet"))
shaped("galaxy_chestplate", ["I I", "III", "III"], {"I": i("galaxy_ingot")}, i("galaxy_chestplate"))
shaped("galaxy_leggings", ["III", "I I", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_leggings"))
shaped("galaxy_boots", ["I I", "I I"], {"I": i("galaxy_ingot")}, i("galaxy_boots"))
shaped("immortal_ingot", ["NGN", "GSG", "NGN"], {"N": m("netherite_ingot"), "G": i("galaxy_ingot"), "S": m("nether_star")}, i("immortal_ingot"))
shaped("godly_ingot", ["IEI", "ESE", "IEI"], {"I": i("immortal_ingot"), "E": m("enchanted_golden_apple"), "S": m("nether_star")}, i("godly_ingot"))
shapeless("immortal_apple", [m("enchanted_golden_apple"), i("immortal_ingot")], i("immortal_apple"))
shapeless("godly_apple", [i("immortal_apple"), i("godly_ingot")], i("godly_apple"))

# bedrock pickaxe (upgrade of a netherite pickaxe)
shaped("bedrock_pickaxe", ["ONO", "NPN", "ONO"], {"O": m("obsidian"), "N": m("netherite_ingot"), "P": m("netherite_pickaxe")}, i("bedrock_pickaxe"))

for tier in ("immortal", "godly"):
    ing = i(f"{tier}_ingot")
    stick = {"immortal": m("blaze_rod"), "godly": m("end_rod")}[tier]
    shaped(f"{tier}_pickaxe", ["III", " S ", " S "], {"I": ing, "S": stick}, i(f"{tier}_pickaxe"))
    shaped(f"{tier}_axe", ["II", "IS", " S"], {"I": ing, "S": stick}, i(f"{tier}_axe"))
    shaped(f"{tier}_sword", ["I", "I", "S"], {"I": ing, "S": stick}, i(f"{tier}_sword"))
    shaped(f"{tier}_spear", ["  I", " S ", "S  "], {"I": ing, "S": stick}, i(f"{tier}_spear"))
    shaped(f"{tier}_helmet", ["III", "I I"], {"I": ing}, i(f"{tier}_helmet"))
    shaped(f"{tier}_chestplate", ["I I", "III", "III"], {"I": ing}, i(f"{tier}_chestplate"))
    shaped(f"{tier}_leggings", ["III", "I I", "I I"], {"I": ing}, i(f"{tier}_leggings"))
    shaped(f"{tier}_boots", ["I I", "I I"], {"I": ing}, i(f"{tier}_boots"))

shaped("immortal_ender_pearl", ["PPP", "PIP", "PPP"], {"P": m("ender_pearl"), "I": i("immortal_ingot")}, i("immortal_ender_pearl"))
shaped("godly_ender_pearl", ["EEE", "EIE", "EEE"], {"E": m("ender_eye"), "I": i("godly_ingot")}, i("godly_ender_pearl"))
shaped("immortal_totem", ["GIG", "ITI", "GIG"], {"G": m("gold_block"), "I": i("immortal_ingot"), "T": m("totem_of_undying")}, i("immortal_totem"))
shaped("godly_totem", ["EGE", "GTG", "EGE"], {"E": m("emerald_block"), "G": i("godly_ingot"), "T": i("immortal_totem")}, i("godly_totem"))
shaped("heart", ["DRD", "RAR", "DRD"], {"D": m("diamond"), "R": m("redstone_block"), "A": m("golden_apple")}, i("heart"))
shaped("immortal_heart", ["GHG", "HIH", "GHG"], {"G": m("gold_block"), "H": i("heart"), "I": i("immortal_ingot")}, i("immortal_heart"))
shaped("godly_heart", ["EHE", "HGH", "EHE"], {"E": m("emerald_block"), "H": i("immortal_heart"), "G": i("godly_ingot")}, i("godly_heart"))

# purple superhero armour (amethyst shards)
A_ = {"A": m("amethyst_shard")}
shaped("purple_hero_helmet", ["AAA", "A A"], A_, i("purple_hero_helmet"))
shaped("purple_hero_chestplate", ["A A", "AAA", "AAA"], A_, i("purple_hero_chestplate"))
shaped("purple_hero_leggings", ["AAA", "A A", "A A"], A_, i("purple_hero_leggings"))
shaped("purple_hero_boots", ["A A", "A A"], A_, i("purple_hero_boots"))

# sword blocks via stonecutter
stonecut("iron_sword_block", m("iron_block"), i("iron_sword_block"))
stonecut("diamond_sword_block", m("diamond_block"), i("diamond_sword_block"))
stonecut("netherite_sword_block", m("netherite_block"), i("netherite_sword_block"))
stonecut("immortal_sword_block", i("immortal_ingot"), i("immortal_sword_block"))
stonecut("godly_sword_block", i("godly_ingot"), i("godly_sword_block"))

# ------------------------------------------------------------ tags
def tag(path, values):
    w(f"{D}/minecraft/tags/{path}.json", {"replace": False, "values": values})

sw = [i(f"{t}_sword_block") for t in SWORD_BLOCKS] + [i("galaxy_sword"), i("immortal_sword"), i("godly_sword")]
tag("item/swords", sw)
for t in ("enchantable/sword", "enchantable/sharp_weapon", "enchantable/fire_aspect", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/sweeping", "enchantable/vanishing"):
    tag(f"item/{t}", sw)
spears = [i("immortal_spear"), i("godly_spear")]
for t in ("enchantable/sharp_weapon", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/fire_aspect"):
    pass
w(f"{D}/minecraft/tags/item/enchantable/spear_extra.json", {"replace": False, "values": spears}) if False else None
# add spears into the weapon tags too (second pass merges in the same file)
for t in ("enchantable/sharp_weapon", "enchantable/melee_weapon", "enchantable/weapon", "enchantable/fire_aspect", "enchantable/vanishing"):
    tag(f"item/{t}", sw + spears)
picks = [i("bedrock_pickaxe"), i("galaxy_pickaxe"), i("immortal_pickaxe"), i("godly_pickaxe")]
axes_ = [i("galaxy_axe"), i("immortal_axe"), i("godly_axe")]
tag("item/pickaxes", picks); tag("item/axes", axes_)
for t in ("enchantable/mining", "enchantable/mining_loot", "enchantable/vanishing"):
    tag(f"item/{t}", picks + axes_ + (sw if t == "enchantable/vanishing" else []) + (spears if t == "enchantable/vanishing" else []))
heads = [i("immortal_helmet"), i("godly_helmet"), i("purple_hero_helmet"), i("galaxy_helmet")]
chests = [i("immortal_chestplate"), i("godly_chestplate"), i("purple_hero_chestplate"), i("galaxy_chestplate")]
legs = [i("immortal_leggings"), i("godly_leggings"), i("purple_hero_leggings"), i("galaxy_leggings")]
feet = [i("immortal_boots"), i("godly_boots"), i("purple_hero_boots"), i("galaxy_boots")]
tag("item/head_armor", heads); tag("item/chest_armor", chests); tag("item/leg_armor", legs); tag("item/foot_armor", feet)
tag("item/enchantable/head_armor", heads); tag("item/enchantable/chest_armor", chests)
tag("item/enchantable/leg_armor", legs); tag("item/enchantable/foot_armor", feet)
tag("item/enchantable/armor", heads + chests + legs + feet)
tag("item/enchantable/equippable", heads + chests + legs + feet)
# durability only matters for the breakable stuff: sword blocks (iron/diamond/netherite) and purple hero armour
tag("item/enchantable/durability", [i("iron_sword_block"), i("diamond_sword_block"), i("netherite_sword_block")] + heads[2:] + chests[2:] + legs[2:] + feet[2:] + [i("galaxy_sword"), i("galaxy_pickaxe"), i("galaxy_axe")])
tag("block/mineable/pickaxe", [i(f"{t}_sword_block") for t in SWORD_BLOCKS])

# ------------------------------------------------------------ language
NAMES = {
 "itemGroup.immortal": "Immortal & Godly",
 "item.immortal.immortal_ingot": "Immortal Ingot", "item.immortal.godly_ingot": "Godly Ingot",
 "item.immortal.golden_steak": "Golden Steak", "item.immortal.golden_porkchop": "Golden Porkchop",
 "item.immortal.golden_chicken": "Golden Chicken", "item.immortal.golden_mutton": "Golden Mutton",
 "item.immortal.golden_rabbit": "Golden Rabbit", "item.immortal.golden_cod": "Golden Cod",
 "item.immortal.golden_salmon": "Golden Salmon", "item.immortal.golden_baked_potato": "Golden Baked Potato",
 "item.immortal.golden_bread": "Golden Bread",
 "item.immortal.immortal_apple": "Immortal Apple", "item.immortal.godly_apple": "Godly Apple",
 "item.immortal.bedrock_pickaxe": "Bedrock Pickaxe",
 "item.immortal.heart": "Heart",
}
for tier, T in (("immortal", "Immortal"), ("godly", "Godly")):
    for k, v in (("pickaxe","Pickaxe"),("axe","Axe"),("sword","Sword"),("spear","Spear"),("helmet","Helmet"),
                 ("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots"),("ender_pearl","Ender Pearl"),
                 ("totem","Totem"),("heart","Heart")):
        NAMES[f"item.immortal.{tier}_{k}"] = f"{T} {v}"
NAMES["item.immortal.galaxy_ingot"] = "Galaxy Ingot"
for k, v in (("pickaxe","Pickaxe"),("axe","Axe"),("sword","Sword"),("helmet","Helmet"),("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots")):
    NAMES[f"item.immortal.galaxy_{k}"] = f"Galaxy {v}"
for k, v in (("helmet","Helmet"),("chestplate","Chestplate"),("leggings","Leggings"),("boots","Boots")):
    NAMES[f"item.immortal.purple_hero_{k}"] = f"Purple Hero {v}"
for t in SWORD_BLOCKS:
    NAMES[f"block.immortal.{t}_sword_block"] = f"{t.capitalize()} Sword Block"
w(f"{A}/lang/en_us.json", NAMES)
print("icons:", len(ICONS), "lang:", len(NAMES))
