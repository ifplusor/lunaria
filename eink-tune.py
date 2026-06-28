#!/usr/bin/env python3
"""E-Ink palette tuner. Reads design targets + current palette, outputs new palette.

Usage:
  python3 eink-tune.py                    # regenerate lunaria-eink.json from targets
  python3 eink-tune.py --validate-only    # check if current palette meets targets

Design parameters are in eink-targets.json.
The current palette is read from lunaria-eink.json (for hue/chroma reference).
"""

import json, math, sys, argparse

# ── Color space utilities ──────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    def clamp(v): return max(0, min(255, int(v)))
    return f'#{clamp(r):02X}{clamp(g):02X}{clamp(b):02X}'

def relative_luminance(rgb):
    def linear(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linear(rgb[0]) + 0.7152 * linear(rgb[1]) + 0.0722 * linear(rgb[2])

def Lstar(Y):
    if Y <= 0.008856: return 903.3 * Y
    return 116 * (Y**(1/3)) - 16

def contrast(l1, l2):
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def rgb_to_oklch(r, g, b):
    def linear(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = linear(r), linear(g), linear(b)
    l_ = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m  = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s  = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_, m, s = l_**(1/3), m**(1/3), s**(1/3)
    L = 0.2104542553*l_ + 0.7936177850*m - 0.0040720468*s
    a = 1.9779984951*l_ - 2.4285922050*m + 0.4505937099*s
    b = 0.0259040371*l_ + 0.7827717662*m - 0.8086757660*s
    C = (a*a + b*b) ** 0.5
    h = math.atan2(b, a) * 180 / math.pi
    if h < 0: h += 360
    return L, C, h

def oklch_to_rgb(L, C, h):
    h_rad = h * math.pi / 180
    a = C * math.cos(h_rad)
    b = C * math.sin(h_rad)
    l = L + 0.3963377774*a + 0.2158037573*b
    m = L - 0.1055613458*a - 0.0638541728*b
    s = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l**3, m**3, s**3
    r =  4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    def gamma(c):
        return 12.92*c if c <= 0.0031308 else 1.055*(c**(1/2.4))-0.055
    return (int(max(0,min(1,gamma(r)))*255),
            int(max(0,min(1,gamma(g)))*255),
            int(max(0,min(1,gamma(bl)))*255))

def set_lstar(target_ls, chroma, hue):
    """Binary search in OKLCH to hit target L*."""
    lo, hi = 0.001, 0.999
    best = oklch_to_rgb(0.5, chroma, hue)
    for _ in range(50):
        mid = (lo + hi) / 2
        rgb = oklch_to_rgb(mid, chroma, hue)
        ls = Lstar(relative_luminance(rgb))
        if abs(ls - target_ls) < 0.2:
            return rgb
        if ls < target_ls: lo = mid
        else: hi = mid
        best = rgb
    return best

def compute_interpolated_neutral(target_ls, fg_rgb, bg_rgb):
    """Interpolate a neutral between fg and bg in OKLCH, preserving warmth."""
    fg_ls = Lstar(relative_luminance(fg_rgb))
    bg_ls = Lstar(relative_luminance(bg_rgb))
    _, _, fg_h = rgb_to_oklch(*fg_rgb)
    bg_L, _, bg_h = rgb_to_oklch(*bg_rgb)
    t = (target_ls - fg_ls) / (bg_ls - fg_ls)
    t = max(0, min(1, t))
    L = (1-t) * 0.3 + t * bg_L  # rough OKLCH L from L*
    C = 0.005  # near-neutral
    h = bg_h if t > 0.5 else fg_h
    return oklch_to_rgb(L, C, h)

# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Tune E-Ink palette')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate current palette against targets')
    parser.add_argument('--targets', default='eink-targets.json',
                        help='Targets file (default: eink-targets.json)')
    parser.add_argument('--palette', default='lunaria-eink.json',
                        help='Palette file (default: lunaria-eink.json)')
    args = parser.parse_args()

    # Load targets and palette
    targets = json.load(open(args.targets))
    eink = json.load(open(args.palette))

    fg_rgb = hex_to_rgb(targets['anchors']['fg']['hex'])
    bg_rgb = hex_to_rgb(targets['anchors']['bg']['hex'])
    bg_lum = relative_luminance(bg_rgb)
    fg_lum = relative_luminance(fg_rgb)

    if args.validate_only:
        validate(eink, targets, bg_lum, fg_lum)
        return

    # ── Anchors ──
    for key in ['fg', 'bg', 'emphBg', 'emphFg', 'bgHighlight', 'bgLowlight',
                'white', 'brightWhite', 'black', 'deepBlack', 'darkGray',
                'darkGrey', 'mediumGrey', 'lightGrey']:
        anchor = targets['anchors'].get(key)
        if anchor and 'hex' in anchor:
            eink[key] = anchor['hex']

    # ── Computed neutrals ──
    neutral_ls = targets['neutrals']
    for token in ['deEmphBg', 'mediumGray', 'deEmphFg', 'lightGray']:
        if token in neutral_ls:
            rgb = compute_interpolated_neutral(neutral_ls[token], fg_rgb, bg_rgb)
            eink[token] = rgb_to_hex(*rgb)
    # aliases
    eink['darkGrey'] = eink['darkGray']
    eink['mediumGrey'] = eink['mediumGray']
    eink['lightGrey'] = eink['lightGray']

    # ── Color tiers ──
    for tier_name in ['soft', 'vivid', 'hc']:
        spec = targets['tiers'][tier_name]
        for hue in ['Red', 'Yellow', 'Green', 'Blue', 'Violet', 'Magenta']:
            token = f'{tier_name}{hue}'
            target_ls = spec['L*'][hue]
            old_rgb = hex_to_rgb(eink[token])
            _, old_C, old_h = rgb_to_oklch(*old_rgb)
            new_C = old_C * spec['chroma_scale']
            rgb = set_lstar(target_ls, new_C, old_h)
            eink[token] = rgb_to_hex(*rgb)

    # ── bg* colors ──
    for token, target_ls in targets['bg_colors'].items():
        if token.startswith('_'): continue
        old_rgb = hex_to_rgb(eink[token])
        _, old_C, old_h = rgb_to_oklch(*old_rgb)
        rgb = set_lstar(target_ls, old_C, old_h)
        eink[token] = rgb_to_hex(*rgb)

    # ── Terminal ──
    for token, target_ls in targets['terminal'].items():
        if token.startswith('_'): continue
        old_rgb = hex_to_rgb(eink[token])
        _, old_C, old_h = rgb_to_oklch(*old_rgb)
        rgb = set_lstar(target_ls, old_C, old_h)
        eink[token] = rgb_to_hex(*rgb)

    # ── Inverse colors ──
    for tier_name in ['vivid', 'hc']:
        for hue in ['Red', 'Yellow', 'Green', 'Blue', 'Violet', 'Magenta']:
            orig = f'{tier_name}{hue}'
            inv = f'inv{tier_name[0].upper()+tier_name[1:]}{hue}'
            orig_ls = Lstar(relative_luminance(hex_to_rgb(eink[orig])))
            _, old_C, old_h = rgb_to_oklch(*hex_to_rgb(eink[orig]))
            inv_ls = max(45, min(85, 55 + (55 - orig_ls)))
            rgb = set_lstar(inv_ls, old_C * 0.85, old_h)
            eink[inv] = rgb_to_hex(*rgb)

    # ── Inverse neutrals ──
    _, _, bg_h = rgb_to_oklch(*bg_rgb)
    for token, tgt in [('invEmphBg', 0), ('invBg', 16), ('invDeEmphBg', 28),
                        ('invDeEmphFg', 52), ('invFg', 74), ('invEmphFg', 90)]:
        if tgt == 0:
            eink[token] = '#000000'
        else:
            eink[token] = rgb_to_hex(*set_lstar(tgt, 0.005, bg_h))

    # ── Write ──
    with open(args.palette, 'w') as f:
        json.dump(eink, f, indent='\t')
        f.write('\n')

    # ── Validate output ──
    validate(eink, targets, bg_lum, fg_lum)
    print(f'Written {args.palette}')


def validate(eink, targets, bg_lum, fg_lum):
    """Check palette meets all targets."""
    errors = []

    # Contrast
    cr = contrast(bg_lum, relative_luminance(hex_to_rgb(eink['fg'])))
    lo, hi = targets['contrast']['target_bg_fg']
    if not (lo <= cr <= hi):
        errors.append(f'bg-fg contrast {cr:.1f}:1 (target {lo}-{hi})')

    # Tiers
    for tier_name in ['soft', 'vivid', 'hc']:
        spec = targets['tiers'][tier_name]
        for hue in ['Red', 'Yellow', 'Green', 'Blue', 'Violet', 'Magenta']:
            token = f'{tier_name}{hue}'
            target_ls = spec['L*'][hue]
            actual_ls = Lstar(relative_luminance(hex_to_rgb(eink[token])))
            if abs(actual_ls - target_ls) > 1.5:
                errors.append(f'{token}: L* {actual_ls:.0f} (target {target_ls})')

    # hc* near fg
    fg_ls = Lstar(fg_lum)
    hc_min = min(Lstar(relative_luminance(hex_to_rgb(eink[f'hc{h}'])))
                 for h in ['Red','Yellow','Green','Blue','Violet','Magenta'])
    if hc_min - fg_ls < 1:
        errors.append(f'hc* minimum {hc_min:.0f} too close to fg {fg_ls:.0f}')

    # Gamut
    for k, v in eink.items():
        if k.startswith('_'): continue
        rgb = hex_to_rgb(v)
        if any(c < 0 or c > 255 for c in rgb):
            errors.append(f'{k}: {v} out of sRGB gamut')

    if errors:
        print('VALIDATION FAILED:')
        for e in errors: print(f'  ✗ {e}')
        sys.exit(1)
    else:
        print(f'VALIDATION PASSED  |  bg-fg {cr:.1f}:1  |  soft* L*49-52  vivid* L*38-47  hc* L*{hc_min}-32')

if __name__ == '__main__':
    main()
