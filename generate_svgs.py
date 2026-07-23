import os
import base64
import urllib.request
from io import BytesIO
import re
import random

try:
    from PIL import Image
    from rembg import remove
except ImportError as e:
    print(f"ImportError: {e}")
    print("Please install required packages: pip install rembg pillow requests")
    exit(1)

# File paths
WORKSPACE = r"d:\yashshinde0080"
IMAGE_PATH = os.path.join(WORKSPACE, "face-normal.png")
README_PATH = os.path.join(WORKSPACE, "README.md")
BANNER_DARK = os.path.join(WORKSPACE, "banner.svg")
BANNER_LIGHT = os.path.join(WORKSPACE, "banner-light.svg")
LANYARD = os.path.join(WORKSPACE, "lanyard.svg")


def get_base64_font():
    """Download JetBrains Mono font and return as base64 data URI."""
    print("Downloading JetBrains Mono font...")
    url = "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Regular.ttf"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            font_data = response.read()
        return "data:font/ttf;base64," + base64.b64encode(font_data).decode("utf-8")
    except Exception as e:
        print(f"Failed to download font: {e}")
        return ""


def process_images():
    """Remove background, prepare full image and avatar crop."""
    print(f"Loading image from {IMAGE_PATH}...")
    with open(IMAGE_PATH, "rb") as f:
        input_data = f.read()

    print("Removing background using rembg...")
    subject_only = remove(input_data)
    img = Image.open(BytesIO(subject_only))

    # Save full body as base64 PNG for banners
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    b64_full = base64.b64encode(buffered.getvalue()).decode("utf-8")

    print("Cropping avatar for lanyard...")
    w, h = img.size
    size = min(w, int(h * 0.6))
    left = (w - size) / 2
    top = h * 0.05
    avatar = img.crop((left, top, left + size, top + size))
    avatar.thumbnail((200, 200), Image.Resampling.LANCZOS)

    buf2 = BytesIO()
    avatar.save(buf2, format="PNG")
    b64_avatar = base64.b64encode(buf2.getvalue()).decode("utf-8")

    return b64_full, b64_avatar


def generate_particles(count=30, is_dark=True):
    """Generate floating particle circles with SMIL animations."""
    colors = ["#f5c2e7", "#cba6f7", "#89b4fa", "#f38ba8", "#a6e3a1"]
    base_opacity = "0.5" if is_dark else "0.35"
    particles = []
    for i in range(count):
        x = random.randint(30, 1250)
        y = random.randint(100, 700)
        r = random.randint(2, 5)
        delay = round(random.uniform(0, 5), 2)
        dur = round(random.uniform(5, 10), 1)
        op = round(random.uniform(0.2, 0.6), 2)
        color = random.choice(colors)
        particles.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="0">\n'
            f'  <animate attributeName="cy" values="{y};{y - random.randint(120, 250)}" dur="{dur}s" '
            f'repeatCount="indefinite" />\n'
            f'  <animate attributeName="opacity" values="0;{op};0" dur="{dur}s" '
            f'begin="{delay}s" repeatCount="indefinite" />\n'
            f'</circle>'
        )
    return "\n".join(particles)


def generate_name_letters():
    """Build per-letter tspans with staggered pop-in animations."""
    name = "Yash Tanaji Shinde"
    parts = []
    for i, char in enumerate(name):
        delay = round(0.8 + i * 0.06, 2)
        if char == " ":
            parts.append('<tspan xml:space="preserve"> </tspan>')
        else:
            parts.append(
                f'<tspan fill-opacity="0">'
                f'<animate attributeName="fill-opacity" from="0" to="1" begin="{delay}s" dur="0.25s" fill="freeze" />'
                f'{char}</tspan>'
            )
    return "".join(parts)


