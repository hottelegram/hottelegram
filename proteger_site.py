# -*- coding: utf-8 -*-
import os
import re
import base64

def obfuscate_js(js_code):
    # Lista de strings sensíveis que vamos remover do código visível e colocar na tabela
    strings_to_obfuscate = [
        "hottelegram.github.io", "localhost", "127.0.0.1", "file:", "utf-8",
        "contextmenu", "dragstart", "keydown", "resize", "visible",
        "Acesso Negado", "Este site foi clonado ilegalmente ou está sendo executado em um domínio não autorizado.",
        "Ir para o site oficial", "Erro de carregamento de segurança.", "Acesso bloqueado por segurança",
        "Feche as ferramentas de desenvolvedor para visualizar o site.", "embers", "ember", "fade-up",
        "log", "info", "warn", "error", "dir", "clear", "table", "debugger", "constructor",
        "security-loader", "data-sec", "sec-script", "data-hash", "[native code]", "file",
        "HeadlessChrome", "Puppeteer", "Playwright", "PhantomJS", "domAutomation", "domAutomationController"
    ]
    
    # Codificando as strings em Base64
    encoded_strings = [base64.b64encode(s.encode('utf-8')).decode('utf-8') for s in strings_to_obfuscate]
    
    # Gerando o código JS da tabela de strings
    string_table_js = "const _0xarr = [" + ", ".join(f'"{s}"' for s in encoded_strings) + "];\n"
    # Decodificador dinâmico
    string_decoder_js = "const _0xdec = function(i) { return decodeURIComponent(escape(atob(_0xarr[i]))); };\n"
    
    # Substituindo strings literais pelo índice na tabela
    obfuscated_code = js_code
    for idx, s in enumerate(strings_to_obfuscate):
        obfuscated_code = obfuscated_code.replace(f'"{s}"', f'_0xdec({idx})')
        obfuscated_code = obfuscated_code.replace(f"'{s}'", f'_0xdec({idx})')
        
    # Mapa de variáveis críticas para renomeação
    var_replacements = {
        "payload": "_0x4a12",
        "key": "_0x8b3f",
        "authorizedDomains": "_0xc7e1",
        "currentHostname": "_0xf0d3",
        "isAuthorized": "_0xe9a4",
        "decrypt": "_0xd21b",
        "decoded": "_0x1b5c",
        "keyBytes": "_0x3f6a",
        "decryptedBytes": "_0x9e8d",
        "decoder": "_0x7a2c",
        "decryptedHTML": "_0x6c1e",
        "detectDevTools": "_0x5f0d",
        "blockSite": "_0x2e9b",
        "checkDevTools": "_0x8a3c",
        "disabledConsole": "_0x3c7e",
        "isAutomated": "_0xa7b9",
        "toStringFunc": "_0xe8f2",
        "container": "_0xd612",
        "colors": "_0xf2a1",
        "obs": "_0xbc82",
        "_0xc1": "_0xd4f1",
        "_0xc2": "_0xe5a2",
        "_0xc3": "_0xf6b3",
        "_0xc4": "_0x17c4"
    }
    
    for var_name, replacement in var_replacements.items():
        obfuscated_code = re.sub(r'\b' + var_name + r'\b', replacement, obfuscated_code)
        
    return string_table_js + string_decoder_js + obfuscated_code

