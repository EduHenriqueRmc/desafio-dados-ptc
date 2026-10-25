import pandas as pd

# Bronze
bronze = pd.read_excel('pedidos_metalurgica_mezzalira.xlsx')

# Prata e Log
prata = bronze.copy()
log = []

def registrar(problema, o_que_fizemos, linhas_afetadas, justificativa = None):
    log.append({
        "O que encontrei": problema,
        "O que fiz": o_que_fizemos,
        "Linhas afetadas": int(linhas_afetadas),
        "Justificativa (Se houve dúvida)": justificativa
    })
    print(f"{problema}: {linhas_afetadas} linha(s) afetada(s)")

# Tratar linhas vazias
antes = len(prata)
prata = prata.dropna(how='all')
vazios_afetados = antes - len(prata)
registrar("Linhas vazias", "Removi linhas completamente vazias", vazios_afetados)

# Tratar duplicados
antes = len(prata)
prata = prata.drop_duplicates()
duplicados_afetados = antes - len(prata)
registrar("Duplicados", "Removi linhas duplicadas", duplicados_afetados)

# Tratar nomes inconsistentes
correcoes = {
    "recife": "Recife",
    "REC": "Recife",
}

antes = prata["Cidade"].copy()
prata["Cidade"] = prata["Cidade"].replace(correcoes)

linhas_corrigidas = (antes != prata["Cidade"]).sum()
registrar("Mesma cidade escrita de jeitos diferentes", "Padronizei recife e REC para Recife", linhas_corrigidas, '"Recife" foi o padrão pois não está abreviado e começa com letra maiúscula')

# Tratar valores inconsistentes
def converte_valor(texto):
    if isinstance(texto, (int, float)):
        return float(texto)
    texto = texto.replace("R$", "").strip()
    texto = texto.replace(".", "").replace(",", ".")
    return float(texto)

eram_texto = prata["Valor (R$)"].str.contains("R$", regex=False).sum()
prata["Valor (R$)"] = prata["Valor (R$)"].apply(converte_valor)

registrar("Valores salvos como texto", "Tirei o R$ e converti para número", eram_texto,)

# Tratar datas inconsistentes
meses = {"jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06",
         "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"}
datas = prata["Data"].replace(meses, regex=True)

formato_barra   = pd.to_datetime(datas, format="%d/%m/%Y", errors="coerce")
formato_iso     = pd.to_datetime(datas, format="%Y-%m-%d", errors="coerce")
formato_tracinho = pd.to_datetime(datas, format="%d-%m-%Y", errors="coerce")

fora_do_padrao = formato_barra.isna().sum()

prata["Data"] = formato_barra.fillna(formato_iso).fillna(formato_tracinho)

registrar("Datas em formatos diferentes", "Converti os três formatos para data de verdade", fora_do_padrao, "Usei o formato YYYY-MM-DD pois é o padrão usado para datas")

# Exportar planilha prata
prata.to_excel("prata.xlsx", index=False)
# Exportar log de correções
pd.DataFrame(log).to_excel("log.xlsx", index=False)

# Ouro
base = prata.assign(mes=prata["Data"].dt.month)

ouro = base.pivot_table(
    index="Cidade",
    columns="mes",
    values="Valor (R$)",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total",
)

nomes_meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
               7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
ouro = ouro.rename(columns=nomes_meses)

# Exportar planilha ouro
ouro.to_excel("ouro.xlsx")

# Resposta
cidades = ouro.drop(index="Total")
cidade_campea = cidades["Total"].idxmax()
melhor_mes = cidades.drop(columns="Total").loc[cidade_campea].idxmax()
cidade_mes = f"A cidade que mais comprou foi {cidade_campea}, no mês de {melhor_mes}"
print(cidade_mes)
