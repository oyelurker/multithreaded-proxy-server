import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. laptopUrlText in badgeLaptopUrl
    content = content.replace(
        '<text x="-160.5" y="-21.22" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">https://shop.example</text>',
        '<text id="laptopUrlText" x="-160.5" y="-21.22" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">https://shop.example</text>'
    )

    # 2. dnsNodeTitle & dnsNodeSub
    content = content.replace(
        '<text x="14" y="-23.4" text-anchor="middle" font-size="13.5" font-weight="800" fill="#211e1b" >DNS</text><text x="14" y="-9.4" text-anchor="middle" font-size="10" font-weight="600" fill="#211e1b" >resolver</text>',
        '<text id="dnsNodeTitle" x="14" y="-23.4" text-anchor="middle" font-size="13.5" font-weight="800" fill="#211e1b">DNS</text><text id="dnsNodeSub" x="14" y="-9.4" text-anchor="middle" font-size="10" font-weight="600" fill="#211e1b">resolver</text>'
    )

    # 3. serverNodeTitle & serverNodeSub
    content = content.replace(
        '<text x="126" y="57.1" text-anchor="middle" font-size="13" font-weight="800" fill="#211e1b" >Web</text><text x="126" y="72.6" text-anchor="middle" font-size="13" font-weight="800" fill="#211e1b" >Server</text>',
        '<text id="serverNodeTitle" x="126" y="57.1" text-anchor="middle" font-size="13" font-weight="800" fill="#211e1b">Web</text><text id="serverNodeSub" x="126" y="72.6" text-anchor="middle" font-size="13" font-weight="800" fill="#211e1b">Server</text>'
    )

    # 4. dbNodeTitle
    content = content.replace(
        '<text x="400.86" y="-23.52" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">database</text>',
        '<text id="dbNodeTitle" x="400.86" y="-23.52" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">database</text>'
    )

    # 5. dbQueryText
    content = content.replace(
        '<text x="217" y="9.78" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">SELECT … FROM products</text>',
        '<text id="dbQueryText" x="217" y="9.78" text-anchor="middle" font-size="10.5" font-weight="700" fill="#211e1b">SELECT … FROM products</text>'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('frontend/index.html')
patch_file(r'C:\Users\HP\.gemini\antigravity\brain\851c5192-0114-4520-91a5-11acbc32aa8f\os_proxy_designed_to_scale.html')
