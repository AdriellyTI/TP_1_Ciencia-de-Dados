# Guia do Trabalho 1 — Aquisição de Dados

**Disciplina:** Ciência de Dados  
**Instituição:** Universidade Federal do Amazonas — Instituto de Computação  
**Baseado no enunciado do Trabalho 1 — Aquisição de Dados**

> Este guia traduz o PDF da disciplina em um roteiro prático. O PDF e as orientações do professor continuam sendo a referência oficial em caso de dúvida.

---

## 1. Visão geral do trabalho

O Trabalho 1 é a primeira fase de um projeto contínuo. A base criada agora será reutilizada em atividades futuras, como:

- análise exploratória de dados (EDA);
- storytelling com dados;
- classificação;
- regressão;
- séries temporais;
- agrupamento.

Portanto, o objetivo não é apenas obter uma tabela que funcione hoje. O grupo deve construir uma base **rica, rastreável, documentada e reprodutível**, que possa ser compreendida e ampliada ao longo do semestre.

A base deve ser criada pelo próprio grupo a partir de fontes reais, usando pelo menos dois métodos de aquisição diferentes:

1. **uma API web**; e
2. **uma coleta direta de HTML, isto é, web scraping**.

> **Nota:** O projeto deste grupo utiliza **três fontes** (duas APIs + um scraping), excedendo o mínimo exigido:
> - Fonte 1 — IBGE/SIDRA (API)
> - Fonte 2 — DIEESE (web scraping de HTML)
> - Fonte 3 — TSE/Dados Abertos (API)

Essas fontes precisam ser integradas em uma base única e coerente. Não basta entregar duas tabelas independentes.

---

## 2. Objetivo principal

O grupo deve:

1. escolher um tema de interesse;
2. formular uma pergunta que possa ser investigada com os dados;
3. coletar dados de pelo menos duas fontes heterogêneas;  <!-- Este projeto: 3 fontes -->
4. garantir que uma fonte seja obtida por API;  <!-- IBGE/SIDRA e TSE -->
5. garantir que outra fonte seja obtida por scraping de HTML;  <!-- DIEESE -->
6. preservar os dados brutos exatamente como foram coletados;
7. tratar, limpar e integrar os dados;
8. registrar a proveniência de cada coleta;
9. documentar limitações, decisões e aspectos éticos e legais;
10. entregar o notebook, os dados e o dataset card em um único pacote.

---

## 3. Escolha do tema e da pergunta

### 3.1 Como escolher um bom tema

O tema deve ser interessante o suficiente para sustentar o trabalho durante o semestre e permitir diferentes tipos de análise. É recomendável escolher um assunto que ofereça:

- variáveis numéricas e categóricas;
- datas ou períodos, quando possível;
- quantidade suficiente de observações;
- possibilidade de comparação entre grupos ou regiões;
- possibilidade de obter dados de fontes diferentes;
- uma chave que permita integrar as fontes;
- ausência ou tratamento adequado de dados pessoais.

Exemplos de unidades de observação são:

- um município;
- um produto;
- um filme;
- um jogo;
- uma viagem;
- uma estação meteorológica em determinado dia;
- um registro de atendimento por período;
- um indicador de uma cidade ou estado.

### 3.2 Pergunta motivadora

A pergunta motivadora deve explicar o que o grupo pretende investigar. Ela não precisa ser uma hipótese definitiva, mas deve orientar a coleta.

Exemplos de formulação:

- Quais fatores estão associados à avaliação de filmes em determinado período?
- Como indicadores socioeconômicos variam entre municípios e regiões?
- Existe relação entre condições meteorológicas e determinados eventos?
- Como preços, avaliações e características de produtos se relacionam?

Evite um tema amplo demais, como “dados sobre educação”. Prefira algo delimitado, como “relação entre indicadores educacionais e características socioeconômicas dos municípios do Amazonas”.

### 3.3 Aprovação do tema

O tema e as fontes pretendidas devem ser aprovados previamente pelo professor. Antes da coleta definitiva, confirme:

