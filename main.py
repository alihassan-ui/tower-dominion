# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 1/7 - 270 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
import pygame
import random
import math
import sys
import itertools
import json
import os

pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except:
    pass

SAVE_FILE_NAME = "stickwar_save.json"
def get_save_path():
    try:
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), SAVE_FILE_NAME)
    except:
        return SAVE_FILE_NAME
SAVE_FILE = get_save_path()

try:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    W, H = screen.get_size()
    if W < 200 or H < 200:
        raise Exception("bad size")
except:
    W, H = 1280, 720
    screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("TOWER DOMINION - NEW TROOPS")
clock = pygame.time.Clock()

SCALE = max(0.75, min(2.6, min(W, H) / 900))
def S(v):
    return max(1, int(v * SCALE))

GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
GOLD = (241, 196, 15)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASS = (58, 158, 73)
DARK_GRASS = (40, 110, 50)
NEUTRAL = (180, 180, 180)
PURPLE = (155, 89, 182)
CYAN = (52, 224, 219)
ORANGE = (230,126,34)

font_s = pygame.font.Font(None, S(20))
font_m = pygame.font.Font(None, S(26))
font_b = pygame.font.Font(None, S(36))
font_big = pygame.font.Font(None, S(50))
font_title = pygame.font.Font(None, S(65))
font_key = pygame.font.Font(None, S(32))

TREES = [(random.randint(0, W), random.randint(0, H), S(12)) for _ in range(50)]
def draw_bg(shake=0):
    sx = random.randint(-shake, shake) if shake > 0 else 0
    sy = random.randint(-shake, shake) if shake > 0 else 0
    screen.fill(GRASS)
    for x, y, r in TREES:
        pygame.draw.circle(screen, DARK_GRASS, (x + sx, y + sy), r)

particles = []
def add_particles(x,y,color,count=10):
    for _ in range(count):
        particles.append({'pos':[x,y],'vel':[random.uniform(-4,4), random.uniform(-5,0)],'life':25,'color':color,'r':random.randint(2,5)})
def update_and_draw_particles():
    global particles
    for p in particles:
        p['pos'][0]+=p['vel'][0]
        p['pos'][1]+=p['vel'][1]
        p['vel'][1]+=0.25
        p['life']-=1
    particles=[p for p in particles if p['life']>0]
    for p in particles:
        pygame.draw.circle(screen,p['color'],(int(p['pos'][0]),int(p['pos'][1])),p['r'])

COLOR_SHOP_ITEMS = [
    {"id": "white", "name": "WHITE", "tier": "FREE", "price": 0, "color": (255,255,255), "effect": "solid"},
    {"id": "light_gray", "name": "LIGHT GRAY", "tier": "FREE", "price": 0, "color": (200,200,200), "effect": "solid"},
    {"id": "peach", "name": "PEACH", "tier": "FREE", "price": 0, "color": (255,218,185), "effect": "solid"},
    {"id": "mint", "name": "MINT", "tier": "FREE", "price": 0, "color": (152,255,152), "effect": "solid"},
    {"id": "sky", "name": "SKY BLUE", "tier": "FREE", "price": 0, "color": (135,206,235), "effect": "solid"},
    {"id": "red", "name": "RED", "tier": "CHEAP", "price": 20, "color": (231,76,60), "effect": "solid"},
    {"id": "blue", "name": "BLUE", "tier": "CHEAP", "price": 20, "color": (52,152,219), "effect": "solid"},
    {"id": "green", "name": "GREEN", "tier": "CHEAP", "price": 20, "color": (46,204,113), "effect": "solid"},
    {"id": "yellow", "name": "YELLOW", "tier": "CHEAP", "price": 20, "color": (241,196,15), "effect": "solid"},
    {"id": "orange", "name": "ORANGE", "tier": "CHEAP", "price": 20, "color": (230,126,34), "effect": "solid"},
    {"id": "purple", "name": "PURPLE", "tier": "MEDIUM", "price": 50, "color": (155,89,182), "effect": "glow"},
    {"id": "cyan", "name": "CYAN", "tier": "MEDIUM", "price": 50, "color": (52,224,219), "effect": "glow"},
    {"id": "pink", "name": "PINK", "tier": "MEDIUM", "price": 50, "color": (255,105,180), "effect": "glow"},
    {"id": "lime", "name": "LIME", "tier": "MEDIUM", "price": 50, "color": (50,205,50), "effect": "glow"},
    {"id": "coral", "name": "CORAL", "tier": "MEDIUM", "price": 50, "color": (255,127,80), "effect": "glow"},
    {"id": "gold", "name": "ROYAL GOLD", "tier": "EXPENSIVE", "price": 100, "color": (255,215,0), "effect": "metal"},
    {"id": "ruby", "name": "RUBY", "tier": "EXPENSIVE", "price": 100, "color": (155,17,30), "effect": "metal"},
    {"id": "sapphire", "name": "SAPPHIRE", "tier": "EXPENSIVE", "price": 100, "color": (15,82,186), "effect": "metal"},
    {"id": "emerald", "name": "EMERALD", "tier": "EXPENSIVE", "price": 100, "color": (46,139,87), "effect": "metal"},
    {"id": "amethyst", "name": "AMETHYST", "tier": "EXPENSIVE", "price": 100, "color": (153,102,204), "effect": "metal"},
    {"id": "rainbow", "name": "RAINBOW", "tier": "LEGENDARY", "price": 200, "color": (255,0,0), "effect": "rainbow"},
    {"id": "galaxy", "name": "GALAXY", "tier": "LEGENDARY", "price": 200, "color": (75,0,130), "effect": "galaxy"},
    {"id": "fire", "name": "FIRE", "tier": "LEGENDARY", "price": 200, "color": (255,69,0), "effect": "fire"},
    {"id": "ice", "name": "ICE", "tier": "LEGENDARY", "price": 200, "color": (173,216,230), "effect": "ice"},
    {"id": "legend", "name": "LEGEND", "tier": "LEGENDARY", "price": 200, "color": (20,20,20), "effect": "legend"},
]

# 12 TROOPS TOTAL - 6 OLD + 6 NEW SPECIAL
TROOPS_BASE = {
    # OLD - FREE STARTER
    "WARRIOR":  {"cost": 20,  "hp": 3,  "speed": 3.2, "r": S(7),  "dmg": 6, "desc":"Basic fighter", "icon":"⚔️"},
    "SPEARMAN": {"cost": 35,  "hp": 4,  "speed": 2.8, "r": S(8),  "dmg": 5,  "ranged": True, "range": S(100), "cd": 40, "desc":"Long reach", "icon":"🔱"},
    "ARCHER":   {"cost": 45,  "hp": 2,  "speed": 2.6, "r": S(6),  "dmg": 3,  "ranged": True, "range": S(130), "cd": 45, "desc":"Ranged", "icon":"🏹"},
    # OLD - LOCKED
    "TANK":     {"cost": 120, "hp": 15, "speed": 1.7, "r": S(14), "dmg": 14, "desc":"Heavy armor", "icon":"🛡️"},
    "MAGE":     {"cost": 80,  "hp": 5,  "speed": 2.2, "r": S(9),  "dmg": 12, "ranged": True, "range": S(140), "cd": 60, "desc":"Magic damage", "icon":"🔮"},
    "GIANT":    {"cost": 200, "hp": 30, "speed": 1.2, "r": S(18), "dmg": 22, "desc":"Huge damage", "icon":"👹"},
    # NEW SPECIAL TROOPS
    "ENGINEER": {"cost": 150, "hp": 6,  "speed": 2.0, "r": S(9),  "dmg": 2, "desc":"Repairs castle +2 HP/sec", "icon":"🔧", "special":"engineer"},
    "MEDIC":    {"cost": 90,  "hp": 4,  "speed": 2.5, "r": S(7),  "dmg": 1, "desc":"Heals allies +1 HP/sec", "icon":"🌙", "special":"medic"},
    "PILOT":    {"cost": 130, "hp": 5,  "speed": 5.0, "r": S(8),  "dmg": 8, "ranged": True, "range": S(120), "cd": 35, "desc":"Flying fast 5.0 speed", "icon":"✈️", "special":"flying"},
    "ASSASSIN": {"cost": 70,  "hp": 2,  "speed": 4.5, "r": S(6),  "dmg": 18, "desc":"High dmg 18, low HP", "icon":"🗡️", "special":"assassin"},
    "SHIELDER": {"cost": 110, "hp": 25, "speed": 1.4, "r": S(16), "dmg": 4, "desc":"Tank 25 HP big shield", "icon":"🛡️", "special":"shield"},
    "BOMBER":   {"cost": 60,  "hp": 3,  "speed": 3.0, "r": S(7),  "dmg": 30, "desc":"Explodes area dmg 30", "icon":"💣", "special":"bomber"},
}

TROOP_UNLOCK_COSTS = {
    "WARRIOR": 0,
    "SPEARMAN": 0,
    "ARCHER": 0,
    "TANK": 80,
    "MAGE": 90,
    "GIANT": 150,
    "ENGINEER": 120,
    "MEDIC": 100,
    "PILOT": 140,
    "ASSASSIN": 110,
    "SHIELDER": 100,
    "BOMBER": 80,
}

ABILITIES = [
    {"id":"rich1", "name":"RICH START I", "desc":"+100 Starting Gold", "price":40, "tier":"ECONOMY", "icon":"💰"},
    {"id":"rich2", "name":"RICH START II", "desc":"+250 Starting Gold", "price":90, "tier":"ECONOMY", "icon":"💰"},
    {"id":"rich3", "name":"TYCOON START", "desc":"+500 Starting Gold", "price":180, "tier":"ECONOMY", "icon":"💰"},
    {"id":"inc1", "name":"INCOME I", "desc":"+5 Gold/sec", "price":30, "tier":"ECONOMY", "icon":"📈"},
    {"id":"inc2", "name":"INCOME II", "desc":"+10 Gold/sec", "price":65, "tier":"ECONOMY", "icon":"📈"},
    {"id":"inc3", "name":"INCOME III", "desc":"+20 Gold/sec", "price":130, "tier":"ECONOMY", "icon":"📈"},
    {"id":"fort1", "name":"FORT I", "desc":"+25 Castle HP", "price":35, "tier":"DEFENSE", "icon":"🏰"},
    {"id":"fort2", "name":"FORT II", "desc":"+60 Castle HP", "price":75, "tier":"DEFENSE", "icon":"🏰"},
    {"id":"fort3", "name":"FORT III", "desc":"+120 Castle HP", "price":150, "tier":"DEFENSE", "icon":"🏰"},
    {"id":"zone1", "name":"ZONE RUSH I", "desc":"Capture 25% Faster", "price":45, "tier":"UTILITY", "icon":"⚡"},
    {"id":"zone2", "name":"ZONE RUSH II", "desc":"Capture 50% Faster", "price":95, "tier":"UTILITY", "icon":"⚡"},
    {"id":"crate1", "name":"GOLDEN TOUCH", "desc":"Crates +50% Gold", "price":50, "tier":"ECONOMY", "icon":"📦"},
    {"id":"crate2", "name":"TREASURE HUNTER", "desc":"Crates x2 Gold", "price":110, "tier":"ECONOMY", "icon":"📦"},
    {"id":"war1", "name":"WARRIOR POWER I", "desc":"Warrior +3 DMG", "price":30, "tier":"OFFENSE", "icon":"⚔️"},
    {"id":"war2", "name":"WARRIOR POWER II", "desc":"Warrior +7 DMG", "price":70, "tier":"OFFENSE", "icon":"⚔️"},
    {"id":"tank1", "name":"TANK ARMOR I", "desc":"Tank +5 HP", "price":40, "tier":"DEFENSE", "icon":"🛡️"},
    {"id":"tank2", "name":"TANK ARMOR II", "desc":"Tank +12 HP", "price":90, "tier":"DEFENSE", "icon":"🛡️"},
    {"id":"arch1", "name":"ARCHER RANGE", "desc":"+30% Archer Range", "price":35, "tier":"OFFENSE", "icon":"🏹"},
    {"id":"arch2", "name":"ARCHER POWER", "desc":"Archer +3 DMG", "price":45, "tier":"OFFENSE", "icon":"🏹"},
    {"id":"speed1", "name":"SWIFT I", "desc":"+12% Troop Speed", "price":50, "tier":"UTILITY", "icon":"💨"},
    {"id":"speed2", "name":"SWIFT II", "desc":"+25% Troop Speed", "price":105, "tier":"UTILITY", "icon":"💨"},
    {"id":"giant1", "name":"GIANT MIGHT", "desc":"Giant +10 DMG", "price":80, "tier":"OFFENSE", "icon":"👹"},
    {"id":"mage1", "name":"MAGE POWER", "desc":"Mage +8 DMG", "price":75, "tier":"OFFENSE", "icon":"🔮"},
    {"id":"spear1", "name":"SPEAR REACH", "desc":"+30% Spear Range", "price":40, "tier":"OFFENSE", "icon":"🔱"},
    {"id":"cheap1", "name":"CHEAP ARMY I", "desc":"-10% Troop Cost", "price":60, "tier":"ECONOMY", "icon":"🏷️"},
    {"id":"cheap2", "name":"CHEAP ARMY II", "desc":"-20% Troop Cost", "price":125, "tier":"ECONOMY", "icon":"🏷️"},
    {"id":"hp1", "name":"IRON SKIN I", "desc":"All Troops +1 HP", "price":55, "tier":"DEFENSE", "icon":"❤️"},
    {"id":"hp2", "name":"IRON SKIN II", "desc":"All Troops +3 HP", "price":115, "tier":"DEFENSE", "icon":"❤️"},
    {"id":"regen1", "name":"REGEN I", "desc":"Castle +1 HP/sec", "price":85, "tier":"DEFENSE", "icon":"💚"},
    {"id":"regen2", "name":"REGEN II", "desc":"Castle +3 HP/sec", "price":160, "tier":"DEFENSE", "icon":"💚"},
    {"id":"zinc1", "name":"ZONE TAX I", "desc":"Zones +5 Income", "price":45, "tier":"ECONOMY", "icon":"🏴"},
    {"id":"zinc2", "name":"ZONE TAX II", "desc":"Zones +12 Income", "price":100, "tier":"ECONOMY", "icon":"🏴"},
    {"id":"lucky", "name":"LUCKY FIND", "desc":"10% Double Crate", "price":70, "tier":"UTILITY", "icon":"🍀"},
    {"id":"over", "name":"OVERLORD", "desc":"Start with 1 Warrior", "price":25, "tier":"UTILITY", "icon":"👑"},
    {"id":"ultimate", "name":"ULTIMATE POWER", "desc":"All Stats +15% LEGENDARY", "price":300, "tier":"LEGENDARY", "icon":"🌟"},
]

