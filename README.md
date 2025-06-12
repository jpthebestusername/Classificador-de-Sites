Classificador de Sites
Descrição
O Classificador de Sites Ideal é uma aplicação web que permite verificar se sites pertencem a segmentos específicos (como contabilidade) que devem ser bloqueados. A ferramenta analisa tanto o domínio quanto o conteúdo das páginas para identificar palavras-chave relacionadas aos segmentos bloqueados.

Funcionalidades Principais
Análise de Domínio: Verifica se o nome do domínio contém palavras bloqueadas

Análise de Conteúdo: Extrai e analisa o texto das páginas (incluindo título, cabeçalho e rodapé)

Verificação de Disponibilidade: Confirma se o site está acessível

Processamento em Paralelo: Analisa múltiplos sites simultaneamente para melhor performance

Filtragem e Exportação: Permite filtrar resultados e exportar para CSV

Tecnologias Utilizadas
Backend (Python/Flask)
Flask para o servidor web

BeautifulSoup para análise de HTML

Requests para requisições HTTP

ThreadPoolExecutor para processamento paralelo

Frontend (HTML/CSS/JavaScript)
Interface limpa e responsiva

Funcionalidades de filtro e exportação

Design moderno com tema escuro

Como Usar
Insira os sites a serem analisados (um por linha)

Clique em "Classificar Sites" para iniciar a análise

Use o campo de filtro para buscar por categorias específicas

Exporte os resultados para CSV quando necessário

Configuração
Os segmentos bloqueados podem ser configurados no arquivo app.py na variável SEGMENTOS_BLOQUEADOS.

Limitações
Analisa apenas até 200 sites por requisição

Depende da disponibilidade dos sites analisados

Pode ter falsos positivos/negativos dependendo da estrutura do site