- o tema;
- a pergunta motivadora;
- as fontes escolhidas;
- a viabilidade da integração;
- o volume esperado de dados;
- eventuais restrições de licença ou acesso.

---

## 4. Requisitos obrigatórios de aquisição

### 4.1 Duas fontes distintas

O grupo precisa utilizar no mínimo duas fontes de dados diferentes. As fontes devem ser realmente distintas, e não duas cópias ou formatos diferentes do mesmo dataset.

### 4.2 Pelo menos uma API

Uma das fontes deve ser adquirida via API pública ou autenticada. O notebook deve mostrar, de forma reprodutível:

- URL-base da API;
- endpoint utilizado;
- parâmetros enviados;
- método HTTP, normalmente `GET`;
- paginação, quando existir;
- campos retornados;
- tratamento de erros e status HTTP;
- momento da coleta;
- armazenamento da resposta bruta.

A API pode retornar JSON, CSV ou outro formato estruturado. A resposta deve ser salva antes da limpeza.

### 4.3 Pelo menos uma coleta direta de HTML

A segunda fonte deve ser obtida a partir do HTML de uma página. Podem ser usados, por exemplo:

- `pandas.read_html`;
- `BeautifulSoup`;
- outro parser de HTML;
- navegador automatizado, apenas quando a página exigir JavaScript e isso for justificado.

O notebook deve explicar:

- URL acessada;
- página ou tabela selecionada;
- seletor ou critério usado para localizar os dados;
- quantidade de páginas ou requisições;
- pausas entre requisições;
- tratamento de falhas;
- forma de armazenamento do HTML bruto.

Apenas copiar manualmente informações de uma página não caracteriza scraping reprodutível.

---

## 5. Integração real das fontes

As fontes devem se cruzar em pelo menos um ponto. O resultado final deve conter informações que não existiam juntas em nenhuma fonte isolada.

### 5.1 Definição da chave de integração

A chave é o campo, ou conjunto de campos, usado para relacionar os registros. Exemplos:

- código do município;
- sigla da unidade federativa;
- identificador de produto;
- nome normalizado de uma cidade;
- combinação de local e data;
- código de categoria;
- identificador de uma obra ou evento;
- **ano eleitoral** (para integrar dados econômicos com resultados eleitorais);
- **sigla do partido** (para mapear o espectro partidário dos governantes).

Prefira códigos oficiais ou identificadores estáveis a nomes livres. Nomes podem conter diferenças de acentuação, abreviações, maiúsculas e grafias.

### 5.2 Normalização dos campos

Antes do join, documente como as divergências foram tratadas. Podem ser necessárias operações como:

- converter texto para minúsculas;
- remover espaços extras;
- remover ou padronizar acentos;
- substituir abreviações;
- corrigir grafias conhecidas;
- padronizar separadores e pontuação;
- converter códigos para o mesmo tipo;
- uniformizar datas e unidades.

Não altere apenas os dados sem registrar a decisão. Mantenha, quando for útil, a coluna original e crie uma coluna normalizada para a integração.

### 5.3 Tipo de junção

Explique no notebook:

- qual foi a chave;
- qual tabela foi a principal;
- se o join foi `inner`, `left`, `right` ou outro;
- quantos registros existiam antes e depois;
- quantos registros foram casados;
- quantos ficaram sem correspondência;
- se houve duplicidades;
- como as falhas de casamento foram tratadas.

Um join `inner` pode eliminar registros sem correspondência. Um join `left` pode preservar a fonte principal e gerar valores ausentes na fonte enriquecedora. A escolha deve ser justificada pelo objetivo do projeto.

### 5.4 Verificações após a integração

Faça pelo menos estas verificações:

- a chave deveria ser única? Ela realmente é?
- houve duplicação inesperada de linhas?
- o número de registros faz sentido?
- as unidades estão compatíveis?
- apareceram valores ausentes?
- os valores numéricos estão em escalas plausíveis?
- a tabela integrada mantém a unidade de observação definida?