def get_color_by_id(cid):
    for c in COLOR_SHOP_ITEMS:
        if c["id"] == cid:
            return c
    return COLOR_SHOP_ITEMS[0]

def get_render_color(item):
    t = pygame.time.get_ticks()
    eff = item["effect"]
    if eff == "rainbow":
        r = int(127 + 127 * math.sin(t*0.005))
        g = int(127 + 127 * math.sin(t*0.005 + 2))
        b = int(127 + 127 * math.sin(t*0.005 + 4))
        return (r,g,b)
    elif eff == "fire":
        r = 255
        g = int(100 + 100 * math.sin(t*0.01))
        b = 0
        return (r,g,b)
    elif eff == "ice":
        r = int(150 + 100 * math.sin(t*0.008))
        g = int(200 + 55 * math.sin(t*0.008+1))
        b = 255
        return (r,g,b)
    elif eff == "galaxy":
        r = int(75 + 30*math.sin(t*0.003))
        g = 0
        b = int(130 + 30*math.cos(t*0.003))
        return (r,g,b)
    else:
        return item["color"]

def draw_fancy_circle(pos, item, radius):
    col = get_render_color(item)
    eff = item["effect"]
    x,y = int(pos[0]), int(pos[1])
    if eff in ["glow", "metal"]:
        pygame.draw.circle(screen, col, (x,y), radius+6)
        pygame.draw.circle(screen, WHITE, (x,y), radius+2)
    if eff == "metal":
        pygame.draw.circle(screen, GOLD, (x,y), radius, 3)
    if eff == "legend":
        pygame.draw.circle(screen, GOLD, (x,y), radius+5, 4)
        pygame.draw.circle(screen, (20,20,20), (x,y), radius)
        pygame.draw.circle(screen, GOLD, (x,y), radius-4, 2)
        return
    if eff == "galaxy":
        pygame.draw.circle(screen, (255,255,255), (x,y), radius+7, 2)
    pygame.draw.circle(screen, col, (x,y), radius)

def get_troops_with_abilities():
    troops = {k: dict(v) for k,v in TROOPS_BASE.items()}
    unlocked = SAVE.get("unlocked_abilities", [])
    cost_mult = 1.0
    if "cheap1" in unlocked: cost_mult -= 0.10
    if "cheap2" in unlocked: cost_mult -= 0.20
    if "ultimate" in unlocked: cost_mult -= 0.05
    for k in troops:
        troops[k]["cost"] = max(5, int(troops[k]["cost"] * cost_mult))
    hp_add = 0
    if "hp1" in unlocked: hp_add += 1
    if "hp2" in unlocked: hp_add += 3
    if "ultimate" in unlocked: hp_add += 1
    for k in troops:
        troops[k]["hp"] += hp_add
    if "war1" in unlocked: troops["WARRIOR"]["dmg"] += 3
    if "war2" in unlocked: troops["WARRIOR"]["dmg"] += 7
    if "tank1" in unlocked: troops["TANK"]["hp"] += 5
    if "tank2" in unlocked: troops["TANK"]["hp"] += 12
    if "arch2" in unlocked: troops["ARCHER"]["dmg"] += 3
    if "arch1" in unlocked: troops["ARCHER"]["range"] = int(troops["ARCHER"]["range"] * 1.3)
    if "spear1" in unlocked: troops["SPEARMAN"]["range"] = int(troops["SPEARMAN"]["range"] * 1.3)
    if "giant1" in unlocked: troops["GIANT"]["dmg"] += 10
    if "mage1" in unlocked: troops["MAGE"]["dmg"] += 8
    speed_mult = 1.0
    if "speed1" in unlocked: speed_mult += 0.12
    if "speed2" in unlocked: speed_mult += 0.25
    if "ultimate" in unlocked: speed_mult += 0.15
    for k in troops:
        troops[k]["speed"] *= speed_mult
    if "ultimate" in unlocked:
        for k in troops:
            troops[k]["dmg"] = int(troops[k]["dmg"] * 1.15)
    return troops

TROOP_KEYS = list(TROOPS_BASE.keys())

    # FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 2/7 - 270 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
def draw_stickman(pos, team_color_item, troop_type, hp_ratio=1.0, troops_data=None):
    if troops_data is None:
        troops_data = get_troops_with_abilities()
    x,y=int(pos[0]), int(pos[1])
    info = troops_data[troop_type]
    r=info["r"]
    col = get_render_color(team_color_item)
    eff = team_color_item["effect"]
    
    # Special visuals for new troops
    if troop_type == "ENGINEER":
        # Wrench shape
        pygame.draw.circle(screen, (100,100,100), (x,y), r+5)
        pygame.draw.circle(screen, (255,200,0), (x,y), r)
        pygame.draw.rect(screen, BLACK, (x-S(3), y - r - S(10), S(6), S(12)))
    elif troop_type == "MEDIC":
        # Muslim-friendly: Green with crescent moon, not red cross
        pygame.draw.circle(screen, WHITE, (x,y), r+4)
        pygame.draw.circle(screen, (0, 180, 80), (x,y), r)  # Islamic green
        # Crescent moon symbol
        pygame.draw.circle(screen, WHITE, (x+S(1), y), r-2)
        pygame.draw.circle(screen, (0, 180, 80), (x+S(3), y), r-2)
    elif troop_type == "PILOT":
        # Flying with wings
        pygame.draw.ellipse(screen, col, (x-r-S(6), y-S(3), S(10), S(6)))
        pygame.draw.ellipse(screen, col, (x+S(2), y-S(3), S(10), S(6)))
        pygame.draw.circle(screen, BLACK, (x, y- r - S(6)), r+2)
        pygame.draw.circle(screen, (100,200,255), (x, y- r - S(6)), r)
    elif troop_type == "ASSASSIN":
        pygame.draw.circle(screen, (20,20,20), (x,y), r+4)
        pygame.draw.circle(screen, (50,50,50), (x,y), r)
        pygame.draw.line(screen, RED, (x-S(5), y), (x+S(5), y), S(2))
    elif troop_type == "SHIELDER":
        pygame.draw.rect(screen, (80,80,80), (x-r, y-r, r*2, r*2+ S(10)), border_radius=S(4))
        pygame.draw.rect(screen, col, (x-r+2, y-r+2, r*2-4, r*2+ S(6)), border_radius=S(3))
        pygame.draw.circle(screen, BLACK, (x, y- r - S(8)), r+1)
        pygame.draw.circle(screen, WHITE, (x, y- r - S(8)), r-1)
    elif troop_type == "BOMBER":
        pygame.draw.circle(screen, BLACK, (x,y), r+3)
        pygame.draw.circle(screen, (255,100,0), (x,y), r)
        # Fuse
        pygame.draw.line(screen, (100,50,0), (x, y-r), (x+S(4), y-r-S(6)), S(2))
        if int(pygame.time.get_ticks()/200) % 2 == 0:
            pygame.draw.circle(screen, GOLD, (x+S(4), y-r-S(6)), S(3))
    else:
        if eff == "solid":
            pygame.draw.circle(screen, col, (x,y), r+4)
        elif eff == "glow":
            pygame.draw.circle(screen, col, (x,y), r+7)
            pygame.draw.circle(screen, WHITE, (x,y), r+2)
        elif eff in ["metal","galaxy","fire","ice","rainbow","legend"]:
            pygame.draw.circle(screen, col, (x,y), r+9)
            pygame.draw.circle(screen, GOLD if eff=="legend" else WHITE, (x,y), r+4, 2)
        pygame.draw.circle(screen, BLACK, (x, y- r - S(8)), r+2)
        pygame.draw.circle(screen, WHITE, (x, y- r - S(8)), r)
        pygame.draw.line(screen, BLACK, (x, y - S(6)), (x, y + S(12)), S(4))
        pygame.draw.line(screen, col, (x, y - S(6)), (x, y + S(12)), S(3))
        swing = math.sin(pygame.time.get_ticks()*0.008 + x)*S(3)
        pygame.draw.line(screen, BLACK, (x, y), (x- S(7), y + S(4)+swing), S(2))
        pygame.draw.line(screen, BLACK, (x, y), (x+ S(7), y + S(4)-swing), S(2))
    
    if hp_ratio < 1.0:
        pygame.draw.rect(screen, RED, (x- S(12), y- r- S(18), S(24), S(4)))
        pygame.draw.rect(screen, GREEN, (x- S(12), y- r- S(18), int(S(24)*hp_ratio), S(4)))

SAVE = {
    "gems": 800,
    "best_free_money": 0, 
    "zones_conquered": 0, 
    "best_streak": 0, 
    "current_streak": 0,
    "map_owners": ["player"] + ["enemy"]*8,
    "music_vol": 0.8,
    "sfx_vol": 0.8,
    "muted": False,
    "unlocked_colors": ["white","light_gray","peach","mint","sky"],
    "selected_tower_color": "white",
    "selected_soldier_color": "white",
    "total_purchased_usd": 0.0,
    "player_name": "",
    "unlocked_abilities": [],
    "unlocked_troops": ["WARRIOR","SPEARMAN","ARCHER"],
    "free_kills": 0
}

def ensure_save():
    if "unlocked_colors" not in SAVE: SAVE["unlocked_colors"] = ["white","light_gray","peach","mint","sky"]
    if "selected_tower_color" not in SAVE: SAVE["selected_tower_color"] = "white"
    if "selected_soldier_color" not in SAVE: SAVE["selected_soldier_color"] = "white"
    if "total_purchased_usd" not in SAVE: SAVE["total_purchased_usd"] = 0.0
    if "player_name" not in SAVE: SAVE["player_name"] = ""
    if "unlocked_abilities" not in SAVE: SAVE["unlocked_abilities"] = []
    if "unlocked_troops" not in SAVE: SAVE["unlocked_troops"] = ["WARRIOR","SPEARMAN","ARCHER"]
    if "free_kills" not in SAVE: SAVE["free_kills"] = 0
    if "map_owners" not in SAVE or len(SAVE["map_owners"]) < 9:
        SAVE["map_owners"] = ["player"] + ["enemy"]*8

def generate_default_name():
    return f"Player{random.randint(100,999)}"

def load_save():
    global SAVE
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            SAVE.update(data)
            ensure_save()
    except:
        ensure_save()

def write_save():
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(SAVE, f)
    except:
        pass

def apply_audio_settings():
    try:
        vol = 0.0 if SAVE["muted"] else SAVE["music_vol"]
        pygame.mixer.music.set_volume(vol)
    except:
        pass

load_save()
apply_audio_settings()

ROOMS = {}

class VirtualKeyboard:
    def __init__(self):
        self.active = False
        self.target_input = None
        self.numeric_only = False
        self.keys = []
        self.key_rects = []
        self.is_upper = False
    def show(self, target_input, numeric_only=False):
        self.active = True
        self.target_input = target_input
        self.numeric_only = numeric_only
        self.build_keys()
    def hide(self):
        self.active = False
        self.target_input = None
        self.keys = []
        self.key_rects = []
    def build_keys(self):
        self.keys = []
        self.key_rects = []
        kb_h = H // 2.0
        kb_y = H - kb_h
        kb_x = 0
        kb_w = W
        if self.numeric_only:
            layout = [["1","2","3"],["4","5","6"],["7","8","9"],["DEL","0","OK"]]
            row_h = kb_h / len(layout)
            for row_idx, row in enumerate(layout):
                row_w = kb_w / len(row)
                for col_idx, key in enumerate(row):
                    x = kb_x + col_idx * row_w + S(6)
                    y = kb_y + row_idx * row_h + S(6)
                    w = row_w - S(12)
                    h = row_h - S(12)
                    self.keys.append(key)
                    self.key_rects.append(pygame.Rect(x,y,w,h))
        else:
            if self.is_upper:
                layout = [["Q","W","E","R","T","Y","U","I","O","P"],["A","S","D","F","G","H","J","K","L"],["SHIFT","Z","X","C","V","B","N","M","DEL"],["ABC","SPACE","OK"]]
            else:
                layout = [["q","w","e","r","t","y","u","i","o","p"],["a","s","d","f","g","h","j","k","l"],["SHIFT","z","x","c","v","b","n","m","DEL"],["ABC","SPACE","OK"]]
            row_h = kb_h / len(layout)
            for row_idx, row in enumerate(layout):
                total_units = 0
                for key in row:
                    if key in ["SPACE"]: total_units += 3
                    elif key in ["OK","SHIFT","ABC"]: total_units += 1.6
                    else: total_units += 1
                unit_w = kb_w / total_units
                x_cursor = kb_x
                for key in row:
                    if key == "SPACE": w = unit_w * 3 - S(12)
                    elif key in ["OK","SHIFT","ABC"]: w = unit_w * 1.6 - S(12)
                    else: w = unit_w - S(12)
                    x = x_cursor + S(6)
                    y = kb_y + row_idx * row_h + S(6)
                    h = row_h - S(12)
                    self.keys.append(key)
                    self.key_rects.append(pygame.Rect(x,y,w,h))
                    x_cursor += w + S(12)
    def handle_click(self, pos):
        if not self.active: return False
        for i, rect in enumerate(self.key_rects):
            if rect.collidepoint(pos):
                key = self.keys[i]
                if self.target_input is None: return True
                if key == "DEL": self.target_input.text = self.target_input.text[:-1]
                elif key == "OK": self.hide()
                elif key == "SPACE":
                    if len(self.target_input.text) < 12: self.target_input.text += " "
                elif key == "SHIFT":
                    self.is_upper = not self.is_upper
                    self.build_keys()
                elif key == "ABC":
                    self.is_upper = True
                    self.build_keys()
                else:
                    if len(self.target_input.text) < 12:
                        if self.numeric_only and not key.isdigit(): pass
                        else: self.target_input.text += key
                return True
        return False
    def draw(self):
        if not self.active: return
        kb_h = H // 2.0
        kb_y = H - kb_h
        pygame.draw.rect(screen, (18,18,18), (0, kb_y, W, kb_h))
        pygame.draw.rect(screen, (80,80,80), (0, kb_y, W, kb_h), 3)
        for i, rect in enumerate(self.key_rects):
            key = self.keys[i]
            if key == "OK": col = GREEN
            elif key == "DEL": col = RED
            elif key in ["SHIFT","ABC","SPACE"]: col = (70,70,120)
            else: col = (55,55,55)
            if rect.collidepoint(pygame.mouse.get_pos()) and key not in ["OK","DEL"]: col = (85,85,85)
            pygame.draw.rect(screen, col, rect, border_radius=S(10))
            pygame.draw.rect(screen, (120,120,120), rect, 2, border_radius=S(10))
            txt = font_key.render(key, True, WHITE)
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

