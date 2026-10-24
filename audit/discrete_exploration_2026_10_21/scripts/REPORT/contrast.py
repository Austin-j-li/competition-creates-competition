"""Print WCAG contrast ratios of the report's fallback colors. Print only."""


def lum(hexc):
    hexc = hexc.lstrip("#")
    rgb = [int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(x, y):
    a, b = sorted((lum(x), lum(y)), reverse=True)
    return (a + 0.05) / (b + 0.05)


themes = {
    "light": {"bg": "#ffffff", "cd": "#f6f5f1",
              "fg": "#1c1c1a", "mfg": "#5f5e5a", "bd": "#dcdad3",
              "c1": "#2f6bd8", "c2": "#a95b0c", "c3": "#1c7b51", "c4": "#8b44b8", "c5": "#b93a3a",
              "ok": "#23794a", "inf": "#2f6bd8", "warn": "#94600d", "bad": "#b8322a"},
    "dark": {"bg": "#161614", "cd": "#22211e",
             "fg": "#e9e7e1", "mfg": "#a9a79f", "bd": "#3d3c38",
             "c1": "#76aafb", "c2": "#efa155", "c3": "#4fc18c", "c4": "#c994ec", "c5": "#f28585",
             "ok": "#5cc690", "inf": "#76aafb", "warn": "#e2b252", "bad": "#f38b82"},
}
for name, t in themes.items():
    print("==", name, "==")
    for key in ("fg", "mfg", "bd", "c1", "c2", "c3", "c4", "c5", "ok", "inf", "warn", "bad"):
        print("  %-4s %s  on bg %.2f  on card %.2f" % (key, t[key], ratio(t[key], t["bg"]), ratio(t[key], t["cd"])))
