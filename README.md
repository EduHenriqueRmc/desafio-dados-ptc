# Desafio: Do dado bagunçado ao dado útil (Etapa 1)

Tratamento da planilha de pedidos da **Metalúrgica Mezzalira** para descobrir **qual cidade mais comprou e em qual mês**, seguindo a arquitetura em camadas **Bronze, Prata e Ouro**.

> Projeto de treinamento da Trilha de Dados do CITi. Os dados são fictícios.

## Resposta

**A cidade que mais comprou foi Recife, com R$ 55.260,00. O mês em que ela mais comprou foi março (R$ 29.730,00).**

- 📊 Planilha com as abas Bronze, Prata, Log e Ouro: https://docs.google.com/spreadsheets/d/1m5CnZfPtHr8mNU8MCpTmPJ7E8e9WhKXI/edit?usp=sharing&ouid=118407572818330874924&rtpof=true&sd=true

## Sobre o desafio

A planilha original tem cerca de 60 linhas e cinco problemas plantados de propósito:

1. Pedidos duplicados
2. Datas em formatos diferentes
3. A mesma cidade escrita de jeitos diferentes (`Recife`, `recife`, `REC`)
4. Valores digitados como texto (`R$ 1.200,00`)
5. Linhas vazias

## Camadas

| Camada | O que é | Arquivo |
|:---|:---|:---|
| 🥉 **Bronze** | Cópia intocada da planilha original. Nunca é alterada. | `pedidos_metalurgica_mezzalira.xlsx` |
| 🥈 **Prata** | Dados limpos, com os cinco problemas corrigidos. | `prata.xlsx` |
| 📝 **Log** | Registro de cada correção, com a quantidade de linhas afetadas. | `log.xlsx` |
| 🥇 **Ouro** | Tabela dinâmica com o faturamento por cidade e por mês. | `ouro.xlsx` |

A Prata é feita a partir de uma **cópia** da Bronze (`prata = bronze.copy()`), então o original nunca é modificado.

## Estrutura do repositório

```
.
├── main.py                                  # tratamento completo (Bronze → Prata → Log → Ouro)
├── pedidos_metalurgica_mezzalira.xlsx       # Bronze (original, intocado)
├── prata.xlsx                               # saída: dados limpos
├── log.xlsx                                 # saída: log de correções
├── ouro.xlsx                                # saída: tabela dinâmica
└── README.md
```

## Como executar

**Requisitos:** Python 3.10 ou superior.

```bash
# 1. clonar o repositório
git clone <URL-DO-REPOSITORIO>
cd <NOME-DO-REPOSITORIO>

# 2. criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. instalar as dependências
pip install pandas openpyxl

# 4. rodar
python main.py
```

O script lê a Bronze, aplica os tratamentos e gera `prata.xlsx`, `log.xlsx` e `ouro.xlsx` na mesma pasta.

## Tratamentos aplicados (Prata)

| # | Problema | O que foi feito | Como |
|:-:|:---|:---|:---|
| 1 | Linhas vazias | Removidas as linhas sem nenhum dado | `dropna(how="all")` |
| 2 | Pedidos duplicados | Mantida só a primeira ocorrência de cada linha repetida | `drop_duplicates()` |
| 3 | Cidade escrita de jeitos diferentes | `recife` e `REC` padronizados para `Recife` | `replace()` com dicionário de correções |
| 4 | Valores salvos como texto | Removido o `R$` e convertido para número | função `converte_valor` |
| 5 | Datas em formatos diferentes | Mês escrito (`fev`) trocado por número e datas convertidas para o padrão `AAAA-MM-DD` | dicionário de meses + `pd.to_datetime` por formato |

Todas as correções são registradas pela função `registrar()`, que alimenta o Log.

## Conferência

Para garantir que nenhuma linha se perdeu na tabela dinâmica, o total da Ouro deve ser igual à soma da Prata:

```python
print(ouro.loc["Total", "Total"], prata["Valor (R$)"].sum())
```

## Tecnologias

- Python
- pandas
- openpyxl

## Autor

**Eduardo Henrique do Rêgo** · [GitHub](https://github.com/EduHenriqueRmc) · [LinkedIn](https://www.linkedin.com/in/eduardo-henrique-do-r%C3%AAgo-255984350/)

Desafio proposto por Guilherme Muniz · Trilha de Dados do CITi.
