# -*- coding: utf-8 -*-
import os
import re
import base64

def main():
    desenv_path = "site_nichoht_desenvolvimento.html"
    prod_paths = ["site_nichoht.html", "index.html"]

    if not os.path.exists(desenv_path):
        print(f"Erro: O arquivo {desenv_path} nao foi encontrado.")
        return

    print("Lendo arquivo de desenvolvimento...")
    with open(desenv_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Vamos extrair o conteúdo de dentro do <body> e criptografá-lo
    # Para garantir compatibilidade com tags body com atributos, usamos regex
    body_match = re.search(r"<body[^>]*>(.*)</body>", html_content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        print("Erro: Nao foi possivel encontrar as tags <body> no arquivo de desenvolvimento.")
        return

    original_body_content = body_match.group(1)

    # Chave de criptografia dinâmica e secreta
    xor_key = "HotTelegramSecurityKey2026!#"
    
    # Criptografando o conteúdo original do body (Nível de BYTES UTF-8)
    body_bytes = original_body_content.encode('utf-8')
    key_bytes = xor_key.encode('utf-8')
    
    xored_bytes = bytearray(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(body_bytes))
    
    # Convertendo para base64
    b64_body = base64.b64encode(xored_bytes).decode('utf-8')

    # Script JavaScript de segurança a ser injetado
    security_js = f"""
    (function() {{
        // Chave e payload criptografado
        const payload = "{b64_body}";
        const key = "{xor_key}";
        const authorizedDomains = ["hottelegram.github.io", "localhost", "127.0.0.1", ""];

        // 1. Verificação de Domínio
        const currentHostname = window.location.hostname.toLowerCase();
        let isAuthorized = false;
        
        for (let d of authorizedDomains) {{
            if (currentHostname === d || currentHostname.endsWith("." + d)) {{
                isAuthorized = true;
                break;
            }}
        }}

        // Se o protocolo for file://, permite para testes locais
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

        // 2. Descriptografia XOR (Byte-aligned usando TextDecoder)
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
            const decoder = new TextDecoder('utf-8');
            return decoder.decode(decryptedBytes);
        }}

        // Executa descriptografia e insere no body
        try {{
            const decryptedHTML = decrypt(payload, key);
            document.body.innerHTML = decryptedHTML;
        }} catch(e) {{
            document.body.innerHTML = "<div style='color:red; text-align:center; padding:50px;'>Erro de carregamento de segurança.</div>";
            return;
        }}

        // 3. Bloqueio de Clique Direito
        document.addEventListener('contextmenu', function(e) {{
            e.preventDefault();
            return false;
        }}, true);

        // Bloqueio de Arrastar Elementos (Imagens e Links)
        document.addEventListener('dragstart', function(e) {{
            e.preventDefault();
            return false;
        }}, true);

        // 4. Bloqueio de Teclas de Atalho
        document.addEventListener('keydown', function(e) {{
            // F12
            if (e.key === "F12" || e.keyCode === 123) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+Shift+I (Inspetor), Ctrl+Shift+J (Console), Ctrl+Shift+C (Elemento)
            if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C' || e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+U (Ver Código Fonte)
            if (e.ctrlKey && (e.key === 'u' || e.key === 'U' || e.keyCode === 85)) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+S (Salvar Página)
            if (e.ctrlKey && (e.key === 's' || e.key === 'S' || e.keyCode === 83)) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+A (Selecionar Tudo)
            if (e.ctrlKey && (e.key === 'a' || e.key === 'A' || e.keyCode === 65)) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+C (Copiar)
            if (e.ctrlKey && (e.key === 'c' || e.key === 'C' || e.keyCode === 67)) {{
                e.preventDefault();
                return false;
            }}
            // Ctrl+P (Imprimir)
            if (e.ctrlKey && (e.key === 'p' || e.key === 'P' || e.keyCode === 80)) {{
                e.preventDefault();
                return false;
            }}
        }}, true);

        // 5. Anti-DevTools / Console / Debugger
        // Desabilitar logs do console para impedir depuração de clonagem
        const disabledConsole = {{}};
        ["log", "info", "warn", "error", "dir", "clear", "table"].forEach(method => {{
            disabledConsole[method] = console[method];
            console[method] = function() {{}};
        }});

        // Loop de depuração contínuo (debugger statement)
        setInterval(function() {{
            (function() {{
                const start = new Date();
                debugger;
                const end = new Date();
                // Se a instrução debugger demorar mais de 50ms, significa que o DevTools está aberto e pausou
                if (end - start > 50) {{
                    document.body.innerHTML = "";
                    window.location.reload();
                }}
            }})();
        }}, 200);

        // Detecção por redimensionamento de janela (Devtools acoplado)
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

        // Reiniciar animação dos embers se o contêiner existir
        const container = document.getElementById('embers');
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

        // Reiniciar IntersectionObserver para efeitos de Fade In
        if (typeof IntersectionObserver !== 'undefined') {{
            const obs = new IntersectionObserver(entries => {{
                entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
            }}, {{ threshold: 0.1 }});
            document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));
        }}

    }})();
    """

    # Vamos recriar a página original substituindo o corpo (body) pelo loader de segurança
    # e incluindo o estilo de user-select no head.
    
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

    # Procurar a tag </style> do head para injetar o CSS de segurança ali
    if "</style>" in html_content:
        html_content = html_content.replace("</style>", anti_select_css + "\n</style>", 1)

    # 2. Criar a nova estrutura do HTML final com o Loader e o script de segurança.
    loader_html = """
<body>
  <!-- Protetor de Conteudo Premium - Carregando... -->
  <div id="security-loader" style="
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
      @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>

  <script>
  %SECURITY_JS%
  </script>
</body>
"""
    loader_html_with_js = loader_html.replace("%SECURITY_JS%", security_js)

    # Agora substituímos o body original do HTML pelo loader_html_with_js
    final_html = re.sub(r"<body[^>]*>.*?</body>", loader_html_with_js, html_content, flags=re.DOTALL | re.IGNORECASE)

    # Escrever em todas as saídas desejadas
    for path in prod_paths:
        print(f"Escrevendo arquivo final protegido em {path}...")
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_html)

    print("Protecao aplicada com sucesso em todos os arquivos!")

if __name__ == "__main__":
    main()
