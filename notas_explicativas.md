Notas Explicativas – Enriquecimento de Municípios via API do IBGE
1. Objetivo

Este projeto tem como objetivo enriquecer uma base de dados contendo nomes de municípios brasileiros com informações adicionais obtidas a partir da API pública do IBGE.

A partir do arquivo de entrada (CSV), o script consulta a API de localidades do IBGE e adiciona informações como:

Nome oficial do município

Estado (UF)

Região

Mesorregião

Microrregião

O resultado final é salvo em um novo arquivo CSV contendo os dados originais acrescidos das informações obtidas da API.

2. Fonte de dados

Os dados são obtidos através da API pública do IBGE:

https://servicodados.ibge.gov.br/api/docs/localidades

Essa API fornece informações atualizadas sobre municípios, estados e regiões do Brasil.

3. Estrutura do pipeline

O pipeline segue os seguintes passos:

Leitura do arquivo CSV de entrada contendo municípios

Consulta à API do IBGE para buscar os dados do município

Extração das informações relevantes da resposta JSON

Enriquecimento da base original com os novos campos

Exportação do resultado para um novo arquivo CSV

4. Tratamento de erros

O script inclui tratamento para alguns cenários comuns:

Município não encontrado na API

Falhas de requisição HTTP

Dados ausentes na resposta da API

Nestes casos, o script mantém o registro original e preenche os campos adicionais como None ou vazio.

5. Limitações conhecidas

Algumas limitações do projeto incluem:

Dependência da disponibilidade da API do IBGE

Diferenças de grafia entre o nome do município no CSV e o nome oficial na API podem impedir o match automático

O script realiza requisições sequenciais, o que pode impactar performance para bases muito grandes

6. Possíveis melhorias

Algumas melhorias possíveis seriam:

Implementação de cache de municípios para reduzir chamadas repetidas à API

Uso de paralelização para acelerar as requisições

Implementação de normalização de texto para melhorar o matching de municípios

Inclusão de testes automatizados

7. Execução do projeto

Para executar o script:

python main.py

O script irá ler o arquivo input.csv e gerar o arquivo resultado.csv.