---

## 6. Preservação dos dados brutos

Os dados brutos são parte obrigatória da entrega. Eles devem ser guardados **antes de qualquer limpeza ou transformação**.

Organize o pacote, por exemplo, assim:

```text
projeto/
├── notebook_coleta.ipynb
├── dados_brutos/
│   ├── api_resposta_YYYYMMDD.json
│   ├── pagina_fonte_YYYYMMDD.html
│   └── tabela_scraping_YYYYMMDD.csv
├── dados_tratados/
│   └── base_integrada.parquet
├── documentacao/
│   ├── dataset_card.md
│   └── proveniencia.csv
└── README.md
```

Regras importantes:

- não sobrescrever o bruto com a versão limpa;
- não remover colunas do arquivo original antes de salvá-lo;
- registrar a data e, de preferência, a hora no nome do arquivo ou na proveniência;
- separar visualmente as pastas de bruto e tratado;
- guardar respostas de API e HTML original, não apenas o resultado convertido para DataFrame;
- explicar se o servidor devolveu redirecionamento, erro ou conteúdo parcial.

---

## 7. Limpeza e tratamento

A limpeza deve ser feita depois que os dados brutos estiverem salvos. Toda transformação relevante deve ser explicada no notebook e no dataset card.

Possíveis etapas:

- remoção de duplicatas justificadas;
- correção de tipos;
- conversão de datas e horários;
- padronização de nomes e categorias;
- tratamento de valores ausentes;
- conversão de unidades;
- remoção de registros inválidos;
- criação de variáveis derivadas;
- normalização da chave de integração;
- validação de intervalos plausíveis.

Não remova valores apenas porque são inconvenientes. Para cada descarte ou imputação, registre:

- quais registros foram afetados;
- qual regra foi usada;
- por que a regra era necessária;
- qual impacto pode ter causado na análise.

A base tratada deve possuir tipos coerentes e uma linha com significado claro. A granularidade precisa ser declarada, por exemplo: “cada linha representa um município” ou “cada linha representa um produto observado em uma data”.

---

## 8. Volume mínimo e qualidade da base

O PDF não fixa uma quantidade única de linhas, pois o volume depende do tema. Porém, a base deve ter substância para as análises futuras. Como referência inicial, considere:

- ordem de centenas de linhas;
- aproximadamente uma dezena de colunas;
- diversidade de variáveis, incluindo categóricas, numéricas, datas e texto quando fizer sentido.

O piso do volume deve ser acordado com o professor na aprovação do tema.

Mais importante que atingir números artificialmente é garantir que a base tenha:

- cobertura coerente;
- observações suficientes para comparação;
- dados de qualidade;
- documentação completa;
- integração válida;
- potencial de reutilização.

---

## 9. Proveniência e reprodutibilidade

A proveniência responde a três perguntas para cada fonte:

1. **De onde veio?** URL exata.
2. **Quando foi coletada?** Data e hora, preferencialmente com fuso horário.
3. **Como foi coletada?** Método, endpoint, parâmetros, seletores, paginação e demais configurações.

Um registro de proveniência pode ser uma tabela CSV, JSON ou Markdown com campos como:

| Campo | O que registrar |
|---|---|
| `fonte_id` | Identificador da fonte |
| `nome` | Nome legível da fonte |
| `url` | URL exata acessada |
| `data_hora_coleta` | Data, hora e fuso |
| `metodo` | API ou scraping |
| `endpoint_ou_seletor` | Endpoint e parâmetros ou seletores HTML |
| `arquivo_bruto` | Caminho do arquivo preservado |
| `status_http` | Código de resposta |
| `quantidade_registros` | Volume obtido |
| `observacoes` | Erros, limitações e decisões |

Exemplo de registro de proveniência para o projeto (três fontes):