def main():
    desenv_path = "site_nichoht_desenvolvimento.html"
    prod_paths = ["site_nichoht.html", "index.html"]

    if not os.path.exists(desenv_path):
        print(f"Erro: O arquivo {desenv_path} nao foi encontrado.")
        return

    print("Lendo arquivo de desenvolvimento...")
    with open(desenv_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Extraindo o conteúdo original do body
    body_match = re.search(r"<body[^>]*>(.*)</body>", html_content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        print("Erro: Nao foi possivel encontrar as tags <body> no arquivo de desenvolvimento.")
        return

    original_body_content = body_match.group(1)

    # Chave secreta XOR
    xor_key = "HotTelegramSecurityKey2026!#"
    
    # Criptografando o conteúdo original (Bytes UTF-8)
    body_bytes = original_body_content.encode('utf-8')
    key_bytes = xor_key.encode('utf-8')
    xored_bytes = bytearray(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(body_bytes))
    b64_body = base64.b64encode(xored_bytes).decode('utf-8')

    # 1. Fragmentação do Payload em 4 partes
    chunk_size = len(b64_body) // 4
    chunk1 = b64_body[:chunk_size]
    chunk2 = b64_body[chunk_size:chunk_size*2]
    chunk3 = b64_body[chunk_size*2:chunk_size*3]
    chunk4 = b64_body[chunk_size*3:]

    # JS bruto com as lógicas de segurança (que será ofuscado dinamicamente)
    raw_security_js = f"""
    (function() {{
        // 1. Auto-Defesa (Self-Defending) - Verifica se funções nativas foram alteradas
        try {{
            const toStringFunc = Function.prototype.toString;
            if (toStringFunc.toString().indexOf("[native code]") === -1) {{
                document.body.innerHTML = "";
                return;
            }}
            if (atob.toString().indexOf("[native code]") === -1 || 
                TextDecoder.toString().indexOf("[native code]") === -1) {{
                document.body.innerHTML = "";
                return;
            }}
        }} catch(e) {{
            document.body.innerHTML = "";
            return;
        }}

        // 2. Detecção de Automação e Headless (Playwright, Selenium, Puppeteer)
        const isAutomated = 
            navigator.webdriver || 
            window.callPhantom || 
            window._phantom || 
            window.__phantomgogo__ || 
            window.__nightmare || 
            /HeadlessChrome|Puppeteer|Playwright|PhantomJS/i.test(navigator.userAgent) ||
            window.domAutomation ||
            window.domAutomationController;

        if (isAutomated) {{
            document.body.innerHTML = "";
            return;
        }}

        // 3. Verificação de Domínio
        const authorizedDomains = ["hottelegram.github.io", "localhost", "127.0.0.1", ""];
        const currentHostname = window.location.hostname.toLowerCase();
        let isAuthorized = false;
        
        for (let d of authorizedDomains) {{
            if (currentHostname === d || currentHostname.endsWith("." + d)) {{
                isAuthorized = true;
                break;
            }}
        }}

        if (window.location.protocol === "file:") {{
            isAuthorized = true;
        }}

        if (!isAuthorized) {{
            document.body.innerHTML = `
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    background: #0a0a0a;
                    color: #fff;
                    font-family: 'Outfit', sans-serif;
                    text-align: center;
                    padding: 20px;
                ">
                    <div style="font-size: 80px; margin-bottom: 20px;">🔒</div>
                    <h1 style="font-size: 28px; font-weight: 800; margin-bottom: 10px; color: #ff5555;">Acesso Negado</h1>
                    <p style="color: #888; max-width: 450px; line-height: 1.6;">
                        Este site foi clonado ilegalmente ou está sendo executado em um domínio não autorizado.
                    </p>
                    <a href="https://hottelegram.github.io/hottelegram/" style="
                        margin-top: 25px;
                        background: linear-gradient(135deg, #ff6b1a 0%, #e50914 100%);
                        color: #fff;
                        text-decoration: none;
                        font-weight: 700;
                        padding: 12px 30px;
                        border-radius: 50px;
                        box-shadow: 0 4px 15px rgba(229,9,20,0.4);
                    ">Ir para o site oficial</a>
                </div>
            `;
            return;
        }}

        // 4. Reconstrução dos Fragmentos do Payload
        const _0xc1 = "{chunk1}";
        const _0xc2 = "{chunk3}";
        const _0xc3 = document.getElementById("security-loader").getAttribute("data-sec");
        const _0xc4 = document.getElementById("sec-script").getAttribute("data-hash");
        const payload = _0xc1 + _0xc3 + _0xc2 + _0xc4;
        const key = "{xor_key}";

        // 5. Descriptografia XOR
        function decrypt(b64Str, keyStr) {{
            const decoded = atob(b64Str);
            const keyBytes = [];
            for (let i = 0; i < keyStr.length; i++) {{
                keyBytes.push(keyStr.charCodeAt(i));
            }}
            const decryptedBytes = new Uint8Array(decoded.length);
            for (let i = 0; i < decoded.length; i++) {{
                decryptedBytes[i] = decoded.charCodeAt(i) ^ keyBytes[i % keyBytes.length];
            }}
            const decoder = new TextDecoder("utf-8");
            return decoder.decode(decryptedBytes);
        }}

        try {{
            const decryptedHTML = decrypt(payload, key);
            document.body.innerHTML = decryptedHTML;
        }} catch(e) {{
            document.body.innerHTML = "<div style='color:red; text-align:center; padding:50px;'>Erro de carregamento de segurança.</div>";
            return;
        }}

        // 6. Bloqueios de Interface (Mouse/Teclado)
        document.addEventListener('contextmenu', function(e) {{
            e.preventDefault();
            return false;
        }}, true);

        document.addEventListener('dragstart', function(e) {{
            e.preventDefault();
            return false;
        }}, true);

        document.addEventListener('keydown', function(e) {{
            if (e.key === "F12" || e.keyCode === 123) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C' || e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && (e.key === 'u' || e.key === 'U' || e.keyCode === 85)) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && (e.key === 's' || e.key === 'S' || e.keyCode === 83)) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && (e.key === 'a' || e.key === 'A' || e.keyCode === 65)) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && (e.key === 'c' || e.key === 'C' || e.keyCode === 67)) {{
                e.preventDefault();
                return false;
            }}
            if (e.ctrlKey && (e.key === 'p' || e.key === 'P' || e.keyCode === 80)) {{
                e.preventDefault();
                return false;
            }}
        }}, true);

        // 7. Anti-DevTools
        const disabledConsole = {{}};
        ["log", "info", "warn", "error", "dir", "clear", "table"].forEach(method => {{
            disabledConsole[method] = console[method];
            console[method] = function() {{}};
        }});

        setInterval(function() {{
            (function() {{
                const start = new Date();
                debugger;
                const end = new Date();
                if (end - start > 50) {{
                    document.body.innerHTML = "";
                    window.location.reload();
                }}
            }})();
        }}, 200);

        let threshold = 160;
        function checkDevTools() {{
            const widthDev = window.outerWidth - window.innerWidth > threshold;
            const heightDev = window.outerHeight - window.innerHeight > threshold;
            if (widthDev || heightDev) {{
                document.body.innerHTML = "";
            }}
        }}
        window.addEventListener('resize', checkDevTools);
        setInterval(checkDevTools, 500);

        // 8. Reativar efeitos originais do site
        const container = document.getElementById("embers");
        if (container) {{
            const colors = ['#ff6b1a','#e50914','#ffb347','#ff4444','#ff8c00'];
            container.innerHTML = '';
            for (let i = 0; i < 28; i++) {{
                const e = document.createElement('div');
                e.className = 'ember';
                const size = Math.random() * 3 + 1.5;
                const left = Math.random() * 100;
                const delay = Math.random() * 8;
                const dur = Math.random() * 6 + 5;
                const drift = (Math.random() - 0.5) * 120;
                e.style.cssText = `
                    left:${{left}}%;
                    width:${{size}}px;
                    height:${{size}}px;
                    background:${{colors[Math.floor(Math.random()*colors.length)]}};
                    animation-duration:${{dur}}s;
                    animation-delay:${{delay}}s;
                    --drift:${{drift}}px;
                    box-shadow:0 0 ${{size*2}}px ${{colors[Math.floor(Math.random()*colors.length)]}};
                `;
                container.appendChild(e);
            }}
        }}

        if (typeof IntersectionObserver !== 'undefined') {{
            const obs = new IntersectionObserver(entries => {{
                entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
            }}, {{ threshold: 0.1 }});
            document.querySelectorAll(".fade-up").forEach(el => obs.observe(el));
        }}

    }})();
    """

    print("Ofuscando JavaScript...")
    obfuscated_security_js = obfuscate_js(raw_security_js)

    # 2. Injetando Meta Tags de Bloqueio de Robôs e IAs no Head
    anti_bot_meta = """
  <!-- Anti-Robots, Anti-AI & SEO Privacy Controls -->
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
  <meta name="googlebot" content="noindex, nofollow">
  <meta name="bingbot" content="noindex, nofollow">
  <meta name="referrer" content="no-referrer">
  """
    
    # 3. CSS anti-seleção no Head
    anti_select_css = """
    /* Trava de interface do protetor de conteudo */
    *, html, body {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
        -webkit-touch-callout: none !important;
    }
    img, a {
        -webkit-user-drag: none !important;
        user-drag: none !important;
    }
    """

    # Injetando as meta tags logo após a tag <head>
    if "<head>" in html_content:
        html_content = html_content.replace("<head>", "<head>\n" + anti_bot_meta, 1)

    # Injetando o CSS anti-seleção no final do bloco <style>
    if "</style>" in html_content:
        html_content = html_content.replace("</style>", anti_select_css + "\n</style>", 1)

    # 4. Criando o Body de produção com o Loader contendo o Fragmento 2,
    # a tag noscript com a tela de bloqueio estilizada e a tag script com o Fragmento 4
    # e a lógica ofuscada.
    
    production_body_content = f"""
<body>
  <!-- Tela de Bloqueio No-JavaScript (Visual Premium Consistente com o Site) -->
  <noscript>
      <div style="
          position: fixed;
          inset: 0;
          background: #0a0a0a;
          z-index: 999999;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          font-family: 'Outfit', sans-serif;
          text-align: center;
          padding: 20px;
      ">
          <div style="font-size: 80px; margin-bottom: 20px; filter: drop-shadow(0 0 15px rgba(229, 9, 20, 0.4));">⚠️</div>
          <h1 style="
              font-family: 'Bebas Neue', sans-serif;
              font-size: clamp(32px, 8vw, 52px);
              font-weight: 800;
              margin-bottom: 15px;
              color: #e50914;
              letter-spacing: 2px;
              text-shadow: 0 0 15px rgba(229, 9, 20, 0.4);
          ">JavaScript Necessário</h1>
          <p style="color: #bbb; max-width: 450px; line-height: 1.7; font-size: 15px; margin-bottom: 5px;">
              Para acessar o conteúdo exclusivo de <strong>HotTelegram</strong> e garantir a integridade do seu acesso, você precisa habilitar o JavaScript no seu navegador.
          </p>
          <p style="color: #666; font-size: 13px; max-width: 320px;">
              Seu acesso é criptografado dinamicamente para sua segurança.
          </p>
          <div style="margin-top: 40px; font-size: 11px; color: #333; text-transform: uppercase; letter-spacing: 2.5px;">
              Segurança HotTelegram Ativa
          </div>
      </div>
  </noscript>

  <!-- Carregador Seguro contendo o Segmento 2 do Payload -->
  <div id="security-loader" data-sec="{chunk2}" style="
      position: fixed;
      inset: 0;
      background: #0a0a0a;
      z-index: 99999;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: 'Outfit', sans-serif;
  ">
      <div style="
          width: 50px;
          height: 50px;
          border: 3px solid rgba(229, 9, 20, 0.1);
          border-top: 3px solid #e50914;
          border-radius: 50%;
          animation: spin 1s linear infinite;
      "></div>
      <div style="
          margin-top: 20px;
          color: #888;
          font-size: 14px;
          letter-spacing: 2px;
          text-transform: uppercase;
      ">Segurança HotTelegram</div>
  </div>
  <style>
      @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
  </style>

  <!-- Script de descriptografia contendo o Segmento 4 do Payload e código ofuscado -->
  <script id="sec-script" data-hash="{chunk4}">
  {obfuscated_security_js}
  </script>
</body>
"""

    # Substitui o body original no HTML final
    final_html = re.sub(r"<body[^>]*>.*?</body>", production_body_content, html_content, flags=re.DOTALL | re.IGNORECASE)

    # Escrever em todas as saídas desejadas
    for path in prod_paths:
        print(f"Escrevendo arquivo final protegido em {path}...")
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_html)

    print("Protecao de Fase 2 aplicada com sucesso em todos os arquivos!")

if __name__ == "__main__":
    main()
