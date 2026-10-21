# Sinergia Surveys — site e sistema (protótipo navegável)

Site institucional e sistema de pesquisas da Sinergia Research & Intelligence, montados a partir do mapa de navegação e do protótipo consolidado do Figma. Tudo roda no navegador: os dados de exemplo ficam salvos no `localStorage` de quem está usando, e cada pessoa vê a sua própria cópia. Nada é enviado para servidor.

## Estrutura

```
index.html                 site completo (HTML, CSS e JS num arquivo só)
assets/logo-sinergia.png   logo
```

## Login e permissões

O login tem duas entradas:

- **Administrador**: gerencia pesquisas, projetos, convites, resultados, cadastros, usuários e permissões.
- **Usuário**: navega como **Agente**, **Cliente Empresa** e/ou **Participante**, conforme o que o administrador marcar em *Usuários e permissões*. Quem tem mais de uma permissão escolhe o perfil ao entrar e troca pelo menu lateral ("Navegar como").

Na aba *Permissões por perfil*, o administrador também liga ou desliga funções de cada perfil (por exemplo, esconder "Recursos" dos agentes).

### Contas de demonstração (qualquer senha com 4+ caracteres)

| Conta | Acesso |
|---|---|
| helena@sinergia.com.br | Administrador |
| demo@sinergia.com.br | Usuário · Agente, Cliente e Participante |
| joao.tadeu@sinergia.com.br | Usuário · Agente e Participante |
| marina@cinemaalfa.com.br | Usuário · Cliente (Cinema Alfa) |
| ana.ribeiro@email.com | Usuário · Participante |

O cadastro de participante no site cria uma conta nova com permissão de Participante. O botão *Restaurar dados de exemplo* (menu do administrador) volta tudo ao estado inicial.

## Telas

| Área | Telas do Figma | Endereço |
|---|---|---|
| Site | Home, Serviços, Cinema, CAT, CIA, Pesquisa aberta, Cadastro | `#home`, `#servicos`, `#cinema`, `#cat`, `#cia`, `#pesquisa`, `#cadastro` |
| Acesso | Login (Administrador / Usuário) e escolha de perfil | `#login`, `#navegar` |
| Administrador | A1 Pesquisas e A2 Nova pesquisa, A3 Resultados, A4 Projetos, A5 Projeto, A6 Convites, A7 Cadastros, A8 Usuários e permissões | `#adm-pesquisas`, `#adm-resultados`, `#adm-projetos`, `#adm-projeto`, `#adm-convites`, `#adm-cadastros`, `#adm-usuarios` |
| Agente | G1 Minhas pesquisas, G2 Detalhes, G3/G4 Aplicar, G5 Recursos, G6 Perfil | `#ag-pesquisas`, `#ag-detalhes`, `#ag-aplicar`, `#ag-recursos`, `#ag-perfil` |
| Cliente Empresa | K1 Resultados, K2 Projetos, K3 Projeto, K4 Perfil | `#cl-resultados`, `#cl-projetos`, `#cl-projeto`, `#cl-perfil` |
| Participante | R1 Minhas pesquisas, R2 Preferências, R3 Pergunta com imagens, R4 Revisão, R5 Concluída, R6 Minhas respostas, R7 Perfil | `#pa-pesquisas`, `#pa-preferencias`, `#pa-responder`, `#pa-revisao`, `#pa-concluida`, `#pa-respostas`, `#pa-perfil` |

As áreas logadas exigem login; um endereço de outra área redireciona para a área permitida.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub e envie `index.html` e a pasta `assets` para a raiz.
2. No repositório, abra **Settings → Pages**.
3. Em **Source**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)` e clique em **Save**.
4. Em um ou dois minutos o site fica em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

## Sobre o acesso

- Em contas gratuitas, o GitHub Pages só publica repositórios **públicos**: qualquer pessoa com o link consegue abrir. O arquivo pede aos buscadores para não indexar a página (`noindex`), mas isso não é uma proteção de acesso.
- Para restringir a algumas pessoas: deixe o repositório **privado** e adicione-as como colaboradoras (Settings → Collaborators). Elas baixam e abrem o `index.html` no navegador, sem precisar de servidor.
- Páginas privadas com controle de acesso exigem GitHub Enterprise Cloud.

## Testar localmente

Abra `index.html` direto no navegador. As fontes vêm do Google Fonts, então é preciso estar on-line para vê-las; sem internet o site usa fontes de reserva.