| fonte_id | nome | url | metodo | endpoint_ou_seletor |
|---|---|---|---|---|
| 1 | IBGE/SIDRA | `https://sidra.ibge.gov.br/Tabela/61` | API | `api/ipca?...` |
| 2 | DIEESE | `https://www.dieese.org.br/analisecestabasica/` | Web scraping | Tabela HTML de cesta básica |
| 3 | TSE/Dados Abertos | `https://dadosabertos.tse.jus.br/api/3/action` | API | `package_show?id=candidatos-{ano}` |

O notebook também deve poder ser executado novamente por outra pessoa, considerando eventuais mudanças naturais nas fontes externas. Para isso, inclua dependências, parâmetros e instruções de execução.

---

## 10. Aspectos éticos e legais

### 10.1 `robots.txt`

Para cada site raspado:

1. localize o arquivo `robots.txt` no domínio;
2. verifique as regras aplicáveis ao robô ou agente utilizado;
3. confira se os caminhos pretendidos podem ser acessados;
4. registre a URL do `robots.txt`, a data da verificação e o que foi encontrado;
5. respeite as restrições.

O fato de uma página ser acessível no navegador não significa automaticamente que qualquer forma de coleta seja permitida.

### 10.2 Licença e termos de uso

Para cada fonte, identifique:

- licença dos dados, se houver;
- termos de uso do site ou da API;
- necessidade de atribuição;
- restrições à redistribuição;
- limites de requisições;
- proibições de uso comercial, quando aplicável;
- exigências relacionadas a marcas ou conteúdo protegido.

O dataset card deve dizer se o uso pretendido pelo trabalho é compatível com a licença ou com os termos encontrados. Não invente uma licença quando ela não estiver indicada; registre que a informação não foi localizada e discuta a consequência.

### 10.3 Dados pessoais e LGPD

Verifique se a coleta contém dados que identifiquem ou possam identificar pessoas. Se houver:

- colete apenas o necessário;
- não inclua dados pessoais sem justificativa;
- remova ou anonimize identificadores quando possível;
- evite nomes, e-mails, telefones, endereços e identificadores diretos;
- explique a minimização realizada;
- discuta as implicações da LGPD no dataset card.

Se não houver dados pessoais, declare isso explicitamente e explique brevemente por que os campos não identificam pessoas.

### 10.4 Carga sobre os servidores

Para não sobrecarregar os sites:

- faça somente as requisições necessárias;
- use pausas entre requisições;
- evite loops sem limite;
- use paginação de maneira controlada;
- não baixe arquivos que não serão utilizados;
- trate erros sem repetir requisições indefinidamente;
- respeite limites documentados da API.

---

## 11. Notebook de coleta

O notebook é o principal registro executável do trabalho. Ele deve ser comentado e conter, em uma sequência compreensível:

1. título, integrantes e objetivo;
2. pergunta motivadora;
3. bibliotecas e dependências;
4. configurações da coleta;
5. aquisição da fonte via API;  <!-- Fonte 1: IBGE/SIDRA -->
6. salvamento da resposta bruta da API;  <!-- Fonte 1: IBGE/SIDRA -->
7. aquisição da segunda fonte via API;  <!-- Fonte 3: TSE/Dados Abertos -->
8. salvamento da resposta bruta da segunda API;  <!-- Fonte 3: TSE -->
9. aquisição da fonte via HTML;  <!-- Fonte 2: DIEESE -->
10. salvamento do HTML ou arquivo bruto do scraping;  <!-- Fonte 2: DIEESE -->
11. leitura das fontes;
12. inspeção inicial dos dados;
11. normalização das chaves;
12. integração das fontes;
13. tratamento e limpeza;
14. validações de qualidade;
15. exportação da base tratada;
16. resumo das dimensões finais;
17. limitações e decisões importantes.

O notebook deve:

- tratar respostas HTTP inesperadas;
- informar erros de conexão ou conteúdo ausente;
- evitar depender de passos manuais não documentados;
- usar parâmetros claros;
- preservar o bruto antes do tratamento;
- produzir o mesmo tipo de saída quando executado novamente, salvo mudanças da fonte externa.

