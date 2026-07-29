#!/usr/bin/env python3
import os
import sys
try:
    from PIL import Image, ImageEnhance
except ImportError:
    print("Pillow is not installed. Please run: pip install Pillow")
    sys.exit(1)

# The ramp used in the original ascii.svg (light to dark)
RAMP = [" ", ".", ":", "-", "=", "+", "*", "c", "s", "#", "%", "@"]

def get_char(val):
    # val is 0-255, where 0 is black and 255 is white
    idx = int((val / 255.0) * (len(RAMP) - 1))
    return RAMP[len(RAMP) - 1 - idx]

def main():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    img_path = os.path.join(workspace, "portrait.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(workspace, "portrait.png")
    
    if not os.path.exists(img_path):
        print("Error: Could not find portrait.jpg or portrait.png in the workspace root.")
        return

    print(f"Processing {img_path}...")
    
    img = Image.open(img_path).convert("L")
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    cols = 75
    char_width = 7.74
    char_height = 15.0
    
    orig_w, orig_h = img.size
    target_h = int((orig_h / orig_w) * cols * (char_width / char_height))
    
    img = img.resize((cols, target_h), Image.Resampling.LANCZOS)
    
    pixels = img.load()
    
    svg_lines = []
    svg_lines.append('<svg xmlns="http://www.w3.org/2000/svg" width="724" height="868" viewBox="0 0 724 868" font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,&apos;Liberation Mono&apos;,monospace">')
    svg_lines.append("""<style>@font-face{font-family:JBMono;font-style:normal;font-weight:400;font-display:block;src:url(data:font/woff2;base64,d09GMgABAAAAAAT4AA4AAAAACXwAAASmAAJN0wAAAAAAAAAAAAAAAAAAAAAAAAAAGhYbIBwqBmAAgQwRCAqIGIZQATYCJAM8CyAABCAFhCYHIBufByg+DNhkyEL73hCPSpDQcO3wJH4sGfunsjwyWl9JPDwv59e5byT3dCUxGbGVVBkrFc22Pz/Yvb5Avg8p5uFDuKQAJ2rXJGDr2rk2u/3qL2jONDcItMqJsqdHHkQYZ1BLICjLshaHF38jpGzByRmo+P4HQOeYM2ZolZP992Oz8jAPVbRBaEQykRJJYv8jYskk2ZbMs2byQnJNI82u76jTisLcwKzRs+J0BASKA0JIQggUVV27rK6D4ygUyg+5XECgqIbYsqndlc9wkXFoZMHV+dOQrN0KkLakIQD6aCfHKJBGR4BEEYNmOLN3ZwCPqi2T70/eR5pILHKI1DB9R235SMiH8nKE9lG5lgCVVcpRWG00DDxCWgbdnDwyOfFr4RI83f3pn5B77pWXLmhRGHSUVatSQBGFrjA5cioFCDX/Xx5EV4A4gsJfbsshOWmJAtJGsVk6FFtUz81fPEclE0OEGuOzxm59K5H9ols/7aInPnPLR8h80q1fvNjHj0SuWOaVpu1vJDto0N3P4ca0WIruec10j5fIdBv4RuYjI3Q1AD1MBu/L3JtsUR/SOXgQcfDWPHG3a++EnX7Q9pyIKCZzqPI+GoMx9NTtevqGDUTxAzfzruup2ODiLGCVoCwoSi8msMXdYskqMzgoQ455Hax4DLQP3/LW48iXi97R6o93eknQsu1aRPZB0S33yNyfSJEFMP8Q/F33xxpSVr4sIXn4PpVnViyyKaSBYoZtvbXt3o//oBJMVjRhUcK9xz39xF4H6csmzPQetVo32Nu5t5P6dOoeDc2cTZA+qCs0wjs7bmaaJXxphD3UXbi3ghnGu4bdMwR/2jvZZWllcPhCDV07tKPGa3JiAmoFXpEGL+o1eNIgO6zeI832cooKeznlevaYXgIuTeoq7rbeeOrqtziN1TIZYeUtjY0M1qxAV9TgIytCdRGXwd1U/+2qfyncOOcutjMt70LVg/4NXwzu5Kacd3WK6qh7iQ/hFI5Ym7LHikuP2VqHu6fh/6inD3t460ZdGLB7+sL0+R+Jsn07O/YeLuspc3b3hM7io53v3Uzs9KFmvY6eDlp74+95T6HOcNIYsbPQ1d9ObRkdbV+8nKr/KrZysH+tccCmXXtWzVu7dl6pScw8OoITQ+TowHQ3x7EtuzuGmqbNnkwQ9YbTtvgYVcDczVP+ESYe5QtvN3Rel97qnbkNFFIiDQGQcCStjwU5VbKQ+r3Kt+Zs59EV+v8J+f6DX99S7cmv+ynv9Df/A1BQAsH/4UtDGHquDYQBlfL7wQxgBAw+wgegAw22A7h7KCgXCEBe73GdECgVt8yyScEDnPmaRCHD9En5i+AeuSRUd1mSlPRVkk9b3yX5NY+6kgIGxORwBTWNI7pISFoiLSQgiISQEkMcgdrBh0fbUSP1SnMJictATEiIS0BMS0sI8/EgIXrMIwUlpGUg2IJIpKQMLRGRgBA35nluQh4JMSJHTe2xHb58ztXis3yx6rwolzSpooyYnM7Zi9PafBHBBtOPF0PyJM73cGeIWogc7kQ+Iunn+qJkQjBykm3rAgkhNYBcUUVAwbtTbpzrBnMM+uUmkgIB) format('woff2')}.a{fill:#6e7681}@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}}</style>""")

    x_start = 14
    y_start = 25.2

    for row in range(target_h):
        line_chars = []
        for col in range(cols):
            val = pixels[col, row]
            line_chars.append(get_char(val))
        
        line_str = "".join(line_chars).rstrip()
        if not line_str:
            continue
            
        y = y_start + (row * char_height)
        w_px = max(len(line_str), 1) * char_width
        delay = (row / target_h) * 5.0
        cid = f"c{row}"
        
        svg_lines.append(f'<clipPath id="{cid}"><rect x="{x_start}" y="{int(y)-11}" height="{int(char_height)}" width="0">')
        svg_lines.append(f'<animate attributeName="width" from="0" to="{w_px:.1f}" begin="{delay:.2f}s" dur="0.09s" fill="freeze"/></rect></clipPath>')
        
        safe_str = line_str.replace("&", "&amp;").replace("<", "&lt;")
        svg_lines.append(f'<g clip-path="url(#{cid})"><text xml:space="preserve" x="{x_start}" y="{y:.1f}" class="a" font-size="12.9">{safe_str}</text></g>')
        
        svg_lines.append(f'<rect y="{int(y)-10}" width="6" height="12" class="a" opacity="0">')
        svg_lines.append(f'<animate attributeName="x" from="{x_start}" to="{x_start + w_px + 7.74:.1f}" begin="{delay:.2f}s" dur="0.09s" fill="freeze"/>')
        svg_lines.append(f'<set attributeName="opacity" to="0.8" begin="{delay:.2f}s"/>')
        svg_lines.append(f'<set attributeName="opacity" to="0" begin="{delay + 0.09:.2f}s"/></rect>')

    svg_lines.append('</svg>')
    
    out_path = os.path.join(workspace, "ascii.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
        
    print(f"Generated {out_path} successfully!")

if __name__ == "__main__":
    main()