def generate_banner(is_dark, b64_img, b64_font):
    """Generate animated banner SVG — image on LEFT, content on RIGHT."""
    # Palette
    bg = "#1e1e2e" if is_dark else "#eff1f5"
    txt_main = "#cdd6f4" if is_dark else "#4c4f69"
    txt_sub = "#a6adc8" if is_dark else "#6c6f85"
    pill_bg = "#313244" if is_dark else "#ccd0da"
    neon = "#89b4fa" if is_dark else "#1e66f5"
    card_bg = "#181825" if is_dark else "#e6e9ef"
    card_border = "#313244" if is_dark else "#bcc0cc"
    term_bg = "#11111b" if is_dark else "#dce0e8"
    kw_color = "#cba6f7" if is_dark else "#8839ef"
    fn_color = "#89b4fa" if is_dark else "#1e66f5"
    str_color = "#a6e3a1" if is_dark else "#40a02b"
    class_color = "#f9e2af" if is_dark else "#df8e1d"
    text_color = txt_main

    particles = generate_particles(30, is_dark)
    name_letters = generate_name_letters()
    orbs = [
        (120, 200, 120, "#f5c2e7", "0s"),
        (900, 150, 100, "#89b4fa", "2s"),
        (1100, 600, 130, "#cba6f7", "1s"),
        (380, 500, 80, "#f38ba8", "3s"),
    ]
    orb_svg = "\n".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" class="orb" filter="blur(60px)" '
        f'style="animation-delay: {d};" />'
        for cx, cy, r, c, d in orbs
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 740" width="1280" height="740">
    <defs>
        <style>
            @font-face {{
                font-family: 'JetBrains Mono';
                src: url('{b64_font}') format('truetype');
            }}
            .term {{ font-family: 'Courier New', monospace; font-size: 20px; fill: {txt_main}; }}
            .name {{ font-family: 'JetBrains Mono', monospace; font-size: 55px; font-weight: bold; fill: url(#grad); }}
            .quote {{ font-family: 'Courier New', monospace; font-size: 18px; fill: {txt_sub}; font-style: italic; }}
            .pill-txt {{ font-family: sans-serif; font-size: 16px; fill: {txt_main}; font-weight: bold; }}
            .neon {{ font-family: 'Courier New', monospace; font-size: 24px; fill: {neon}; font-weight: bold; }}
            .role {{ font-family: 'Courier New', monospace; font-size: 28px; fill: {txt_main}; }}
            .code {{ font-family: 'Courier New', monospace; font-size: 16px; }}
            .pill {{ transition: all .3s ease; }}
            .pill:hover {{ transform: scale(1.05); filter: brightness(1.2); cursor: default; }}
            @keyframes blink {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0; }} }}
            .cursor {{ animation: blink 1s step-end infinite; }}
            @keyframes float {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-20px); }} }}
            @keyframes pulse {{ 0%,100% {{ opacity:0.25; }} 50% {{ opacity:0.55; }} }}
            .orb {{ animation: float 6s ease-in-out infinite, pulse 4s ease-in-out infinite; }}
            @keyframes flicker {{
                0%,100% {{ opacity: 1; }}
                3% {{ opacity: 0.4; }}
                6% {{ opacity: 1; }}
                7% {{ opacity: 0.7; }}
                10% {{ opacity: 1; }}
                20% {{ opacity: 0.9; }}
                50% {{ opacity: 1; }}
                52% {{ opacity: 0.5; }}
                55% {{ opacity: 1; }}
            }}
            .nf {{ animation: flicker 2.1s infinite; }}
        </style>

        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%">
                <animate attributeName="stop-color"
                    values="#f5c2e7;#cba6f7;#b4befe;#f5c2e7" dur="5s" repeatCount="indefinite" />
            </stop>
            <stop offset="50%">
                <animate attributeName="stop-color"
                    values="#cba6f7;#b4befe;#f5c2e7;#cba6f7" dur="5s" repeatCount="indefinite" />
            </stop>
            <stop offset="100%">
                <animate attributeName="stop-color"
                    values="#b4befe;#f5c2e7;#cba6f7;#b4befe" dur="5s" repeatCount="indefinite" />
            </stop>
        </linearGradient>

        <!-- Banner rounded‑corners clip -->
        <clipPath id="banner-clip"><rect width="1280" height="740" rx="20" /></clipPath>

        <!-- Tall clip‑paths so no OS font clips letters -->
        <clipPath id="term-reveal">
            <rect x="0" y="-8" width="0" height="66">
                <animate attributeName="width" from="0" to="540" dur="2s" fill="freeze" />
            </rect>
        </clipPath>
        <clipPath id="editor-reveal">
            <rect x="0" y="0" width="0" height="150">
                <animate attributeName="width" from="0" to="540" begin="1s" dur="3s" fill="freeze" />
            </rect>
        </clipPath>

        <mask id="hologram-mask">
            <rect x="0" y="0" width="450" height="740" fill="white" />
        </mask>
        <!-- Reveal mask: starts empty, grows down -->
        <mask id="hologram-reveal">
            <rect x="0" y="0" width="450" height="0" fill="white">
                <animate attributeName="height" from="0" to="740" begin="0.5s" dur="1.5s" fill="freeze" />
            </rect>
        </mask>

        <clipPath id="avatar-rect-clip">
            <rect x="20" y="20" width="400" height="700" rx="16" />
        </clipPath>
    </defs>

    <!-- Background -->
    <rect width="1280" height="740" rx="20" fill="{bg}" />

    <!-- Ambient orbs -->
    <g opacity="0.6">
    {orb_svg}
    </g>

    <!-- Particles -->
    <g>
    {particles}
    </g>

    <g clip-path="url(#banner-clip)">
        <!-- ───── LEFT SIDE — Character image ───── -->
        <g transform="translate(30,0)">
            <!-- Hologram glow flash -->
            <rect x="20" y="20" width="400" height="700" rx="16" fill="#89b4fa" opacity="0">
                <animate attributeName="opacity" values="0.5;0" begin="0s" dur="2s" fill="freeze" />
            </rect>

            <!-- Image masked by reveal AND clipped to rect -->
            <g clip-path="url(#avatar-rect-clip)">
                <image href="data:image/png;base64,{b64_img}" x="0" y="0" width="440" height="740"
                    mask="url(#hologram-reveal)" preserveAspectRatio="xMidYMid slice" opacity="0">
                    <animate attributeName="opacity" from="0" to="1" begin="0.5s" dur="1.5s" fill="freeze" />
                </image>

                <!-- One‑time scan line (trails the hologram reveal) -->
                <rect x="0" y="0" width="440" height="4" fill="#89b4fa" opacity="0.9">
                    <animate attributeName="y" from="0" to="740" begin="0.5s" dur="1.5s" fill="freeze" />
                </rect>
                
                <!-- Continuous avatar scanner (starts after initial reveal) -->
                <rect x="0" y="0" width="440" height="4" fill="#89b4fa" opacity="0.5">
                    <animate attributeName="y" from="-20" to="760" begin="3s" dur="3.5s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0;0.5;0.8;0.5;0" begin="3s" dur="3.5s" repeatCount="indefinite" />
                </rect>
            </g>

            <!-- Solid Rectangular Border -->
            <rect x="20" y="20" width="400" height="700" rx="16" fill="none" stroke="#89b4fa" stroke-width="6" opacity="0">
                <animate attributeName="opacity" from="0" to="1" begin="0.5s" dur="1.5s" fill="freeze" />
            </rect>
        </g>

        <g transform="translate(500,45)">
            <rect width="540" height="50" rx="10" fill="{term_bg}" opacity="0.85" />
            <circle cx="22" cy="25" r="6" fill="#f38ba8" />
            <circle cx="42" cy="25" r="6" fill="#f9e2af" />
            <circle cx="62" cy="25" r="6" fill="#a6e3a1" />
            <text x="84" y="32" class="term" clip-path="url(#term-reveal)">yash@dev :~ vim README.md</text>
            <rect x="380" y="14" width="10" height="24" fill="{txt_main}" class="cursor">
                <animate attributeName="x" from="84" to="380" dur="2s" fill="freeze" />
            </rect>
        </g>

        <!-- Name — letters pop in one by one -->
        <g transform="translate(500,170)">
            <text x="0" y="0" class="name">{name_letters}</text>
        </g>

        <!-- Role — non‑overlapping cycle -->
        <g transform="translate(500,230)">
            <text x="0" y="0" class="role" fill-opacity="0">
                <tspan>&gt; I am an AI Engineer.</tspan>
                <animate attributeName="fill-opacity" values="0;1;1;0;0;0" keyTimes="0;0.055;0.277;0.333;0.95;1" dur="9s" repeatCount="indefinite" />
            </text>
            <text x="0" y="0" class="role" fill-opacity="0">
                <tspan>&gt; I build LLM Applications.</tspan>
                <animate attributeName="fill-opacity" values="0;0;1;1;0;0" keyTimes="0;0.333;0.388;0.611;0.666;1" dur="9s" repeatCount="indefinite" />
            </text>
            <text x="0" y="0" class="role" fill-opacity="0">
                <tspan>&gt; I solve complex problems.</tspan>
                <animate attributeName="fill-opacity" values="0;0;1;1;0" keyTimes="0;0.666;0.722;0.944;1" dur="9s" repeatCount="indefinite" />
            </text>
        </g>

        <!-- Quote card -->
        <g transform="translate(500,280)">
            <rect width="540" height="56" rx="8" fill="{pill_bg}" opacity="0.5" />
            <text x="20" y="34" class="quote">"AI Engineer | Python | LLMs"</text>
        </g>

        <!-- Tech stack pills -->
        <g transform="translate(500,380)">
            <text x="0" y="-18" font-family="'Courier New',monospace" font-size="20" fill="{txt_main}">Tech Stack:</text>

            <!-- Row 1 -->
            <g transform="translate(0,2)" class="pill" opacity="0">
                <rect width="88" height="34" rx="17" fill="{pill_bg}" />
                <text x="44" y="22" class="pill-txt" text-anchor="middle">Python</text>
                <animate attributeName="opacity" from="0" to="1" begin=".5s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(96,2)" class="pill" opacity="0">
                <rect width="68" height="34" rx="17" fill="{pill_bg}" />
                <text x="34" y="22" class="pill-txt" text-anchor="middle">SQL</text>
                <animate attributeName="opacity" from="0" to="1" begin=".7s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(172,2)" class="pill" opacity="0">
                <rect width="68" height="34" rx="17" fill="{pill_bg}" />
                <text x="34" y="22" class="pill-txt" text-anchor="middle">Git</text>
                <animate attributeName="opacity" from="0" to="1" begin=".9s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(248,2)" class="pill" opacity="0">
                <rect width="88" height="34" rx="17" fill="{pill_bg}" />
                <text x="44" y="22" class="pill-txt" text-anchor="middle">Linux</text>
                <animate attributeName="opacity" from="0" to="1" begin="1.1s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(344,2)" class="pill" opacity="0">
                <rect width="98" height="34" rx="17" fill="{pill_bg}" />
                <text x="49" y="22" class="pill-txt" text-anchor="middle">Gen AI</text>
                <animate attributeName="opacity" from="0" to="1" begin="1.3s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(450,2)" class="pill" opacity="0">
                <rect width="68" height="34" rx="17" fill="{pill_bg}" />
                <text x="34" y="22" class="pill-txt" text-anchor="middle">LLM</text>
                <animate attributeName="opacity" from="0" to="1" begin="1.5s" dur=".4s" fill="freeze" />
            </g>

            <!-- Row 2 -->
            <g transform="translate(0,44)" class="pill" opacity="0">
                <rect width="98" height="34" rx="17" fill="{pill_bg}" />
                <text x="49" y="22" class="pill-txt" text-anchor="middle">FastAPI</text>
                <animate attributeName="opacity" from="0" to="1" begin="1.7s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(106,44)" class="pill" opacity="0">
                <rect width="108" height="34" rx="17" fill="{pill_bg}" />
                <text x="54" y="22" class="pill-txt" text-anchor="middle">PyTorch</text>
                <animate attributeName="opacity" from="0" to="1" begin="1.9s" dur=".4s" fill="freeze" />
            </g>
            <g transform="translate(222,44)" class="pill" opacity="0">
                <rect width="138" height="34" rx="17" fill="{pill_bg}" />
                <text x="69" y="22" class="pill-txt" text-anchor="middle">DeepLearning</text>
                <animate attributeName="opacity" from="0" to="1" begin="2.1s" dur=".4s" fill="freeze" />
            </g>
        </g>

        <!-- Code‑editor card -->
        <g transform="translate(500,490)">
            <rect width="540" height="150" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="2" />
            <g clip-path="url(#editor-reveal)">
                <circle cx="20" cy="20" r="6" fill="#f38ba8" />
                <circle cx="40" cy="20" r="6" fill="#f9e2af" />
                <circle cx="60" cy="20" r="6" fill="#a6e3a1" />
                
                <text x="20" y="60" class="code" fill="{kw_color}">def <tspan fill="{fn_color}">build_dreams</tspan>():</text>
                <text x="50" y="85" class="code" fill="{kw_color}">return <tspan fill="{class_color}">Innovation</tspan>(</text>
                <text x="80" y="110" class="code" fill="{text_color}">stack=[<tspan fill="{str_color}">'AI'</tspan>, <tspan fill="{str_color}">'LLMs'</tspan>]</text>
                <text x="50" y="135" class="code" fill="{text_color}">)</text>
            </g>
        </g>

        <!-- Neon sign -->
        <text x="900" y="700" class="neon nf" text-anchor="middle">
            KEEP CODING KEEP GROWING
        </text>
    </g>