Antes da entrega, reinicie o kernel e execute todas as células na ordem. Isso ajuda a detectar variáveis que só funcionavam porque ficaram armazenadas de uma execução anterior.

---

## 12. Dataset card

O dataset card é a ficha descritiva da base. Ele deve ser fiel ao que o notebook realmente fez, sem preencher campos com suposições.

### A.1 Identificação

Inclua:

- nome curto e descritivo da base;
- grupo e integrantes;
- tema;
- pergunta motivadora;
- período da coleta.

### A.2 Fontes e proveniência

Para cada fonte, informe:

- nome e URL;
- método de aquisição;
- endpoint, parâmetros ou seletores;
- licença ou termos de uso;
- compatibilidade do uso pretendido;
- data e hora da coleta.

Também descreva:

- chave de integração;
- normalizações realizadas;
- tipo de join;
- tratamento das divergências e dos não casados.

### A.3 Dicionário de variáveis

Crie uma linha para cada variável da base tratada:

| Variável | Tipo | Descrição | Unidade |
|---|---|---|---|
| `nome_da_coluna` | categórica, numérica, data/hora, texto ou booleana | O que a coluna representa | unidade ou “não se aplica” |

Os tipos sugeridos pelo enunciado são:

- categórica;
- numérica contínua;
- numérica discreta;
- data/hora;
- texto;
- booleana.

### A.4 Volume e granularidade

Informe:

- número final de linhas;
- número final de colunas;
- o que cada linha representa;
- período, região ou universo coberto.

### A.5 Limitações e decisões

Registre:

- dados descartados e motivo;
- valores faltantes;
- campos incompletos;
- vieses de cobertura;
- limitações da API ou do site;
- transformações importantes;
- decisões que podem afetar análises futuras.

### A.6 Considerações éticas

Responda explicitamente:

- contém dados pessoais? Se sim, como foram tratados sob a LGPD?
- quais são as restrições de uso e redistribuição?
- o `robots.txt` foi verificado?
- o que foi encontrado?
- quais cuidados foram tomados para não sobrecarregar os servidores?

---

## 13. Estrutura recomendada da entrega

O grupo deve entregar um único repositório ou arquivo compactado contendo:

```text
entrega_trabalho_1/
├── notebook_coleta.ipynb
├── dados_brutos/
├── dados_tratados/
├── documentacao/
│   ├── dataset_card.md
│   └── proveniencia.csv
└── README.md
```

### 13.1 Notebook de coleta

Jupyter Notebook reprodutível, comentado, com aquisição, integração e limpeza.

### 13.2 Dados brutos

Arquivos crus de cada fonte, exatamente como foram coletados, na pasta `dados_brutos/`.

### 13.3 Base tratada

Base final, integrada e limpa, em CSV ou, preferencialmente, Parquet, na pasta `dados_tratados/`.

### 13.4 Registro de proveniência

Log de onde, quando e como cada dado foi coletado.

### 13.5 Dataset card

Ficha preenchida com identificação, fontes, dicionário, volume, limitações e ética.

### 13.6 README

Embora o PDF não liste o README como artefato obrigatório separado, é recomendável incluí-lo com:

- descrição do projeto;
- integrantes;
- estrutura das pastas;
- dependências;
- instruções para executar o notebook;
- localização dos dados brutos e tratados;
- observação sobre acesso à internet ou credenciais, se necessário.

Nunca inclua tokens, senhas ou chaves privadas no pacote entregue.

---

## 14. Checklist de planejamento

- [ ] Formar um grupo de 3 a 4 integrantes.
- [ ] Escolher um tema de interesse do grupo.
- [ ] Definir uma pergunta motivadora investigável.
- [ ] Identificar uma fonte acessível por API.
- [ ] Identificar uma fonte acessível por scraping de HTML.
- [ ] Confirmar que as duas fontes possuem uma chave de integração viável.
- [ ] Estimar o volume de linhas e colunas.
- [ ] Verificar limitações, licenças e termos de uso.
- [ ] Verificar o `robots.txt` do site que será raspado.
- [ ] Apresentar o tema e as fontes ao professor para aprovação.