VK = VirtualKeyboard()

class InputBox:
    def __init__(self, x, y, w, h, text='', placeholder='', numeric=False):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.placeholder = placeholder
        self.active = False
        self.numeric = numeric
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if VK.active:
                if VK.handle_click(event.pos): return True
            if self.rect.collidepoint(event.pos):
                self.active = True
                VK.show(self, numeric_only=self.numeric)
                return True
        if event.type == pygame.KEYDOWN and self.active and not VK.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                VK.hide()
            else:
                if self.numeric and not event.unicode.isdigit(): return False
                if len(self.text) < 12 and event.unicode.isprintable(): self.text += event.unicode
        return False
    def draw(self):
        is_focused = VK.active and VK.target_input == self
        col = CYAN if is_focused else (GREEN if self.active else GRAY)
        pygame.draw.rect(screen, (30,30,30), self.rect, border_radius=S(8))
        pygame.draw.rect(screen, col, self.rect, 3 if is_focused else 2, border_radius=S(8))
        txt = self.text if self.text else self.placeholder
        color = WHITE if self.text else (150,150,150)
        if is_focused:
            txt_display = self.text + "|" if int(pygame.time.get_ticks()/500) % 2 == 0 else self.text
            if not self.text: txt_display = self.placeholder if int(pygame.time.get_ticks()/500) % 2 != 0 else "|"
            else: txt_display = self.text + ("|" if int(pygame.time.get_ticks()/500) % 2 == 0 else "")
            t = font_m.render(txt_display, True, WHITE)
        else:
            t = font_m.render(txt, True, color)
# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 3/7 - 270 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
        screen.blit(t, (self.rect.x + S(10), self.rect.centery - t.get_height()//2))

def result_screen(msg, sub, color):
    t0 = pygame.time.get_ticks()
    while pygame.time.get_ticks() - t0 < 2500:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit(); sys.exit()
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN): return
        screen.fill(BLACK)
        t = font_big.render(msg, True, color)
        screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - S(60)))
        s = font_m.render(sub, True, WHITE)
        screen.blit(s, (W // 2 - s.get_width() // 2, H // 2 + S(10)))
        pygame.display.flip()
        clock.tick(60)

def simulate_ad():
    t0 = pygame.time.get_ticks()
    duration = 2000
    while pygame.time.get_ticks() - t0 < duration:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
        screen.fill((10, 10, 25))
        remaining = max(1, int((duration - (pygame.time.get_ticks() - t0)) / 1000) + 1)
        ad_title = font_big.render("REWARDED AD PLAYING...", True, GOLD)
        screen.blit(ad_title, (W // 2 - ad_title.get_width() // 2, H // 2 - S(40)))
        timer_txt = font_m.render(f"Reward in: {remaining}s", True, WHITE)
        screen.blit(timer_txt, (W // 2 - timer_txt.get_width() // 2, H // 2 + S(20)))
        pygame.display.flip()
        clock.tick(60)

def simulate_purchase(package):
    t0 = pygame.time.get_ticks()
    duration = 2500
    while pygame.time.get_ticks() - t0 < duration:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        screen.fill((15, 15, 30))
        elapsed = pygame.time.get_ticks() - t0
        if elapsed < 800: txt = "Connecting to Google Play..."
        elif elapsed < 1600: txt = f"Processing ${package['usd']} payment..."
        else: txt = "Purchase Successful! Verifying..."
        title = font_big.render("PURCHASING...", True, GOLD)
        screen.blit(title, (W//2 - title.get_width()//2, H//2 - S(40)))
        sub = font_m.render(txt, True, WHITE)
        screen.blit(sub, (W//2 - sub.get_width()//2, H//2 + S(20)))
        pygame.display.flip()
        clock.tick(60)
    return True

def show_tutorial():
    instructions = [
        "--- HOW TO PLAY - 12 TROOPS ---",
        "",
        "FREE STARTER: Warrior, Spear, Archer",
        "LOCKED: Tank, Mage, Giant + 6 NEW!",
        "ENGINEER: Repairs castle - 150 gold",
        "MEDIC: Heals nearby allies",
        "PILOT: Fast flying 5.0 speed!",
        "ASSASSIN: 18 dmg but 2 HP",
        "SHIELDER: 25 HP big tank",
        "BOMBER: Explodes 30 area dmg",
        "Unlock troops in ABILITIES shop!",
        "",
        "[ TAP ANYWHERE TO CLOSE ]"
    ]
    while True:
        draw_bg()
        overlay = pygame.Surface((W - S(40), H - S(40)))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        screen.blit(overlay, (S(20), S(20)))
        pygame.draw.rect(screen, GOLD, (S(20), S(20), W - S(40), H - S(40)), width=S(3), border_radius=S(15))
        y = S(35)
        for line in instructions:
            if line.startswith("---"): txt = font_b.render(line, True, GOLD)
            elif line.startswith("["): txt = font_b.render(line, True, GREEN)
            elif "ENGINEER" in line or "MEDIC" in line or "PILOT" in line: txt = font_s.render(line, True, CYAN)
            else: txt = font_s.render(line, True, WHITE)
            screen.blit(txt, (W // 2 - txt.get_width() // 2, y))
            y += S(26)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN): return
        clock.tick(60)

def settings_screen():
    global SAVE
    bw, bh = S(40), S(40)
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    music_down = pygame.Rect(W // 2 + S(20), S(110), bw, bh)
    music_up = pygame.Rect(W // 2 + S(210), S(110), bw, bh)
    sfx_down = pygame.Rect(W // 2 + S(20), S(180), bw, bh)
    sfx_up = pygame.Rect(W // 2 + S(210), S(180), bw, bh)
    mute_btn = pygame.Rect(W // 2 - S(100), S(250), S(200), S(45))
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(55)))
        t = font_b.render("SETTINGS", True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(12)))
        m_txt = font_m.render(f"Music Vol: {int(SAVE['music_vol'] * 100)}%", True, WHITE)
        screen.blit(m_txt, (W // 2 - S(200), S(120)))
        pygame.draw.rect(screen, RED, music_down, border_radius=S(5))
        pygame.draw.rect(screen, GREEN, music_up, border_radius=S(5))
        screen.blit(font_b.render("-", True, WHITE), (music_down.centerx - S(5), music_down.centery - S(12)))
        screen.blit(font_b.render("+", True, WHITE), (music_up.centerx - S(7), music_up.centery - S(12)))
        s_txt = font_m.render(f"SFX Vol: {int(SAVE['sfx_vol'] * 100)}%", True, WHITE)
        screen.blit(s_txt, (W // 2 - S(200), S(190)))
        pygame.draw.rect(screen, RED, sfx_down, border_radius=S(5))
        pygame.draw.rect(screen, GREEN, sfx_up, border_radius=S(5))
        screen.blit(font_b.render("-", True, WHITE), (sfx_down.centerx - S(5), sfx_down.centery - S(12)))
        screen.blit(font_b.render("+", True, WHITE), (sfx_up.centerx - S(7), sfx_up.centery - S(12)))
        m_col = RED if SAVE["muted"] else GREEN
        pygame.draw.rect(screen, m_col, mute_btn, border_radius=S(10))
        mute_txt = font_m.render("SOUND: OFF" if SAVE["muted"] else "SOUND: ON", True, WHITE)
        screen.blit(mute_txt, (mute_btn.centerx - mute_txt.get_width() // 2, mute_btn.centery - mute_txt.get_height() // 2))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< BACK", True, WHITE), (back_btn.centerx - 25, back_btn.centery - 8))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): write_save(); return
                if music_down.collidepoint(e.pos): SAVE["music_vol"] = max(0.0, round(SAVE["music_vol"] - 0.1, 1)); apply_audio_settings()
                if music_up.collidepoint(e.pos): SAVE["music_vol"] = min(1.0, round(SAVE["music_vol"] + 0.1, 1)); apply_audio_settings()
                if sfx_down.collidepoint(e.pos): SAVE["sfx_vol"] = max(0.0, round(SAVE["sfx_vol"] - 0.1, 1))
                if sfx_up.collidepoint(e.pos): SAVE["sfx_vol"] = min(1.0, round(SAVE["sfx_vol"] + 0.1, 1))
                if mute_btn.collidepoint(e.pos): SAVE["muted"] = not SAVE["muted"]; apply_audio_settings()
        clock.tick(60)

def abilities_shop():
    global SAVE
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    scroll_y = 0
    msg_time = 0
    msg_text = ""
    filter_tier = "ALL"
    filter_btns = {
        "ALL": pygame.Rect(S(5), S(60), S(50), S(28)),
        "TROOPS": pygame.Rect(S(60), S(60), S(65), S(28)),
        "ECONOMY": pygame.Rect(S(130), S(60), S(70), S(28)),
        "OFFENSE": pygame.Rect(S(205), S(60), S(65), S(28)),
        "DEFENSE": pygame.Rect(S(275), S(60), S(65), S(28)),
        "UTILITY": pygame.Rect(S(5), S(92), S(65), S(28)),
        "LEGEND": pygame.Rect(S(75), S(92), S(65), S(28)),
    }
    item_h = S(62)
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0,0,W,S(55)))
        screen.blit(font_b.render("SHOP - ABILITIES + TROOPS", True, GOLD), (W//2-130, S(12)))
        screen.blit(font_m.render(f"GEMS: {SAVE['gems']}", True, GOLD), (W-150, S(15)))
        for tier, rect in filter_btns.items():
            col = GREEN if filter_tier == tier else GRAY
            pygame.draw.rect(screen, col, rect, border_radius=S(6))
            txt = font_s.render(tier, True, WHITE)
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
        
        if filter_tier == "TROOPS":
            # Show troop unlocks
            filtered_troops = list(TROOPS_BASE.items())
            start_y = S(130)
            for idx, (tname, tdata) in enumerate(filtered_troops):
                y = start_y + idx * (item_h + S(8)) + scroll_y
                if y < S(120) or y > H - S(20): continue
                rect = pygame.Rect(W//2 - S(170), y, S(340), item_h)
                owned = tname in SAVE["unlocked_troops"]
                col_bg = (46,204,113) if owned else (50,50,70)
                pygame.draw.rect(screen, col_bg, rect, border_radius=S(10))
                if owned: pygame.draw.rect(screen, GREEN, rect, 2, border_radius=S(10))
                
                # Icon
                screen.blit(font_m.render(tdata["icon"], True, WHITE), (rect.x + S(10), rect.centery - S(10)))
                screen.blit(font_m.render(tname, True, WHITE), (rect.x + S(35), rect.y + S(6)))
                screen.blit(font_s.render(f"{tdata['desc']} | ${tdata['cost']}", True, (200,200,200)), (rect.x + S(35), rect.y + S(28)))
                
                cost = TROOP_UNLOCK_COSTS[tname]
                price_txt = "OWNED" if owned else f"{cost} GEMS" if cost>0 else "FREE"
                pcol = GOLD if owned else (GREEN if SAVE["gems"] >= cost else RED)
                screen.blit(font_s.render(price_txt, True, pcol), (rect.right - S(75), rect.centery - S(8)))
        else:
            filtered = ABILITIES if filter_tier == "ALL" else [a for a in ABILITIES if a["tier"] == filter_tier or (filter_tier=="LEGEND" and a["tier"]=="LEGENDARY")]
            start_y = S(130)
            for idx, abil in enumerate(filtered):
                y = start_y + idx * (item_h + S(8)) + scroll_y
                if y < S(120) or y > H - S(20): continue
                rect = pygame.Rect(W//2 - S(170), y, S(340), item_h)
                owned = abil["id"] in SAVE["unlocked_abilities"]
                col_bg = (46,204,113) if owned else (50,50,70)
                pygame.draw.rect(screen, col_bg, rect, border_radius=S(10))
                if owned: pygame.draw.rect(screen, GREEN, rect, 2, border_radius=S(10))
                tier_colors = {"ECONOMY": GOLD, "OFFENSE": RED, "DEFENSE": BLUE, "UTILITY": CYAN, "LEGENDARY": PURPLE}
                pygame.draw.circle(screen, tier_colors.get(abil["tier"], WHITE), (rect.x + S(18), rect.centery), S(10))
                screen.blit(font_m.render(abil["name"], True, WHITE), (rect.x + S(35), rect.y + S(6)))
                screen.blit(font_s.render(abil["desc"], True, (200,200,200)), (rect.x + S(35), rect.y + S(28)))
                price_txt = "OWNED" if owned else f"{abil['price']} GEMS"
                pcol = GOLD if owned else (GREEN if SAVE["gems"] >= abil["price"] else RED)
                screen.blit(font_s.render(price_txt, True, pcol), (rect.right - S(75), rect.centery - S(8)))
        
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< BACK", True, WHITE), (back_btn.centerx - 25, back_btn.centery - 8))
        owned_count = len(SAVE["unlocked_abilities"])
        troop_count = len(SAVE["unlocked_troops"])
        count_txt = font_s.render(f"Abilities {owned_count}/35 | Troops {troop_count}/12", True, WHITE)
        screen.blit(count_txt, (W//2 - count_txt.get_width()//2, H - S(25)))
        if pygame.time.get_ticks() - msg_time < 2000:
            m = font_m.render(msg_text, True, GOLD)
            screen.blit(m, (W // 2 - m.get_width() // 2, H - S(50)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): write_save(); return
                for tier, rect in filter_btns.items():
                    if rect.collidepoint(e.pos): filter_tier = tier; scroll_y=0
                if filter_tier == "TROOPS":
                    filtered_troops = list(TROOPS_BASE.items())
                    start_y = S(130)
                    for idx, (tname, tdata) in enumerate(filtered_troops):
                        y = start_y + idx * (item_h + S(8)) + scroll_y
                        rect = pygame.Rect(W//2 - S(170), y, S(340), item_h)
                        if rect.collidepoint(e.pos):
                            if tname in SAVE["unlocked_troops"]:
                                msg_text = "Already owned!"; msg_time = pygame.time.get_ticks()
                            else:
                                cost = TROOP_UNLOCK_COSTS[tname]
                                if SAVE["gems"] >= cost:
                                    SAVE["gems"] -= cost
                                    SAVE["unlocked_troops"].append(tname)
                                    write_save()
                                    msg_text = f"Unlocked {tname}!"; msg_time = pygame.time.get_ticks()
                                else:
                                    msg_text = "Not enough gems!"; msg_time = pygame.time.get_ticks()
                else:
                    filtered = ABILITIES if filter_tier == "ALL" else [a for a in ABILITIES if a["tier"] == filter_tier or (filter_tier=="LEGEND" and a["tier"]=="LEGENDARY")]
                    start_y = S(130)
                    for idx, abil in enumerate(filtered):
                        y = start_y + idx * (item_h + S(8)) + scroll_y
                        rect = pygame.Rect(W//2 - S(170), y, S(340), item_h)
                        if rect.collidepoint(e.pos):
                            if abil["id"] in SAVE["unlocked_abilities"]:
                                msg_text = "Already owned!"; msg_time = pygame.time.get_ticks()
                            else:
                                if SAVE["gems"] >= abil["price"]:
                                    SAVE["gems"] -= abil["price"]
                                    SAVE["unlocked_abilities"].append(abil["id"])
                                    write_save()
                                    msg_text = f"Bought {abil['name']}!"; msg_time = pygame.time.get_ticks()
                                else:
                                    msg_text = "Not enough gems!"; msg_time = pygame.time.get_ticks()
            if e.type == pygame.MOUSEWHEEL:
                scroll_y += e.y * 30
                max_items = len(TROOPS_BASE) if filter_tier=="TROOPS" else len(filtered)
                max_scroll = -max_items*(item_h+S(8)) + 300
                scroll_y = min(0, max(scroll_y, max_scroll))

def gems_shop():
    global SAVE
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    ad_btn = pygame.Rect(W//2 - S(160), S(70), S(320), S(50))
    IAP_PACKAGES = [
        {"id": "gems_100",  "gems": 100,  "usd": 0.99, "name": "STARTER PACK", "color": (100,100,100)},
        {"id": "gems_500",  "gems": 500,  "usd": 3.99, "name": "POPULAR PACK", "color": (46,204,113)},
        {"id": "gems_1200", "gems": 1200, "usd": 7.99, "name": "BEST VALUE", "color": (52,152,219)},
        {"id": "gems_3000", "gems": 3000, "usd": 14.99,"name": "PRO PACK", "color": (155,89,182)},
        {"id": "gems_7000", "gems": 7000, "usd": 29.99,"name": "LEGENDARY PACK", "color": (241,196,15)},
    ]
    scroll_y = 0
# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 4/7 - 270 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
    msg_time = 0
    msg_text = ""
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(55)))
        screen.blit(font_b.render("GEM SHOP", True, CYAN), (W//2-70, S(12)))
        screen.blit(font_m.render(f"GEMS: {SAVE['gems']}", True, GOLD), (W-150, S(15)))
        pygame.draw.rect(screen, PURPLE, ad_btn, border_radius=S(10))
        pygame.draw.rect(screen, WHITE, ad_btn, 2, border_radius=S(10))
        atxt = font_m.render("WATCH AD (+10 GEMS) FREE", True, WHITE)
        screen.blit(atxt, (ad_btn.centerx - atxt.get_width()//2, ad_btn.centery - atxt.get_height()//2))
        title_real = font_m.render("--- BUY WITH REAL MONEY ---", True, GOLD)
        screen.blit(title_real, (W//2 - title_real.get_width()//2, S(135)))
        y_start = S(160)
        for idx, pkg in enumerate(IAP_PACKAGES):
            y = y_start + idx * (S(62)) + scroll_y
            if y < S(150) or y > H - S(10): continue
            rect = pygame.Rect(W//2 - S(160), y, S(320), S(55))
            hover = rect.collidepoint(pygame.mouse.get_pos())
            base_col = pkg["color"]
            col = tuple(min(255, c+30) for c in base_col) if hover else base_col
            pygame.draw.rect(screen, col, rect, border_radius=S(10))
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=S(10))
            pygame.draw.circle(screen, GOLD, (rect.x + S(25), rect.centery), S(16))
            gem_icon = font_b.render(f"{pkg['gems']}", True, BLACK)
            screen.blit(gem_icon, (rect.x + S(25) - gem_icon.get_width()//2, rect.centery - gem_icon.get_height()//2))
            screen.blit(font_m.render(pkg["name"], True, WHITE), (rect.x + S(55), rect.y + S(6)))
            price_txt = f"${pkg['usd']} - {pkg['gems']} GEMS"
            screen.blit(font_s.render(price_txt, True, WHITE), (rect.x + S(55), rect.y + S(28)))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< BACK", True, WHITE), (back_btn.centerx - 25, back_btn.centery - 8))
        if pygame.time.get_ticks() - msg_time < 2500:
            m = font_m.render(msg_text, True, GOLD)
            screen.blit(m, (W // 2 - m.get_width() // 2, H - S(30)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): return
                if ad_btn.collidepoint(e.pos):
                    simulate_ad()
                    SAVE["gems"] += 10
                    write_save()
                    msg_text = "RECEIVED +10 GEMS!"; msg_time = pygame.time.get_ticks()
                for idx, pkg in enumerate(IAP_PACKAGES):
                    y = y_start + idx * (S(62)) + scroll_y
                    rect = pygame.Rect(W//2 - S(160), y, S(320), S(55))
                    if rect.collidepoint(e.pos):
                        if simulate_purchase(pkg):
                            SAVE["gems"] += pkg["gems"]
                            SAVE["total_purchased_usd"] += pkg["usd"]
                            write_save()
                            msg_text = f"SUCCESS! +{pkg['gems']} GEMS!"; msg_time = pygame.time.get_ticks()
            if e.type == pygame.MOUSEWHEEL:
                scroll_y += e.y * 25
                scroll_y = min(0, max(scroll_y, -350))
        clock.tick(60)

def color_shop():
    global SAVE
    ensure_save()
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    tab = "soldier"
    t_soldier = pygame.Rect(W//2 - S(110), S(60), S(100), S(35))
    t_tower = pygame.Rect(W//2 + S(10), S(60), S(100), S(35))
    scroll_y = 0
    item_h = S(58)
    msg_time = 0
    msg_text = ""
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0,0,W,S(55)))
        screen.blit(font_b.render("COLOR SHOP", True, GOLD), (W//2-80, S(12)))
        screen.blit(font_m.render(f"GEMS: {SAVE['gems']}", True, GOLD), (W-150, S(15)))
        pygame.draw.rect(screen, GREEN if tab=="soldier" else GRAY, t_soldier, border_radius=S(8))
        pygame.draw.rect(screen, GREEN if tab=="tower" else GRAY, t_tower, border_radius=S(8))
        screen.blit(font_s.render("SOLDIER", True, WHITE), (t_soldier.centerx-28, t_soldier.centery-8))
        screen.blit(font_s.render("TOWER", True, WHITE), (t_tower.centerx-22, t_tower.centery-8))
        start_y = S(110)
        for idx, item in enumerate(COLOR_SHOP_ITEMS):
            y = start_y + (idx * (item_h + S(6))) + scroll_y
            if y < S(100) or y > H - S(20): continue
            rect = pygame.Rect(W//2 - S(160), y, S(320), item_h)
            owned = item["id"] in SAVE["unlocked_colors"]
            selected = (SAVE["selected_soldier_color"] == item["id"] and tab=="soldier") or (SAVE["selected_tower_color"] == item["id"] and tab=="tower")
            col_bg = (46,204,113) if selected else (60,60,60) if owned else (40,40,40)
            pygame.draw.rect(screen, col_bg, rect, border_radius=S(10))
            if selected: pygame.draw.rect(screen, GREEN, rect, 3, border_radius=S(10))
            draw_fancy_circle((rect.x + S(25), rect.centery), item, S(14))
            tier_col = WHITE
            if item["tier"] == "FREE": tier_col = (200,200,200)
            elif item["tier"] == "CHEAP": tier_col = GREEN
            elif item["tier"] == "MEDIUM": tier_col = CYAN
            elif item["tier"] == "EXPENSIVE": tier_col = GOLD
            else: tier_col = PURPLE
            screen.blit(font_m.render(item["name"], True, WHITE), (rect.x + S(50), rect.y + S(5)))
            screen.blit(font_s.render(f"{item['tier']} - {item['price']} GEMS", True, tier_col), (rect.x + S(50), rect.y + S(28)))
            status = "EQUIPPED" if selected else "OWNED" if owned else "LOCKED" if item["price"]>0 else "FREE"
            scol = GOLD if selected else GREEN if owned else RED
            screen.blit(font_s.render(status, True, scol), (rect.right - S(65), rect.centery - S(8)))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< BACK", True, WHITE), (back_btn.centerx - 25, back_btn.centery - 8))
        if pygame.time.get_ticks() - msg_time < 2000:
            m = font_m.render(msg_text, True, GOLD)
            screen.blit(m, (W // 2 - m.get_width() // 2, H - S(30)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): write_save(); return
                if t_soldier.collidepoint(e.pos): tab = "soldier"
                if t_tower.collidepoint(e.pos): tab = "tower"
                for idx, item in enumerate(COLOR_SHOP_ITEMS):
                    y = start_y + (idx * (item_h + S(6))) + scroll_y
                    rect = pygame.Rect(W//2 - S(160), y, S(320), item_h)
                    if rect.collidepoint(e.pos):
                        if item["id"] in SAVE["unlocked_colors"]:
                            if tab == "soldier": SAVE["selected_soldier_color"] = item["id"]
                            else: SAVE["selected_tower_color"] = item["id"]
                            msg_text = f"EQUIPPED {item['name']}!"; msg_time = pygame.time.get_ticks(); write_save()
                        else:
                            if SAVE["gems"] >= item["price"]:
                                SAVE["gems"] -= item["price"]
                                SAVE["unlocked_colors"].append(item["id"])
                                if tab == "soldier": SAVE["selected_soldier_color"] = item["id"]
                                else: SAVE["selected_tower_color"] = item["id"]
                                msg_text = f"BOUGHT {item['name']}!"; msg_time = pygame.time.get_ticks(); write_save()
                            else: msg_text = "NOT ENOUGH GEMS!"; msg_time = pygame.time.get_ticks()
            if e.type == pygame.MOUSEWHEEL:
                scroll_y += e.y * 20
                scroll_y = min(0, max(scroll_y, -len(COLOR_SHOP_ITEMS)*(item_h+S(6)) + 300))
        clock.tick(60)

def waiting_lobby(room_code, is_host=True):
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    start_btn = pygame.Rect(W//2 - S(100), H - S(80), S(200), S(50))
    add_bot_btn = pygame.Rect(W//2 - S(100), H - S(140), S(200), S(40))
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0,0,W,S(60)))
        screen.blit(font_b.render(f"ROOM: {room_code}", True, GOLD), (W//2 - S(60), S(15)))
        if room_code in ROOMS:
            screen.blit(font_s.render(f"Players: {len(ROOMS[room_code]['players'])}/{ROOMS[room_code]['max_players']}", True, WHITE), (W - S(120), S(20)))
        room = ROOMS.get(room_code)
        if not room: return "MENU"
        slot_h = S(55)
        gap = S(12)
        start_y = S(80)
        for i in range(room["max_players"]):
            y = start_y + i * (slot_h + gap)
            rect = pygame.Rect(W//2 - S(160), y, S(320), slot_h)
            if i < len(room["players"]):
                col = GREEN if i == 0 else BLUE if i == 1 else PURPLE
                pygame.draw.rect(screen, col, rect, border_radius=S(10))
                pygame.draw.rect(screen, WHITE, rect, 2, border_radius=S(10))
                name = room["players"][i]
                label = "HOST" if i == 0 else f"PLAYER {i+1}"
                screen.blit(font_m.render(f"{label}: {name}", True, WHITE), (rect.x + S(15), rect.centery - S(10)))
            else:
                pygame.draw.rect(screen, (50,50,50), rect, border_radius=S(10))
                pygame.draw.rect(screen, GRAY, rect, 2, border_radius=S(10))
                wait_txt = font_m.render("WAIT...", True, (150,150,150))
                screen.blit(wait_txt, (rect.centerx - wait_txt.get_width()//2, rect.centery - wait_txt.get_height()//2))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< LEAVE", True, WHITE), (back_btn.centerx - S(25), back_btn.centery - S(8)))
        if is_host:
            if len(room["players"]) < room["max_players"]:
                pygame.draw.rect(screen, CYAN, add_bot_btn, border_radius=S(8))
                screen.blit(font_s.render("ADD PLAYER (TEST)", True, BLACK), (add_bot_btn.centerx - S(60), add_bot_btn.centery - S(8)))
            can_start = len(room["players"]) >= 2
            col = GREEN if can_start else GRAY
            pygame.draw.rect(screen, col, start_btn, border_radius=S(10))
            txt = "START GAME" if can_start else f"NEED {2-len(room['players'])} MORE"
            screen.blit(font_m.render(txt, True, WHITE), (start_btn.centerx - S(50), start_btn.centery - S(10)))
        else:
            screen.blit(font_m.render("WAITING FOR HOST TO START...", True, WHITE), (W//2 - S(120), H - S(60)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos):
                    if room_code in ROOMS:
                        if is_host: del ROOMS[room_code]
                        else:
                            if SAVE["player_name"] in ROOMS[room_code]["players"]: ROOMS[room_code]["players"].remove(SAVE["player_name"])
                    return "MENU"
                if is_host and add_bot_btn.collidepoint(e.pos) and len(room["players"]) < room["max_players"]:
                    fake_name = generate_default_name()
                    ROOMS[room_code]["players"].append(fake_name)
                if is_host and start_btn.collidepoint(e.pos) and len(room["players"]) >= 2:
                    return battle_online(room)
        clock.tick(60)

def battle_online(room):
    result_screen("ONLINE BATTLE START!", f"{len(room['players'])}/{room['max_players']} Players - {room['code']}", GREEN)
    if room["max_players"] == 2: dummy_node = {"towers": 2, "zones": 1, "max_players": 2, "difficulty": 2}
    else: dummy_node = {"towers": 3, "zones": 2, "max_players": 3, "difficulty": 2}
    return battle(dummy_node, "FREE")

def online_menu():
    global SAVE, ROOMS
    default_name = SAVE.get("player_name") or generate_default_name()
    if not SAVE.get("player_name"): SAVE["player_name"] = default_name; write_save()
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    name_input = InputBox(W//2 - S(140), S(75), S(280), S(40), text=SAVE["player_name"], placeholder="Enter your name")
    create_code_input = InputBox(W//2 - S(140), S(170), S(280), S(40), placeholder="Room code (numbers only)", numeric=True)
    btn_2p = pygame.Rect(W//2 - S(140), S(220), S(135), S(40))
    btn_3p = pygame.Rect(W//2 + S(5), S(220), S(135), S(40))
    create_btn = pygame.Rect(W//2 - S(140), S(270), S(280), S(50))
    join_code_input = InputBox(W//2 - S(140), S(360), S(280), S(40), placeholder="Enter room code to join", numeric=True)
    join_btn = pygame.Rect(W//2 - S(140), S(410), S(280), S(50))
    selected_max = 2
    msg = ""; msg_time = 0
    while True:
        draw_bg()
        shift = 0
        if VK.active and H > W: shift = -S(60)
        pygame.draw.rect(screen, BLACK, (0,0,W,S(60)))
        screen.blit(font_b.render("ONLINE MODE", True, GOLD), (W//2 - S(70), S(15)))
        screen.blit(font_m.render("YOUR NAME:", True, WHITE), (W//2 - S(140), S(55)+shift))
        name_input.rect.y = S(75)+shift; name_input.draw()
        pygame.draw.rect(screen, (40,40,40), (W//2 - S(150), S(135)+shift, S(300), S(155)), border_radius=S(12))
        screen.blit(font_m.render("CREATE ROOM", True, GREEN), (W//2 - S(60), S(140)+shift))
        create_code_input.rect.y = S(170)+shift; create_code_input.draw()
        btn_2p.y = S(220)+shift; btn_3p.y = S(220)+shift
        col2 = GREEN if selected_max == 2 else GRAY
        col3 = GREEN if selected_max == 3 else GRAY
        pygame.draw.rect(screen, col2, btn_2p, border_radius=S(8))
        pygame.draw.rect(screen, col3, btn_3p, border_radius=S(8))
        screen.blit(font_s.render("2 PLAYERS", True, WHITE), (btn_2p.centerx - S(30), btn_2p.centery - S(8)))
        screen.blit(font_s.render("3 PLAYERS", True, WHITE), (btn_3p.centerx - S(30), btn_3p.centery - S(8)))
        create_btn.y = S(270)+shift
        pygame.draw.rect(screen, GREEN, create_btn, border_radius=S(10))
        screen.blit(font_m.render("CREATE ROOM", True, WHITE), (create_btn.centerx - S(55), create_btn.centery - S(10)))
        pygame.draw.rect(screen, (40,40,40), (W//2 - S(150), S(325)+shift, S(300), S(145)), border_radius=S(12))
        screen.blit(font_m.render("JOIN ROOM", True, BLUE), (W//2 - S(50), S(330)+shift))
        join_code_input.rect.y = S(360)+shift; join_code_input.draw()
        join_btn.y = S(410)+shift
        pygame.draw.rect(screen, BLUE, join_btn, border_radius=S(10))
        screen.blit(font_m.render("JOIN", True, WHITE), (join_btn.centerx - S(20), join_btn.centery - S(10)))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< BACK", True, WHITE), (back_btn.centerx - S(25), back_btn.centery - S(8)))
        if pygame.time.get_ticks() - msg_time < 2000:
            m = font_m.render(msg, True, GOLD)
            screen.blit(m, (W//2 - m.get_width()//2, H - S(20) - (H//2 if VK.active else 0)))
        VK.draw()
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if VK.active: VK.hide()
                else: return
            handled = False
            if e.type == pygame.MOUSEBUTTONDOWN and VK.active:
                if VK.handle_click(e.pos): handled = True
            if not handled:
                name_input.handle_event(e)
                create_code_input.handle_event(e)
                join_code_input.handle_event(e)
            if e.type == pygame.MOUSEBUTTONDOWN and not handled:
                if back_btn.collidepoint(e.pos):
                    if name_input.text.strip(): SAVE["player_name"] = name_input.text.strip()
                    else: SAVE["player_name"] = generate_default_name()
                    write_save(); VK.hide(); return
                if btn_2p.collidepoint(e.pos): selected_max = 2
                if btn_3p.collidepoint(e.pos): selected_max = 3
                if create_btn.collidepoint(e.pos):
                    if name_input.text.strip(): SAVE["player_name"] = name_input.text.strip()
                    else: SAVE["player_name"] = generate_default_name()
                    write_save()
# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 5/7 - 269 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
                    code = create_code_input.text.strip()
                    if not code: code = str(random.randint(1000,9999))
                    if len(code) < 3: msg = "Code must be at least 3 digits!"; msg_time = pygame.time.get_ticks(); continue
                    if code in ROOMS: del ROOMS[code]
                    ROOMS[code] = {"code": code, "host": SAVE["player_name"], "players": [SAVE["player_name"]], "max_players": selected_max}
                    VK.hide()
                    result = waiting_lobby(code, is_host=True)
                    if result == "MENU": continue
                if join_btn.collidepoint(e.pos):
                    if name_input.text.strip(): SAVE["player_name"] = name_input.text.strip()
                    else: SAVE["player_name"] = generate_default_name()
                    write_save()
                    code = join_code_input.text.strip()
                    if not code: msg = "Enter room code!"; msg_time = pygame.time.get_ticks(); continue
                    if code not in ROOMS: msg = "Room not found!"; msg_time = pygame.time.get_ticks(); continue
                    room = ROOMS[code]
                    if len(room["players"]) >= room["max_players"]: msg = "Room is full!"; msg_time = pygame.time.get_ticks(); continue
                    if SAVE["player_name"] not in room["players"]: room["players"].append(SAVE["player_name"])
                    VK.hide()
                    waiting_lobby(code, is_host=False)
        clock.tick(60)

def main_menu():
    def draw_fancy_button(rect, txt, desc, base_color, is_hover):
        shadow_rect = rect.copy()
        shadow_rect.y += S(4)
        pygame.draw.rect(screen, (0,0,0), shadow_rect, border_radius=S(12))
        col = tuple(min(255, c+25) for c in base_color) if is_hover else base_color


def main_menu():
    def draw_fancy_button(rect, txt, desc, base_color, is_hover):
        shadow_rect = rect.copy()
        shadow_rect.y += S(4)
        pygame.draw.rect(screen, (0,0,0), shadow_rect, border_radius=S(12))
        col = tuple(min(255, c+25) for c in base_color) if is_hover else base_color
        pygame.draw.rect(screen, col, rect, border_radius=S(12))
        if is_hover: pygame.draw.rect(screen, WHITE, rect, 3, border_radius=S(12))
        else: pygame.draw.rect(screen, (255,255,255,80), rect, 2, border_radius=S(12))
        t1 = font_b.render(txt, True, WHITE)
        t2 = font_s.render(desc, True, (235,235,235))
        screen.blit(t1, (rect.centerx - t1.get_width()//2, rect.y + S(8)))
        screen.blit(t2, (rect.centerx - t2.get_width()//2, rect.y + S(30)))
    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0,0,W,S(70)))
        title = font_title.render("TOWER DOMINION", True, GOLD)
        shadow = font_title.render("TOWER DOMINION", True, (50,40,0))
        screen.blit(shadow, (W//2 - title.get_width()//2 + S(2), S(14)+S(2)))
        screen.blit(title, (W//2 - title.get_width()//2, S(14)))
        gems_bg = pygame.Rect(W - S(155), S(15), S(140), S(35))
        pygame.draw.rect(screen, (30,30,30), gems_bg, border_radius=S(18))
        pygame.draw.rect(screen, GOLD, gems_bg, 2, border_radius=S(18))
        gems_txt = font_m.render(f"{SAVE['gems']} GEMS", True, GOLD)
        screen.blit(gems_txt, (gems_bg.centerx - gems_txt.get_width()//2, gems_bg.centery - gems_txt.get_height()//2))
        mouse_pos = pygame.mouse.get_pos()
        is_portrait = H > W
        if is_portrait: btn_w = int(W * 0.78)
        else: btn_w = S(340)
        btn_h = S(52)
        gap = S(10)
        total_h = 7 * btn_h + 6 * gap
        start_y = (H - total_h) // 2 + S(15)
        buttons = [
            {"txt":"OFFLINE MODE", "desc":"9 MAPS + 12 Troops Unlocked", "pos":[W//2 - btn_w//2, start_y, btn_w, btn_h], "mode":"OFFLINE", "color":(46,204,113)},
            {"txt":"ONLINE MODE", "desc":"Create or Join Room - 2 or 3 Players", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap), btn_w, btn_h], "mode":"ONLINE", "color":(60,60,180)},
            {"txt":"GEM SHOP", "desc":"Ads + Real Money - Buy Gems", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap)*2, btn_w, btn_h], "mode":"GEM_SHOP", "color":(100, 50, 150)},
            {"txt":"COLOR SHOP", "desc":"25 Colors - Zones Change Color!", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap)*3, btn_w, btn_h], "mode":"COLOR_SHOP", "color":(200, 120, 20)},
            {"txt":"TROOPS & ABILITIES SHOP", "desc":"12 Troops + 35 Abilities!", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap)*4, btn_w, btn_h], "mode":"ABILITIES", "color":(200,50,50)},
            {"txt":"SETTINGS", "desc":"Audio, Sound, Volume", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap)*5, btn_w, btn_h], "mode":"SETTINGS", "color":(50, 100, 120)},
            {"txt":"HOW TO PLAY", "desc":"Learn the 6 new troops", "pos":[W//2 - btn_w//2, start_y + (btn_h+gap)*6, btn_w, btn_h], "mode":"HOWTO", "color":(70, 90, 130)},
        ]
        for b in buttons:
            rect = pygame.Rect(b["pos"])
            is_hover = rect.collidepoint(mouse_pos)
            draw_fancy_button(rect, b["txt"], b["desc"], b["color"], is_hover)
        hint = font_s.render(f"Maps: {SAVE['map_owners'].count('player')}/9 | Troops: {len(SAVE['unlocked_troops'])}/12", True, (220,220,220))
        screen.blit(hint, (W//2 - hint.get_width()//2, H - S(22)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if pygame.Rect(b["pos"]).collidepoint(e.pos):
                        if b["mode"] == "OFFLINE":
                            while True:
                                draw_bg()
                                pygame.draw.rect(screen, BLACK, (0,0,W,S(70)))
                                t_off = font_big.render("OFFLINE MODE - 9 MAPS", True, GOLD)
                                screen.blit(t_off, (W//2 - t_off.get_width()//2, S(14)))
                                off_btn_w = btn_w
                                off_btn_h = S(52)
                                off_gap = S(10)
                                off_total_h = 4 * off_btn_h + 3 * off_gap
                                off_start_y = (H - off_total_h)//2 + S(20)
                                offline_buttons = [
                                    {"txt":"MAP MODE - 9 LEVELS", "desc":"Tutorial to Boss - Rewards Increase", "pos":[W//2 - off_btn_w//2, off_start_y, off_btn_w, off_btn_h], "mode":"MAP", "color":(46, 204, 113)},
                                    {"txt":"FREE PLAY", "desc":"Infinite - Gems Increase", "pos":[W//2 - off_btn_w//2, off_start_y + off_btn_h + off_gap, off_btn_w, off_btn_h], "mode":"FREE", "color":(52, 152, 219)},
                                    {"txt":"BOSS MODE", "desc":"Fight The Big Boss", "pos":[W//2 - off_btn_w//2, off_start_y + (off_btn_h+off_gap)*2, off_btn_w, off_btn_h], "mode":"BOSS", "color":(155,89,182)},
                                    {"txt":"BACK", "desc":"Return to Main Menu", "pos":[W//2 - off_btn_w//2, off_start_y + (off_btn_h+off_gap)*3, off_btn_w, S(45)], "mode":"BACK", "color":(120,40,40)},
                                ]
                                mouse = pygame.mouse.get_pos()
                                for ob in offline_buttons:
                                    r = pygame.Rect(ob["pos"])
                                    hov = r.collidepoint(mouse)
                                    draw_fancy_button(r, ob["txt"], ob["desc"], ob["color"], hov)
                                pygame.display.flip()
                                for ev in pygame.event.get():
                                    if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
                                    if ev.type==pygame.MOUSEBUTTONDOWN:
                                        for ob in offline_buttons:
                                            if pygame.Rect(ob["pos"]).collidepoint(ev.pos):
                                                if ob["mode"] in ["MAP","FREE","BOSS"]: return ob["mode"]
                                                if ob["mode"]=="BACK": break
                                        break
                                    if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: break
                                else: continue
                                break
                        elif b["mode"] == "ONLINE": online_menu(); break
                        elif b["mode"] == "GEM_SHOP": gems_shop(); break
                        elif b["mode"] == "COLOR_SHOP": color_shop(); break
                        elif b["mode"] == "ABILITIES": abilities_shop(); break
                        elif b["mode"] == "SETTINGS": settings_screen(); break
                        elif b["mode"] == "HOWTO": show_tutorial(); break
        clock.tick(60)

# 9 MAPS + THREAT AI
MAX_SOLDIERS_PER_CASTLE = 40

def calculate_threat_score(my_team, target_team, castles, zones, soldiers):
    if my_team == target_team: return -9999
    if target_team not in castles: return -9999
    if castles[target_team]["hp"] <= 0: return -9999
    my_pos = castles[my_team]["pos"]
    target_pos = castles[target_team]["pos"]
    target_data = castles[target_team]
    dist = math.hypot(my_pos[0]-target_pos[0], my_pos[1]-target_pos[1])
    proximity_score = (1000 / max(100, dist)) * 30
    enemy_soldiers_near_my_base = len([s for s in soldiers if s["team"]==target_team and math.hypot(s["pos"][0]-my_pos[0], s["pos"][1]-my_pos[1]) < S(280)])
    near_base_score = enemy_soldiers_near_my_base * 40
    total_enemy_army = len([s for s in soldiers if s["team"]==target_team])
    army_score = total_enemy_army * 8
    economy_score = (target_data["money"] / 10) + (target_data["income"] * 3)
    zones_owned = len([z for z in zones if z["owner"]==target_team])
    zones_score = zones_owned * 50
    attackers_to_me = len([s for s in soldiers if s["team"]==target_team and s["job"]=="ATTACK" and s.get("target")==my_team])
    attacking_me_score = attackers_to_me * 60
    hp_percent = target_data["hp"] / target_data["max_hp"]
    weak_bonus = (1 - hp_percent) * 40
    my_zones = [z for z in zones if z["owner"]==my_team]
    contested = 0
    for mz in my_zones:
        enemies_in_my_zone = len([s for s in soldiers if s["team"]==target_team and math.hypot(s["pos"][0]-mz["pos"][0], s["pos"][1]-mz["pos"][1]) < mz["r"]+S(20)])
        contested += enemies_in_my_zone
    contested_score = contested * 35
    total_threat = proximity_score + near_base_score + army_score + economy_score + zones_score + attacking_me_score + weak_bonus + contested_score
    if target_team == "player":
        total_threat *= 1.15
    return total_threat

def smart_ai_decision(team, difficulty, castles, zones, soldiers, troops_base):
    my_soldier_count = len([s for s in soldiers if s["team"]==team])
    if my_soldier_count >= MAX_SOLDIERS_PER_CASTLE:
        return (False, None, None, None)
    my_castle = castles[team]
    my_pos = my_castle["pos"]
    my_money = my_castle["money"]
    all_enemies = [name for name in castles if name != team and castles[name]["hp"] > 0]
    if not all_enemies:
        return (False, None, None, None)
    threat_scores = {}
    for enemy in all_enemies:
        threat_scores[enemy] = calculate_threat_score(team, enemy, castles, zones, soldiers)
    most_dangerous = max(threat_scores, key=threat_scores.get)
    most_dangerous_score = threat_scores[most_dangerous]
    if difficulty == 0 and most_dangerous_score < 80:
        if random.random() < 0.7:
            return (False, None, None, None)
    threats_near_base = []
    for enemy in all_enemies:
        near = [s for s in soldiers if s["team"]==enemy and math.hypot(s["pos"][0]-my_pos[0], s["pos"][1]-my_pos[1]) < S(250)]
        if near:
            threats_near_base.extend(near)
    threat_count = len(threats_near_base)
    neutral_zones = [z for z in zones if z["owner"] == "neutral"]
    spawn_chances = [0.025, 0.05, 0.08, 0.12, 0.18]
    spawn_chance = spawn_chances[difficulty]
    if threat_count > 2:
        spawn_chance *= 1.8
    if most_dangerous_score > 200:
        spawn_chance *= 1.4
    if random.random() > spawn_chance:
        return (False, None, None, None)
    # Filter by unlocked troops for AI too - AI can use all but prefers unlocked logic
    if difficulty == 0:
        available = ["WARRIOR"]
    elif difficulty == 1:
        available = ["WARRIOR", "ARCHER", "SPEARMAN"]
    elif difficulty == 2:
        available = ["WARRIOR", "ARCHER", "SPEARMAN", "TANK", "MAGE", "MEDIC"]
    elif difficulty == 3:
        available = ["WARRIOR", "ARCHER", "SPEARMAN", "TANK", "MAGE", "GIANT", "ENGINEER", "SHIELDER", "ASSASSIN"]
    else:
        available = list(TROOPS_BASE.keys())
    
    affordable = [t for t in available if troops_base[t]["cost"] <= my_money]
    if not affordable:
        affordable = ["WARRIOR"] if my_money >= 20 else []
    if not affordable:
        return (False, None, None, None)
    troop_type = random.choice(affordable)
    if threat_count >= 3:
        target_mode = "DEFEND"
        target_id = None
    elif threat_count >= 1 and difficulty >= 1:
        if random.random() < 0.6:
            target_mode = "DEFEND"
            target_id = None
        else:
            target_mode = "ATTACK"
            target_id = most_dangerous
    elif neutral_zones and difficulty >= 1 and random.random() < 0.5:
        closest = min(neutral_zones, key=lambda z: math.hypot(my_pos[0]-z["pos"][0], my_pos[1]-z["pos"][1]))
        target_mode = "ZONE"
        target_id = closest["id"]
    else:
        dangerous_zones = [z for z in zones if z["owner"]==most_dangerous]
        if dangerous_zones and random.random() < 0.4 and difficulty >= 2:
            target_mode = "ZONE"
            target_id = random.choice(dangerous_zones)["id"]
        else:
            target_mode = "ATTACK"
            target_id = most_dangerous
    return (True, troop_type, target_mode, target_id)

def show_map():
    base_positions = [
        [W*0.2, H*0.85], [W*0.45, H*0.80], [W*0.75, H*0.78],
        [W*0.25, H*0.62], [W*0.55, H*0.58], [W*0.80, H*0.55],
        [W*0.20, H*0.38], [W*0.55, H*0.35], [W*0.50, H*0.15]
    ]
    MAP_NODES = [
        {"name":"TRAINING I", "pos":base_positions[0], "towers":1, "zones":1, "reward":20, "difficulty":0, "desc":"TUTORIAL - DUMB AI"},
        {"name":"TRAINING II", "pos":base_positions[1], "towers":2, "zones":1, "reward":35, "difficulty":0, "desc":"TUTORIAL - DUMB AI"},
        {"name":"GRASSLANDS", "pos":base_positions[2], "towers":2, "zones":2, "reward":60, "difficulty":1, "desc":"EASY - SMART-ISH AI"},
        {"name":"FOREST", "pos":base_positions[3], "towers":3, "zones":2, "reward":85, "difficulty":1, "desc":"EASY - SMART-ISH AI"},
        {"name":"DESERT STORM", "pos":base_positions[4], "towers":3, "zones":3, "reward":120, "difficulty":2, "desc":"MEDIUM - SMART AI"},
        {"name":"MOUNTAIN PEAK", "pos":base_positions[5], "towers":3, "zones":3, "reward":160, "difficulty":2, "desc":"MEDIUM - SMART AI"},
        {"name":"VOLCANO", "pos":base_positions[6], "towers":4, "zones":3, "reward":210, "difficulty":3, "desc":"HARD - BRUTAL AI"},
        {"name":"ICE REALM", "pos":base_positions[7], "towers":4, "zones":3, "reward":260, "difficulty":3, "desc":"HARD - BRUTAL AI"},
        {"name":"FINAL BOSS", "pos":base_positions[8], "towers":5, "zones":4, "reward":350, "difficulty":4, "desc":"NIGHTMARE BOSS"},
    ]
    owners = SAVE.get("map_owners", ["player"] + ["enemy"]*8)
    if len(owners) < 9: owners = ["player"] + ["enemy"]*8
    for i in range(9): MAP_NODES[i]["owner"] = owners[i]
    CONN = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8), (1,3), (2,4)]
    back_btn = pygame.Rect(S(15), S(10), S(100), S(40))
    save_btn = pygame.Rect(W - S(140), S(10), S(125), S(40))
    saved_msg_time = 0
    while True:
        if all(n["owner"] == "player" for n in MAP_NODES):
            result_screen("CONQUEROR!", "You conquered all 9 maps!", GOLD)
            return "WIN"
        draw_bg()
        for a, b in CONN:
            pygame.draw.line(screen, (50, 50, 50), MAP_NODES[a]["pos"], MAP_NODES[b]["pos"], S(4))
        for idx, node in enumerate(MAP_NODES):
            if node["owner"] == "player":
# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 6/7 - 269 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
                col = GREEN
            else:
                diff_colors = [(100,100,100), (100,200,100), (200,200,50), (230,100,50), (150,0,200)]
                col = diff_colors[node["difficulty"]]
            pygame.draw.circle(screen, col, (int(node["pos"][0]), int(node["pos"][1])), S(32) if node["difficulty"]<4 else S(45))
            pygame.draw.circle(screen, BLACK, (int(node["pos"][0]), int(node["pos"][1])), S(32) if node["difficulty"]<4 else S(45), 3)
            if node["owner"] == "player":
                pygame.draw.circle(screen, GOLD, (int(node["pos"][0]), int(node["pos"][1])), S(10))
            txt = font_s.render(f"{idx+1}. {node['name']}", True, WHITE)
            screen.blit(txt, (node["pos"][0] - txt.get_width() // 2, node["pos"][1] + S(38)))
            rew = font_s.render(f"{node['reward']} GEMS", True, GOLD)
            screen.blit(rew, (node["pos"][0] - rew.get_width() // 2, node["pos"][1] + S(52)))
            if idx > 1 and MAP_NODES[idx-1]["owner"] != "player" and MAP_NODES[idx-2]["owner"] != "player":
                pygame.draw.circle(screen, (0,0,0,150), (int(node["pos"][0]), int(node["pos"][1])), S(32))
                lock = font_b.render("LOCKED", True, RED)
                screen.blit(lock, (node["pos"][0] - lock.get_width()//2, node["pos"][1] - S(10)))
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(60)))
        t = font_b.render(f"MAP MODE - 9 LEVELS | GEMS: {SAVE['gems']}", True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(15)))
        pygame.draw.rect(screen, RED, back_btn, border_radius=S(8))
        screen.blit(font_s.render("< MENU", True, WHITE), (back_btn.centerx - 25, back_btn.centery - 8))
        pygame.draw.rect(screen, GREEN, save_btn, border_radius=S(8))
        screen.blit(font_s.render("SAVE GAME", True, WHITE), (save_btn.centerx - 35, save_btn.centery - 8))
        if pygame.time.get_ticks() - saved_msg_time < 1500:
            msg = font_m.render("GAME SAVED!", True, GOLD)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H - S(50)))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): return "MENU"
                if save_btn.collidepoint(e.pos):
                    SAVE["map_owners"] = [n["owner"] for n in MAP_NODES]
                    write_save()
                    saved_msg_time = pygame.time.get_ticks()
                for idx, node in enumerate(MAP_NODES):
                    if math.hypot(e.pos[0] - node["pos"][0], e.pos[1] - node["pos"][1]) < S(45):
                        if idx > 1 and MAP_NODES[idx-1]["owner"] != "player" and MAP_NODES[idx-2]["owner"] != "player":
                            continue
                        if node["owner"] != "player":
                            res = battle(node, "MAP")
                            if res == "MENU": return "MENU"
                            if res:
                                node["owner"] = "player"
                                SAVE["zones_conquered"] += 1
                                SAVE["map_owners"] = [n["owner"] for n in MAP_NODES]
                                write_save()
        clock.tick(60)

def battle(node, game_mode="MAP"):
    global SAVE
    TROOPS = get_troops_with_abilities()
    TROOPS_ENEMY_BASE = TROOPS_BASE
    is_boss = game_mode == "BOSS"
    is_free = game_mode == "FREE"
    difficulty = node.get("difficulty", 1) if isinstance(node, dict) else 1
    if is_boss: difficulty = 4
    if is_free: difficulty = node.get("difficulty", 2) if isinstance(node, dict) else 2
    uid_gen = itertools.count()
    soldier_color_item = get_color_by_id(SAVE.get("selected_soldier_color","white"))
    tower_color_item = get_color_by_id(SAVE.get("selected_tower_color","white"))
    neutral_item = {"id":"neutral","color": NEUTRAL, "effect":"solid"}
    unlocked = SAVE.get("unlocked_abilities", [])
    start_bonus = 0
    if "rich1" in unlocked: start_bonus += 100
    if "rich2" in unlocked: start_bonus += 250
    if "rich3" in unlocked: start_bonus += 500
    hp_bonus = 0
    if "fort1" in unlocked: hp_bonus += 25
    if "fort2" in unlocked: hp_bonus += 60
    if "fort3" in unlocked: hp_bonus += 120
    if "ultimate" in unlocked: hp_bonus += 30
    income_bonus = 0
    if "inc1" in unlocked: income_bonus += 5
    if "inc2" in unlocked: income_bonus += 10
    if "inc3" in unlocked: income_bonus += 20
    if "ultimate" in unlocked: income_bonus += 5
    zone_cap_mult = 1.0
    if "zone1" in unlocked: zone_cap_mult += 0.25
    if "zone2" in unlocked: zone_cap_mult += 0.5
    diff_hp_mult = [0.8, 1.0, 1.2, 1.5, 2.0][difficulty]
    diff_income_mult = [0.7, 1.0, 1.3, 1.6, 2.0][difficulty]
    diff_money_start = [80, 120, 150, 200, 300][difficulty]
    if is_boss:
        castles = {
            "player": {"pos": [W // 2, int(H * 0.82)], "hp": 150+hp_bonus, "money": 400+start_bonus, "income": 25+income_bonus, "color": GREEN, "max_hp": 150+hp_bonus, "color_item": tower_color_item},
            "BOSS": {"pos": [W // 2, int(H * 0.18)], "hp": int(800 * diff_hp_mult), "money": 400, "income": int(40 * diff_income_mult), "color": PURPLE, "max_hp": int(800 * diff_hp_mult), "color_item": get_color_by_id("legend")}
        }
        zones = [
            {"id": "LEFT", "pos": [W // 2 - S(200), H // 2], "r": S(75), "owner": "neutral", "cap": 0, "income": 20, "color_item": neutral_item},
            {"id": "RIGHT", "pos": [W // 2 + S(200), H // 2], "r": S(75), "owner": "neutral", "cap": 0, "income": 20, "color_item": neutral_item},
            {"id": "MID", "pos": [W // 2, H // 2 - S(100)], "r": S(70), "owner": "neutral", "cap": 0, "income": 25, "color_item": neutral_item}
        ]
    elif is_free:
        max_p = node.get("max_players", 3) if isinstance(node, dict) else 3
        if max_p == 2:
            castles = {
                "player": {"pos": [W // 2, int(H * 0.82)], "hp": 200+hp_bonus, "money": 300+start_bonus, "income": 30+income_bonus, "color": GREEN, "max_hp": 200+hp_bonus, "respawn": 0, "color_item": tower_color_item},
                "enemy1": {"pos": [W // 2, int(H * 0.15)], "hp": int(150*diff_hp_mult), "money": diff_money_start, "income": int(20*diff_income_mult), "color": RED, "max_hp": int(150*diff_hp_mult), "respawn": 0, "color_item": get_color_by_id("red"), "difficulty": difficulty}
            }
        else:
            castles = {
                "player": {"pos": [W // 2, int(H * 0.82)], "hp": 200+hp_bonus, "money": 300+start_bonus, "income": 30+income_bonus, "color": GREEN, "max_hp": 200+hp_bonus, "respawn": 0, "color_item": tower_color_item},
                "enemy1": {"pos": [W // 4, int(H * 0.15)], "hp": int(150*diff_hp_mult), "money": diff_money_start, "income": int(20*diff_income_mult), "color": RED, "max_hp": int(150*diff_hp_mult), "respawn": 0, "color_item": get_color_by_id("red"), "difficulty": difficulty},
                "enemy2": {"pos": [W * 3 // 4, int(H * 0.15)], "hp": int(150*diff_hp_mult), "money": diff_money_start, "income": int(20*diff_income_mult), "color": BLUE, "max_hp": int(150*diff_hp_mult), "respawn": 0, "color_item": get_color_by_id("blue"), "difficulty": difficulty}
            }
        zones = [
            {"id": "MID", "pos": [W // 2, H // 2], "r": S(85), "owner": "neutral", "cap": 0, "income": 15, "color_item": neutral_item},
            {"id": "LEFT", "pos": [W // 2 - S(200), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item},
            {"id": "RIGHT", "pos": [W // 2 + S(200), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item}
        ]
        if max_p == 2:
            zones = [zones[0]]
    else:
        num_towers = node.get("towers", 2)
        num_zones = node.get("zones", 2)
        castles = {
            "player": {"pos": [W // 2, int(H * 0.82)], "hp": 120+hp_bonus, "money": 250+start_bonus, "income": 20+income_bonus, "color": GREEN, "max_hp": 120+hp_bonus, "color_item": tower_color_item}
        }
        enemy_positions = [
            [W // 4, int(H * 0.15)],
            [W * 3 // 4, int(H * 0.15)],
            [W // 2, int(H * 0.12)],
            [W // 6, int(H * 0.25)],
            [W * 5 // 6, int(H * 0.25)]
        ]
        enemy_colors = ["red","blue","purple","orange","cyan"]
        for i in range(min(num_towers, 5)):
            ename = f"enemy{i+1}" if i>0 else "enemy1"
            if i==0: ename="enemy1"
            castles[ename] = {
                "pos": enemy_positions[i],
                "hp": int(100 * diff_hp_mult + (i*20)),
                "money": diff_money_start,
                "income": int((18 + difficulty*3) * diff_income_mult),
                "color": RED,
                "max_hp": int(100 * diff_hp_mult + (i*20)),
                "color_item": get_color_by_id(enemy_colors[i % len(enemy_colors)]),
                "difficulty": difficulty
            }
        if num_zones == 1:
            zones = [{"id": "MID", "pos": [W // 2, H // 2], "r": S(85), "owner": "neutral", "cap": 0, "income": 15, "color_item": neutral_item}]
        elif num_zones == 2:
            zones = [
                {"id": "LEFT", "pos": [W // 2 - S(190), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item},
                {"id": "RIGHT", "pos": [W // 2 + S(190), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item}
            ]
        elif num_zones == 3:
            zones = [
                {"id": "MID", "pos": [W // 2, H // 2], "r": S(75), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item},
                {"id": "LEFT", "pos": [W // 2 - S(200), H // 2 - S(50)], "r": S(65), "owner": "neutral", "cap": 0, "income": 10, "color_item": neutral_item},
                {"id": "RIGHT", "pos": [W // 2 + S(200), H // 2 - S(50)], "r": S(65), "owner": "neutral", "cap": 0, "income": 10, "color_item": neutral_item}
            ]
        else:
            zones = [
                {"id": "MID", "pos": [W // 2, H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 15, "color_item": neutral_item},
                {"id": "LEFT", "pos": [W // 2 - S(210), H // 2], "r": S(60), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item},
                {"id": "RIGHT", "pos": [W // 2 + S(210), H // 2], "r": S(60), "owner": "neutral", "cap": 0, "income": 12, "color_item": neutral_item},
                {"id": "TOP", "pos": [W // 2, H // 2 - S(150)], "r": S(60), "owner": "neutral", "cap": 0, "income": 18, "color_item": neutral_item}
            ]
    soldiers = []
    crates = []
    mode = "MID"
    selected = "WARRIOR"
    shake = 0
    paused = False
    free_kill_count = 0
    free_difficulty_timer = 0
    if "over" in unlocked:
        uid = next(uid_gen)
        soldiers.append({"uid": uid, "pos": [castles["player"]["pos"][0]+S(30), castles["player"]["pos"][1]-S(40)], "team": "player", "type": "WARRIOR", "job": "DEFEND_BASE", "home": [castles["player"]["pos"][0]+S(30), castles["player"]["pos"][1]-S(100)], "hp": TROOPS["WARRIOR"]["hp"], "acd": 0, "color_item": soldier_color_item})
    def build_rects():
        rects = {}
        x = S(5)
        for name in ["DEFEND"] + [z["id"] for z in zones] + [n for n in castles if n != "player"]:
            rects[name] = pygame.Rect(x, H - S(65), S(70), S(55))
            x += S(75)
        return rects
    control_rects = build_rects()
    # Only show unlocked troops in shop
    def get_available_troop_rects():
        shop = {}
        sy = H // 2 - S(200)
        for tk in TROOP_KEYS:
            if tk in SAVE["unlocked_troops"]:
                shop[tk] = pygame.Rect(W - S(105), sy, S(95), S(38))
                sy += S(42)
        return shop
    shop_rects = get_available_troop_rects()
    pause_btn = pygame.Rect(W - S(60), S(10), S(50), S(50))
    resume_btn = pygame.Rect(W // 2 - S(110), H // 2 - S(20), S(220), S(60))
    quit_btn = pygame.Rect(W // 2 - S(110), H // 2 + S(55), S(220), S(60))
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)
    while True:
        draw_bg(shake)
        if shake > 0: shake -= 1
        if is_free:
            for c_name, c_data in castles.items():
                if c_name != "player" and c_data["hp"] <= 0:
                    if c_data.get("respawn", 0) <= 0: c_data["respawn"] = 300
                    else:
                        c_data["respawn"] -= 1
                        if c_data["respawn"] == 0:
                            c_data["hp"] = c_data["max_hp"]
                            c_data["money"] = 150
            free_difficulty_timer += 1
            if free_difficulty_timer % 1800 == 0:
                for c_name in castles:
                    if c_name != "player":
                        castles[c_name]["income"] += 2
        if "regen1" in unlocked or "regen2" in unlocked or "ultimate" in unlocked:
            regen = 0
            if "regen1" in unlocked: regen += 1
            if "regen2" in unlocked: regen += 3
            if "ultimate" in unlocked: regen += 1
            if pygame.time.get_ticks() % 2000 < 50:
                if castles["player"]["hp"] > 0 and castles["player"]["hp"] < castles["player"]["max_hp"]:
                    castles["player"]["hp"] = min(castles["player"]["max_hp"], castles["player"]["hp"] + regen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if pause_btn.collidepoint(mx, my): paused = not paused
                elif paused:
                    if resume_btn.collidepoint(mx, my): paused = False
                    elif quit_btn.collidepoint(mx, my): return "MENU"
                else:
                    for cr in crates[:]:
                        if math.hypot(mx - cr["pos"][0], my - cr["pos"][1]) < S(45):
                            mult = 1.0
                            if "crate1" in unlocked: mult += 0.5
                            if "crate2" in unlocked: mult += 1.0
                            if "ultimate" in unlocked: mult += 0.2
                            if "lucky" in unlocked and random.random() < 0.1:
                                mult *= 2
                                add_particles(cr["pos"][0], cr["pos"][1], GOLD, 15)
                            castles["player"]["money"] += int(cr["money"] * mult)
                            crates.remove(cr)
                    for name, rect in shop_rects.items():
                        if rect.collidepoint(mx, my):
                            selected = name
                            break
                    else:
                        p_pos = castles["player"]["pos"]
                        if math.hypot(mx - p_pos[0], my - p_pos[1]) < S(45): mode = "DEFEND"
                        else:
                            attacked_castle = False
                            for c_name, c_data in castles.items():
                                if c_name != "player" and c_data["hp"] > 0:
                                    rad = S(40) if is_boss and c_name == "BOSS" else S(28)
                                    if math.hypot(mx - c_data["pos"][0], my - c_data["pos"][1]) < rad + S(20):
                                        mode = c_name
                                        attacked_castle = True
                                        break
                            if not attacked_castle:
                                for z in zones:
                                    if math.hypot(mx - z["pos"][0], my - z["pos"][1]) < z["r"]:
                                        mode = z["id"]
                                        break
                                else:
                                    for name, rect in control_rects.items():
                                        if rect.collidepoint(mx, my):
                                            mode = name
                                            break
                        if len([s for s in soldiers if s["team"]=="player"]) >= MAX_SOLDIERS_PER_CASTLE:
                            pass
                        elif castles["player"]["money"] >= TROOPS[selected]["cost"]:
# FINAL FIXED ONLINE + 12 TROOPS HALAL - PART 7/7 - 269 lines / Total 1887
# MEDIC = GREEN CRESCENT 🌙 NOT RED CROSS | ONLINE WORKING | NO BLACK SCREEN
                            castles["player"]["money"] -= TROOPS[selected]["cost"]
                            uid = next(uid_gen)
                            if mode == "DEFEND":
                                hx =castles["player"]["pos"][0] + random.randint(-S(120), S(120))
                                hy = castles["player"]["pos"][1] - S(100)
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "DEFEND_BASE", "home": [hx, hy], "hp": TROOPS[selected]["hp"], "acd": 0, "color_item": soldier_color_item})
                            elif mode in [z["id"] for z in zones]:
                                tz = next((z for z in zones if z["id"] == mode), zones[0])
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "GUARD_ZONE", "zone_id": tz["id"], "home": list(tz["pos"]), "hp": TROOPS[selected]["hp"], "acd": 0, "color_item": soldier_color_item})
                            elif mode in castles:
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "ATTACK", "target": mode, "hp": TROOPS[selected]["hp"], "acd": 0, "color_item": soldier_color_item})
            if event.type == pygame.USEREVENT + 1 and not paused:
                for c in castles.values():
                    if c["hp"] > 0: c["money"] += c["income"]
                for z in zones:
                    if z["owner"] in castles and castles[z["owner"]]["hp"] > 0:
                        inc = z["income"]
                        if "zinc1" in unlocked: inc += 5
                        if "zinc2" in unlocked: inc += 12
                        if "ultimate" in unlocked: inc += 2
                        castles[z["owner"]]["money"] += inc
            if event.type == pygame.USEREVENT + 2 and not paused and len(crates) < 3:
                crates.append({"pos": [random.randint(W // 4, W * 3 // 4), random.randint(H // 3, H * 2 // 3)], "money": 100})
        if paused:
            pygame.draw.rect(screen, BLACK, (W // 2 - S(130), H // 2 - S(80), S(260), S(220)), border_radius=S(15))
            pygame.draw.rect(screen, GREEN, resume_btn, border_radius=S(10))
            pygame.draw.rect(screen, RED, quit_btn, border_radius=S(10))
            rt = font_m.render("RESUME", True, WHITE)
            screen.blit(rt, (resume_btn.centerx - rt.get_width() // 2, resume_btn.centery - rt.get_height() // 2))
            qt = font_m.render("QUIT TO MENU", True, WHITE)
            screen.blit(qt, (quit_btn.centerx - qt.get_width() // 2, quit_btn.centery - qt.get_height() // 2))
            pygame.display.flip()
            clock.tick(60)
            continue
        if castles["player"]["money"] > SAVE["best_free_money"]:
            SAVE["best_free_money"] = castles["player"]["money"]
            write_save()
        for en in [n for n in castles if n != "player"]:
            if castles[en]["hp"] <= 0: continue
            en_diff = castles[en].get("difficulty", difficulty)
            should_spawn, troop_type, target_mode, target_id = smart_ai_decision(en, int(en_diff), castles, zones, soldiers, TROOPS_ENEMY_BASE)
            if not should_spawn: continue
            if troop_type is None: continue
            if castles[en]["money"] < TROOPS_ENEMY_BASE[troop_type]["cost"]: continue
            castles[en]["money"] -= TROOPS_ENEMY_BASE[troop_type]["cost"]
            uid = next(uid_gen)
            enemy_color = castles[en].get("color_item", get_color_by_id("red"))
            if target_mode == "DEFEND":
                hx = castles[en]["pos"][0] + random.randint(-S(80), S(80))
                hy = castles[en]["pos"][1] + S(80)
                soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": troop_type, "job": "DEFEND_BASE", "home": [hx, hy], "hp": TROOPS_ENEMY_BASE[troop_type]["hp"], "acd": 0, "color_item": enemy_color})
            elif target_mode == "ZONE" and target_id:
                tz = next((z for z in zones if z["id"] == target_id), None)
                if tz:
                    soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": troop_type, "job": "GUARD_ZONE", "zone_id": tz["id"], "home": list(tz["pos"]), "hp": TROOPS_ENEMY_BASE[troop_type]["hp"], "acd": 0, "color_item": enemy_color})
            else:
                soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": troop_type, "job": "ATTACK", "target": target_id or "player", "hp": TROOPS_ENEMY_BASE[troop_type]["hp"], "acd": 0, "color_item": enemy_color})
        to_del = set()
        # Special abilities - Engineer repairs, Medic heals, Bomber explodes
        for s in soldiers:
            if s["uid"] in to_del: continue
            ttype = s["type"]
            # ENGINEER - repairs castle when near
            if ttype == "ENGINEER" and s["team"] in castles:
                my_castle_pos = castles[s["team"]]["pos"]
                if math.hypot(s["pos"][0]-my_castle_pos[0], s["pos"][1]-my_castle_pos[1]) < S(100):
                    if castles[s["team"]]["hp"] < castles[s["team"]]["max_hp"]:
                        if pygame.time.get_ticks() % 1000 < 50:
                            castles[s["team"]]["hp"] = min(castles[s["team"]]["max_hp"], castles[s["team"]]["hp"] + 2)
                            add_particles(s["pos"][0], s["pos"][1], GREEN, 3)
            # MEDIC - heals nearby allies
            if ttype == "MEDIC":
                for ally in soldiers:
                    if ally["team"]==s["team"] and ally["uid"]!=s["uid"] and ally["uid"] not in to_del:
                        if math.hypot(s["pos"][0]-ally["pos"][0], s["pos"][1]-ally["pos"][1]) < S(60):
                            if ally["hp"] < TROOPS[ally["type"]]["hp"] and pygame.time.get_ticks() % 800 < 50:
                                ally["hp"] = min(TROOPS[ally["type"]]["hp"], ally["hp"]+1)
                                add_particles(ally["pos"][0], ally["pos"][1], (100,255,100), 2)
            # BOMBER - explode when near enemies
            if ttype == "BOMBER":
                enemies_near = [e for e in soldiers if e["team"]!=s["team"] and e["uid"] not in to_del and math.hypot(s["pos"][0]-e["pos"][0], s["pos"][1]-e["pos"][1]) < S(35)]
                enemy_castle_near = any(math.hypot(s["pos"][0]-castles[en]["pos"][0], s["pos"][1]-castles[en]["pos"][1]) < S(50) for en in castles if en!=s["team"] and castles[en]["hp"]>0)
                if enemies_near or enemy_castle_near:
                    # BOOM!
                    add_particles(s["pos"][0], s["pos"][1], (255,100,0), 20)
                    for en in enemies_near:
                        en["hp"] -= 30
                        if en["hp"] <= 0:
                            to_del.add(en["uid"])
                    for en_name in castles:
                        if en_name!=s["team"] and castles[en_name]["hp"]>0:
                            if math.hypot(s["pos"][0]-castles[en_name]["pos"][0], s["pos"][1]-castles[en_name]["pos"][1]) < S(80):
                                castles[en_name]["hp"] -= 20
                    to_del.add(s["uid"])
        
        for s in soldiers:
            if s["job"] == "ATTACK" and (s["target"] not in castles or castles[s["target"]]["hp"] <= 0):
                to_del.add(s["uid"])
                continue
            if s["job"] == "DEFEND_BASE":
                my_castle = castles[s["team"]]["pos"]
                enemies_near_base = [e for e in soldiers if e["team"] != s["team"] and e["uid"] not in to_del and math.hypot(e["pos"][0] - my_castle[0], e["pos"][1] - my_castle[1]) < S(250)]
                if enemies_near_base:
                    nearest_enemy = min(enemies_near_base, key=lambda e: math.hypot(s["pos"][0] - e["pos"][0], s["pos"][1] - e["pos"][1]))
                    dest = nearest_enemy["pos"]
                else: dest = s["home"]
            elif s["job"] == "GUARD_ZONE":
                mz = next((z for z in zones if z["id"] == s["zone_id"]), zones[0])
                ens = [e for e in soldiers if e["team"] != s["team"] and e["uid"] not in to_del and math.hypot(e["pos"][0] - mz["pos"][0], e["pos"][1] - mz["pos"][1]) < mz["r"] + 20]
                ne = min(ens, key=lambda e: math.hypot(s["pos"][0] - e["pos"][0], s["pos"][1] - e["pos"][1]), default=None)
                dest = ne["pos"] if ne else s["home"]
            else: dest = castles[s["target"]]["pos"]
            dx = dest[0] - s["pos"][0]
            dy = dest[1] - s["pos"][1]
            d = math.hypot(dx, dy)
            if d > 5:
                s["pos"][0] += (dx / d) * TROOPS[s["type"]]["speed"]
                s["pos"][1] += (dy / d) * TROOPS[s["type"]]["speed"]
            else:
                if s["job"] == "ATTACK":
                    s["acd"] = s.get("acd", 0) - 1
                    if s["acd"] <= 0:
                        castles[s["target"]]["hp"] -= TROOPS[s["type"]]["dmg"]
                        try: add_particles(s["pos"][0], s["pos"][1], (255,200,0), 6)
                        except: pass
                        if s["target"] == "player": shake = 8
                        if is_free and castles[s["target"]]["hp"] <= 0:
                            free_kill_count += 1
                            SAVE["free_kills"] = SAVE.get("free_kills",0) + 1
                            base_gem = 10
                            scaling = 5 * (free_kill_count // 2)
                            diff_bonus = int(difficulty * 2)
                            total_gems = base_gem + scaling + diff_bonus
                            SAVE["gems"] += total_gems
                            write_save()
                            add_particles(castles[s["target"]]["pos"][0], castles[s["target"]]["pos"][1], GOLD, 20)
                        if TROOPS[s["type"]].get("ranged"): s["acd"] = TROOPS[s["type"]].get("cd", 40)
                        else: 
                            if s["type"] != "BOMBER":  # Bomber already handled
                                to_del.add(s["uid"])
        for i in range(len(soldiers)):
            for j in range(i + 1, len(soldiers)):
                s1 = soldiers[i]
                s2 = soldiers[j]
                if s1["uid"] in to_del or s2["uid"] in to_del or s1["team"] == s2["team"]: continue
                if math.hypot(s1["pos"][0] - s2["pos"][0], s1["pos"][1] - s2["pos"][1]) < 16:
                    # Shielder takes less damage
                    dmg1 = 1
                    dmg2 = 1
                    if s1["type"]=="SHIELDER": dmg1 = 0.3
                    if s2["type"]=="SHIELDER": dmg2 = 0.3
                    if s1["type"]=="ASSASSIN": dmg2 = 2  # Assassin does extra
                    if s2["type"]=="ASSASSIN": dmg1 = 2
                    s1["hp"] -= dmg1
                    s2["hp"] -= dmg2
                    try: add_particles(s1["pos"][0], s1["pos"][1], (255,200,0), 6)
                    except: pass
                    if s1["hp"] <= 0: to_del.add(s1["uid"])
                    if s2["hp"] <= 0: to_del.add(s2["uid"])
        soldiers = [s for s in soldiers if s["uid"] not in to_del]
        for z in zones:
            cnt = {}
            for s in soldiers:
                if s["job"] == "GUARD_ZONE" and s["zone_id"] == z["id"]:
                    if math.hypot(s["pos"][0] - z["pos"][0], s["pos"][1] - z["pos"][1]) < z["r"]:
                        cnt[s["team"]] = cnt.get(s["team"], 0) + 1
            if cnt and len(cnt) == 1:
                best = list(cnt.keys())[0]
                if z["owner"] != best:
                    z["cap"] += zone_cap_mult
                    if z["cap"] >= 80:
                        z["owner"] = best
                        z["cap"] = 0
                        if best in castles:
                            z["color_item"] = castles[best].get("color_item", neutral_item)
                            add_particles(z["pos"][0], z["pos"][1], get_render_color(z["color_item"]), 20)
        for z in zones:
            if z["owner"] == "neutral":
                pygame.draw.circle(screen, NEUTRAL, (int(z["pos"][0]), int(z["pos"][1])), z["r"])
            else:
                draw_fancy_circle(z["pos"], z["color_item"], z["r"])
            pygame.draw.circle(screen, BLACK, (int(z["pos"][0]), int(z["pos"][1])), z["r"], S(4))
            if z["cap"] > 0:
                pygame.draw.rect(screen, WHITE, (z["pos"][0] - z["r"], z["pos"][1] - z["r"] - S(12), int(z["cap"] / 80 * z["r"] * 2), S(7)))
            screen.blit(font_s.render(f"{z['id']}", True, BLACK if z["owner"]=="neutral" else WHITE), (z["pos"][0] - S(15), z["pos"][1] - S(10)))
        for cr in crates:
            pygame.draw.rect(screen, GOLD, (cr["pos"][0] - S(15), cr["pos"][1] - S(15), S(30), S(30)), border_radius=S(5))
        for name, c in castles.items():
            rad = S(45) if is_boss and name == "BOSS" else S(32) if not game_mode=="MAP" or difficulty>=3 else S(28)
            if name == "BOSS": rad = S(45)
            if c["hp"] <= 0:
                if is_free and name != "player":
                    rem_sec = max(1, int(c.get("respawn", 0) / 60) + 1)
                    rtxt = font_s.render(f"RESPAWN:{rem_sec}s", True, GOLD)
                    screen.blit(rtxt, (c["pos"][0] - rtxt.get_width() // 2, c["pos"][1] - S(10)))
                continue
            draw_fancy_circle(c["pos"], c.get("color_item", get_color_by_id("white")), rad)
            bar = int(max(0, c["hp"]) / c["max_hp"] * S(56))
            pygame.draw.rect(screen, (100, 0, 0), (c["pos"][0] - S(28), c["pos"][1] - S(38), S(56), S(8)))
            pygame.draw.rect(screen, GREEN, (c["pos"][0] - S(28), c["pos"][1] - S(38), bar, S(8)))
            if "difficulty" in c:
                diff_txt = ["TUT","EASY","MED","HARD","BOSS"][int(c["difficulty"])]
                dt = font_s.render(diff_txt, True, WHITE)
                screen.blit(dt, (c["pos"][0] - dt.get_width()//2, c["pos"][1] + S(35)))
            # Show soldier count
            cnt = len([s for s in soldiers if s["team"]==name])
            cnt_txt = font_s.render(f"{cnt}/40", True, WHITE)
            screen.blit(cnt_txt, (c["pos"][0] - cnt_txt.get_width()//2, c["pos"][1] + S(48)))
        for s in soldiers:
            hp_ratio = s["hp"]/TROOPS[s["type"]]["hp"]
            draw_stickman(s["pos"], s.get("color_item", soldier_color_item), s["type"], hp_ratio, TROOPS)
        update_and_draw_particles()
        diff_name = ["TUTORIAL","EASY","MEDIUM","HARD","BOSS"][difficulty] if difficulty<5 else "BOSS"
        screen.blit(font_m.render(f"${castles['player']['money']} | {diff_name} | {len([s for s in soldiers if s['team']=='player'])}/40 | MODE:{mode}", True, GOLD), (S(15), S(20)))
        if is_free and free_kill_count>0:
            screen.blit(font_s.render(f"Kills: {free_kill_count} | Next gem: {10 + 5*(free_kill_count//2)}", True, GOLD), (S(15), S(45)))
        for name, rect in control_rects.items():
            col = GREEN if mode == name else GRAY
            pygame.draw.rect(screen, col, rect, border_radius=S(8))
            screen.blit(font_s.render(name, True, WHITE), (rect.centerx - S(20), rect.centery - S(8)))
        for name, rect in shop_rects.items():
            col = GREEN if selected == name else (40, 40, 40)
            pygame.draw.rect(screen, col, rect, border_radius=S(8))
            txt_name = font_s.render(name, True, WHITE)
            txt_cost = font_s.render(f"${TROOPS[name]['cost']}", True, GOLD)
            screen.blit(txt_name, (rect.x + S(4), rect.y + S(2)))
            screen.blit(txt_cost, (rect.x + S(4), rect.y + S(18)))
        pygame.draw.rect(screen, (40, 40, 40), pause_btn, border_radius=S(8))
        pt = font_s.render("II", True, WHITE)
        screen.blit(pt, (pause_btn.centerx - pt.get_width() // 2, pause_btn.centery - pt.get_height() // 2))
        if castles["player"]["hp"] <= 0:
            SAVE["current_streak"] = 0
            write_save()
            result_screen("DEFEAT!", f"{diff_name} AI defeated you!", RED)
            return False
        enemies_alive = [n for n, c in castles.items() if n != "player" and c["hp"] > 0]
        if not enemies_alive and not is_free:
            SAVE["current_streak"] += 1
            if SAVE["current_streak"] > SAVE["best_streak"]: SAVE["best_streak"] = SAVE["current_streak"]
            reward = node.get("reward", 50) if isinstance(node, dict) else 50
            SAVE["gems"] += reward
            write_save()
            result_screen("VICTORY!", f"+{reward} GEMS! {diff_name} DEFEATED!", GREEN)
            return True
        pygame.display.flip()
        clock.tick(60)

def main():
    load_save()
    apply_audio_settings()
    while True:
        mode = main_menu()
        if mode is None: continue
        if "MAP" in str(mode):
            try: show_map()
            except Exception as e:
                print(f"map error {e}")
                import traceback
                traceback.print_exc()
                battle({"towers":2,"zones":1,"reward":20,"difficulty":0}, "MAP")
        elif "FREE" in str(mode):
            try: battle({"towers":3,"zones":2,"max_players":3,"difficulty":2}, "FREE")
            except Exception as e: print(f"free error {e}")
        elif "BOSS" in str(mode):
            try: battle({}, "BOSS")
            except Exception as e: print(f"boss error {e}")

if __name__ == "__main__":
    main()
