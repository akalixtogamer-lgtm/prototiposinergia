# Integrações externas

Regra seguida: só aparece como "Funcionando" o que roda de verdade no protótipo. O resto está marcado como **Não implementado** ou **Indisponível**, também na tela *Integrações* do administrador.

| Integração | Situação no protótipo | O que é | Para ativar de verdade |
| --- | --- | --- | --- |
| SurveyMonkey · abrir pesquisa | Funcionando | Cada pesquisa guarda o link público e abre em nova aba (`target=_blank`, `rel=noopener noreferrer`). O link é validado: precisa começar com `https://` e ser de `surveymonkey.com` | Trocar os links de exemplo (`…/r/EXEMPLO-…`) pelos links reais da conta |
| SurveyMonkey · importar respostas | Funcionando (arquivo) | Em *Pesquisas → Importar → Respostas*, CSV com `codigo;data;dispositivo;onde;genero`. XLSX e PDF ficam guardados, mas não são lidos | Padronizar a exportação do SurveyMonkey para essas colunas |
| SurveyMonkey · sincronizar pela API | Não implementado (fora do escopo aprovado) | — | Conta com acesso à API, app registrado no SurveyMonkey, token guardado **no servidor** (nunca no repositório), tratamento de limites de uso |
| Teams / Meet · abrir reunião | Funcionando (redirecionamento) | O agendamento guarda o link; formatos aceitos: `https://teams.microsoft.com/…`, `https://teams.live.com/…`, `https://meet.google.com/abc-defg-hij` | Nada além do link |
| Teams / Meet · criar reunião, ler gravação | Não implementado | — | Microsoft Graph ou Google Calendar/Meet API, consentimento do administrador da conta, servidor |
| Transcrição ao vivo | Indisponível | O protótipo não captura áudio. A transcrição entra por arquivo (`.vtt` ou `.txt`) exportado do Teams/Meet, ou texto colado. Nada é gerado automaticamente | Serviço de captura e reconhecimento de fala, armazenamento seguro, consentimento, retenção e exclusão definidos |

## Redirecionamento × integração

- **Redirecionamento** (o que existe): a Sinergia só abre o endereço. Não sabe quem entrou, não cria a reunião, não recebe gravação.
- **Integração** (não existe): a Sinergia falaria com a API do serviço, com credenciais guardadas no servidor.

## Transcrição: o que já está previsto nas telas

- Consentimento de gravação/transcrição junto com o termo de sigilo (participante marca as duas caixas).
- Estado da reunião: Agendada → Em andamento → Encerrada; transcrição: Aguardando transcrição → Transcrita → Processada → Analisada (ou Excluída).
- Importação de `.vtt` (as falas viram `[mm:ss] Nome: texto`), processamento com anonimização, análise e publicação de insights.
- Exclusão da transcrição pelo administrador; prazo de retenção selecionável em *Integrações* (padrão "A definir": decisão pendente, LGPD).

## Credenciais

Nenhuma chave, token ou senha está no repositório. O teste `tests/test_integracoes.py::test_sem_credenciais_no_repositorio` procura padrões comuns de segredo em todos os arquivos.