</svg>'''
    return svg


def generate_lanyard(b64_avatar):
    """Generate swinging ID‑badge lanyard SVG with holographic shine."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 850" width="400" height="850">
    <defs>
        <!-- Holographic shine gradient -->
        <linearGradient id="shine" x1="0%" y1="0%" x2="200%" y2="0%">
            <stop offset="-100%" stop-color="rgba(255,255,255,0)" />
            <stop offset="-75%" stop-color="rgba(255,255,255,0.35)" />
            <stop offset="-50%" stop-color="rgba(255,255,255,0)" />
            <animate attributeName="x1" from="-200%" to="200%" dur="3s" repeatCount="indefinite" />
            <animate attributeName="x2" from="-100%" to="300%" dur="3s" repeatCount="indefinite" />
        </linearGradient>

        <!-- Avatar ring glow -->
        <radialGradient id="ring-glow" cx="50%" cy="50%" r="50%">
            <stop offset="80%" stop-color="#cba6f7" stop-opacity="0" />
            <stop offset="95%" stop-color="#cba6f7" stop-opacity="0.8" />
            <stop offset="100%" stop-color="#cba6f7" stop-opacity="0" />
        </radialGradient>

        <clipPath id="avatar-clip">
            <circle cx="105" cy="130" r="56" />
        </clipPath>
    </defs>

    <g transform-origin="200 60">
        <!--
            Damped pendulum: drop from −20°, overshoot, settle, then gentle sway.
            Drop:      0–1.5 s  −20 → 8    (fast down, first overshoot)
            Dampen:    1.5–3 s   8 → −4    (backswing)
            Settle:    3–4.5 s  −4 → 0     (settle into rest)
            Sway:      4.5+ s    0 → −4 → 4 → −4 → 0 … (gentle forever)
        -->
        <animateTransform attributeName="transform" type="rotate"
            values="-20; 8; -4; 2; -1; 0; 0; -3; 3; -3; 0; 3; -3; 0"
            keyTimes="0; 0.04; 0.08; 0.12; 0.16; 0.2; 0.25; 0.35; 0.45; 0.55; 0.65; 0.75; 0.85; 1"
            dur="8s" repeatCount="indefinite" calcMode="spline"
            keySplines="0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"
        />

        <!-- Strap -->
        <path d="M160,-50 L180,100 L220,100 L240,-50" fill="none" stroke="#11111b" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" />

        <!-- Metal ring -->
        <circle cx="200" cy="120" r="16" fill="none" stroke="#9399b2" stroke-width="7" />
        <circle cx="200" cy="120" r="16" fill="none" stroke="#cdd6f4" stroke-width="2" opacity="0.4" />

        <!-- Clasp -->
        <rect x="184" y="135" width="32" height="22" rx="5" fill="#585b70" />
        <rect x="184" y="135" width="32" height="4" rx="2" fill="#9399b2" />

        <!-- ID card body -->
        <g transform="translate(95, 170)">
            <rect width="210" height="330" rx="16" fill="#181825" stroke="#313244" stroke-width="2" />

            <!-- Top header bar -->
            <rect width="210" height="42" rx="16" fill="#89b4fa" />
            <rect y="20" width="210" height="22" fill="#89b4fa" />
            <text x="105" y="26" font-family="sans-serif" font-weight="bold" font-size="15" fill="#11111b" text-anchor="middle" letter-spacing="2">STAFF ID</text>

            <!-- Avatar area -->
            <circle cx="105" cy="130" r="60" fill="none" stroke="#cba6f7" stroke-width="4" opacity="0.8" />
            <circle cx="105" cy="130" r="62" fill="url(#ring-glow)" />
            <circle cx="105" cy="130" r="56" fill="#1e1e2e" />

            <!-- Avatar -->
            <image href="data:image/png;base64,{b64_avatar}" x="49" y="74" width="112" height="112"
                clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice" />

            <!-- Info -->
            <text x="105" y="225" font-family="sans-serif" font-weight="bold" font-size="22" fill="#cdd6f4" text-anchor="middle">Yash Shinde</text>
            <text x="105" y="252" font-family="sans-serif" font-size="14" fill="#a6adc8" text-anchor="middle">AIML Engineer</text>
            <text x="105" y="275" font-family="sans-serif" font-size="13" fill="#89b4fa" text-anchor="middle">@yashshinde0080</text>

            <!-- Barcode -->
            <g transform="translate(35, 295)">
                <rect width="4" height="28" fill="#cdd6f4" />
                <rect x="7" width="2" height="28" fill="#cdd6f4" />
                <rect x="12" width="8" height="28" fill="#cdd6f4" />
                <rect x="23" width="3" height="28" fill="#cdd6f4" />
                <rect x="29" width="6" height="28" fill="#cdd6f4" />
                <rect x="38" width="4" height="28" fill="#cdd6f4" />
                <rect x="45" width="9" height="28" fill="#cdd6f4" />
                <rect x="57" width="2" height="28" fill="#cdd6f4" />
                <rect x="62" width="5" height="28" fill="#cdd6f4" />
                <rect x="70" width="3" height="28" fill="#cdd6f4" />
                <rect x="76" width="4" height="28" fill="#cdd6f4" />
                <rect x="83" width="7" height="28" fill="#cdd6f4" />
                <rect x="93" width="2" height="28" fill="#cdd6f4" />
                <rect x="98" width="5" height="28" fill="#cdd6f4" />
                <rect x="106" width="3" height="28" fill="#cdd6f4" />
                <rect x="112" width="8" height="28" fill="#cdd6f4" />
                <rect x="123" width="4" height="28" fill="#cdd6f4" />
                <rect x="130" width="2" height="28" fill="#cdd6f4" />
            </g>

            <!-- Holo shine overlay -->
            <rect width="210" height="330" rx="16" fill="url(#shine)" pointer-events="none" />
        </g>
    </g>
</svg>'''
    return svg