---

## 15. Checklist de aquisição

- [ ] Registrar a URL exata da API.
- [ ] Registrar endpoint, parâmetros e paginação da API.
- [ ] Implementar tratamento de status HTTP e erros.
- [ ] Salvar a resposta bruta da API antes da limpeza.
- [ ] Registrar a URL exata da página HTML.
- [ ] Definir os seletores ou o critério de extração.
- [ ] Salvar o HTML ou o resultado bruto do scraping.
- [ ] Usar pausas entre requisições.
- [ ] Coletar somente o necessário.
- [ ] Registrar data, hora e fuso da coleta.
- [ ] Registrar o volume obtido por cada fonte.
- [ ] Confirmar que os arquivos brutos podem ser abertos e lidos.

---

## 16. Checklist de integração e limpeza

- [ ] Definir formalmente a chave de integração.
- [ ] Verificar o tipo da chave em cada fonte.
- [ ] Normalizar acentos, maiúsculas, espaços e grafias quando necessário.
- [ ] Registrar as regras de normalização.
- [ ] Verificar chaves duplicadas.
- [ ] Escolher e justificar o tipo de join.
- [ ] Medir quantos registros foram casados.
- [ ] Medir quantos registros ficaram sem correspondência.
- [ ] Investigar duplicações provocadas pelo join.
- [ ] Tratar valores ausentes com regra documentada.
- [ ] Corrigir tipos de datas, números e categorias.
- [ ] Verificar unidades e escalas.
- [ ] Registrar dados removidos e o motivo.
- [ ] Confirmar a granularidade final da base.
- [ ] Exportar a base integrada e tratada separadamente do bruto.

---

## 17. Checklist de ética e legalidade

- [ ] Consultar o `robots.txt` de cada site raspado.
- [ ] Registrar a data da consulta ao `robots.txt`.
- [ ] Registrar as regras relevantes encontradas.
- [ ] Identificar a licença ou os termos de cada fonte.
- [ ] Verificar se o uso acadêmico pretendido é permitido.
- [ ] Registrar exigências de atribuição ou redistribuição.
- [ ] Verificar a existência de dados pessoais.
- [ ] Aplicar minimização ou anonimização quando necessário.
- [ ] Documentar o tratamento sob a LGPD, se aplicável.
- [ ] Configurar pausas entre requisições.
- [ ] Evitar coleta excessiva e repetições desnecessárias.
- [ ] Remover credenciais, tokens e dados sensíveis do notebook entregue.

---

## 18. Checklist do notebook — atualizado em 19/09/2026

- [x] O notebook possui título, objetivo e descrição das fontes. **Pendente:** preencher os integrantes.
- [x] A pergunta motivadora está descrita.
- [x] As bibliotecas e dependências estão identificadas.
- [x] A coleta via API está implementada.
- [x] A coleta via HTML está implementada.
- [x] Os dados brutos são salvos antes da limpeza.
- [x] URLs, parâmetros e seletores estão registrados.
- [x] Erros e status HTTP são tratados.
- [x] A chave de integração está explicada.
- [x] O join e seus resultados são verificados.
- [x] As decisões de limpeza estão comentadas.
- [x] A base tratada é exportada.
- [ ] O notebook foi executado do início ao fim em um kernel reiniciado.
- [ ] Não existem células dependentes de execução manual não documentada. **Validar durante a execução limpa.**
- [x] As saídas finais mostram dimensões e verificações básicas.

---

## 19. Checklist do dataset card e da proveniência — atualizado em 19/09/2026

