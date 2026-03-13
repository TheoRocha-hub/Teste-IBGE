Notas Explicativas – Enriquecimento de Municípios via API do IBGE

1. Objetivo:
Enriquecer uma base de municípios brasileiros com dados adicionais da API pública do IBGE, como nome oficial, estado (UF), região, mesorregião e microrregião, gerando um novo CSV com as informações.

2. Fonte de dados:
API pública do IBGE: https://servicodados.ibge.gov.br/api/docs/localidades
, que fornece informações atualizadas sobre municípios, estados e regiões do Brasil.

3. Pipeline resumido:

Leitura do CSV de entrada.
Consulta à API do IBGE.
Extração dos dados relevantes.
Enriquecimento da base original.
Exportação para novo CSV.

4. Tratamento de erros:

Município não encontrado na API, Falhas de requisição HTTP, Dados ausentes na resposta.
Nestes casos, os campos adicionais são preenchidos como None ou vazio.

5. Limitações e erros observados:

Diferenças de grafia entre CSV e nome oficial da API podem impedir o match automático (ex.: Brasileia e Santo André-SP), causando registros não enriquecidos.
Dependência da disponibilidade da API.

6. Possíveis melhorias:

Cache para reduzir chamadas repetidas.
Normalização de texto para melhorar o matching.
Testes automatizados.

7. Execução:

python main.py
O script lê input.csv e gera resultado.csv.