def update_readme():
    """Inject banner + lanyard picture-switching block at top of README."""
    print("Updating README.md...")
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    injection = """<!-- BANNER:profile-header -->
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="banner-light.svg?v=1">
    <source media="(prefers-color-scheme: dark)" srcset="banner.svg?v=1">
    <img src="banner.svg?v=1" alt="Animated Banner" width="100%">
  </picture>
</div>
<br/>

"""

    if "<!-- BANNER:profile-header -->" not in content:
        content = injection + content

        def replacer(m):
            url = m.group(1)
            if not url.startswith("http") and not url.startswith("data:"):
                if "?" not in url:
                    return f'src="{url}?v=1"'
            return m.group(0)

        content = re.sub(r'src="([^"]+)"', replacer, content)

        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully.")
    else:
        print("README.md already contains the SVGs.")


def main():
    print("Starting SVG generation process...\n")

    try:
        b64_full, b64_avatar = process_images()
    except Exception as e:
        print(f"Error processing images: {e}")
        return

    try:
        b64_font = get_base64_font()
    except Exception as e:
        print(f"Error downloading font: {e}")
        b64_font = ""

    print()
    print("Generating Dark Banner...")
    with open(BANNER_DARK, "w", encoding="utf-8") as f:
        f.write(generate_banner(True, b64_full, b64_font))
    print("  [OK] banner.svg")

    print("Generating Light Banner...")
    with open(BANNER_LIGHT, "w", encoding="utf-8") as f:
        f.write(generate_banner(False, b64_full, b64_font))
    print("  [OK] banner-light.svg")

    print("Generating Lanyard...")
    with open(LANYARD, "w", encoding="utf-8") as f:
        f.write(generate_lanyard(b64_avatar))
    print("  [OK] lanyard.svg")

    update_readme()
    print("\nDone! All SVGs generated successfully.")


if __name__ == "__main__":
    main()