- [x] O nome da base é claro.
- [ ] Todos os integrantes estão listados. **Pendente:** substituir `Nome 1` a `Nome 4` pelos nomes reais.
- [x] O tema e a pergunta motivadora estão descritos.
- [x] O período da coleta está informado.
- [x] Todas as fontes possuem URL exata.
- [x] O método de cada fonte está descrito.
- [x] Endpoint, parâmetros ou seletores foram registrados.
- [x] Licenças e termos de uso foram registrados.
- [x] A chave de integração está explicada.
- [x] O tratamento das divergências foi descrito.
- [x] O dicionário contém uma linha por coluna tratada.
- [x] Os tipos e unidades estão informados.
- [x] O número final de linhas e colunas está correto: 4.757 × 35.
- [x] A unidade de observação está clara: capital × mês.
- [x] A cobertura está descrita.
- [x] Dados descartados e limitações estão documentados.
- [x] Valores faltantes e vieses conhecidos estão documentados.
- [x] As decisões de limpeza relevantes estão documentadas.
- [x] A presença ou ausência de dados pessoais foi declarada.
- [x] Restrições de uso e redistribuição estão descritas.
- [x] A verificação do `robots.txt` está registrada.
- [x] A proveniência informa onde, quando e como cada fonte foi coletada.

---

## 20. Checklist final antes da entrega — atualizado em 19/09/2026

- [x] O pacote contém pelo menos duas fontes realmente distintas. <!-- Este projeto utiliza três fontes -->
- [x] Uma fonte foi obtida via API. <!-- IBGE/SIDRA e TSE/Dados Abertos -->
- [x] Uma fonte foi obtida via scraping de HTML. <!-- DIEESE -->
- [x] As fontes estão integradas em uma base única. <!-- 4.757 linhas e 35 colunas -->
- [x] O join usa uma chave explicada e validada.
- [x] Os arquivos brutos estão presentes e intactos.
- [x] A base tratada está separada do bruto.
- [ ] O notebook é reprodutível. **Executar todas as células em kernel reiniciado.**
- [x] O notebook trata erros e status HTTP.
- [x] A coleta respeita pausas e limitações do servidor.
- [x] O `robots.txt` foi verificado e documentado.
- [x] Licenças e termos de uso foram analisados.
- [x] Dados pessoais foram evitados, minimizados ou anonimizados.
- [x] O registro de proveniência está completo.
- [x] O dataset card está completo e consistente com a base gerada.
- [ ] O volume foi conferido com o professor, quando necessário.
- [x] O pacote não contém senhas, tokens ou chaves privadas.
- [ ] Todos os caminhos e instruções do README foram testados após a reorganização final.
- [ ] O arquivo final pode ser aberto e executado em um ambiente limpo.
- [ ] A entrega segue o prazo e o formato definidos pelo professor.

### Pendências objetivas

1. Substituir os nomes fictícios dos integrantes no [README](../projeto/README.md) e no dataset card.
2. Abrir `projeto/notebook_coleta.ipynb`, reiniciar o kernel e executar todas as células em ordem.
3. Conferir as saídas finais do notebook: dimensões, chaves, duplicatas, valores ausentes e arquivos exportados.
4. Testar a abertura do pacote em um ambiente limpo e confirmar o formato exigido pelo professor, indicado como ColabWeb.
5. Depois dessas verificações, revisar o `git status`, criar o commit final e enviar para o repositório remoto.

**Prazo indicado no PDF:** 10/09/2026.  
**Forma de entrega indicada no PDF:** ColabWeb.

---

## 21. Critérios usados na avaliação

A rubrica do trabalho avalia principalmente quatro eixos:

### Qualidade técnica da coleta

Um trabalho forte tem código correto e reprodutível, tratamento de status HTTP e erros, além de paginação e parâmetros quando necessários.

### Integração das fontes

Um trabalho forte cruza as fontes com uma chave adequada e explica divergências, perdas e falhas de casamento.

### Tratamento e limpeza

Um trabalho forte aplica limpeza justificada, usa tipos corretos, documenta decisões e preserva o bruto separado do tratado.

### Documentação

Um trabalho forte apresenta dataset card completo e fiel, além de uma proveniência que permite reconstruir a coleta.

O maior risco é entregar uma solução que parece funcionar, mas não pode ser auditada ou reproduzida. A qualidade da documentação e a preservação do bruto são tão importantes quanto o código de coleta.
