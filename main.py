import requests
import csv
import difflib

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
response = requests.get(url)
municipios_ibge = response.json()
nomes_municipios = [m["nome"] for m in municipios_ibge]

print("Municipios carregados:", len(municipios_ibge))

saida = open("resultado.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(saida)

writer.writerow([
    "municipio_input",
    "populacao_input",
    "municipio_ibge",
    "uf",
    "regiao",
    "id_ibge",
    "status"
])

total_municipios = 0
total_ok = 0
total_nao_encontrado = 0
total_erro_api = 0
pop_total_ok = 0

pop_por_regiao = {}
count_por_regiao = {}

with open("input.csv", newline="", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:

        total_municipios += 1
        nome_csv = linha["municipio"]
        populacao = linha["populacao"]

        melhor_match = difflib.get_close_matches(nome_csv, nomes_municipios, n=1, cutoff=0.8)

        if melhor_match:
            municipio_encontrado = None

            for m in municipios_ibge:
                if m["nome"] == melhor_match[0]:
                    municipio_encontrado = m
                    break

            codigo_ibge = municipio_encontrado["id"]
            nome_oficial = municipio_encontrado["nome"]
            uf = municipio_encontrado["microrregiao"]["mesorregiao"]["UF"]["sigla"]
            regiao = municipio_encontrado["microrregiao"]["mesorregiao"]["UF"]["regiao"]["nome"]

            total_ok += 1
            pop_total_ok += int(populacao)

            if regiao not in pop_por_regiao:
                pop_por_regiao[regiao] = 0
                count_por_regiao[regiao] = 0

            pop_por_regiao[regiao] += int(populacao)
            count_por_regiao[regiao] += 1

            writer.writerow([
                nome_csv,
                populacao,
                nome_oficial,
                uf,
                regiao,
                codigo_ibge,
                "OK"
            ])

            print(nome_csv, "->", nome_oficial, "|", uf, "|", regiao, "|", codigo_ibge)

        else:
            total_nao_encontrado += 1
            writer.writerow([
                nome_csv,
                populacao,
                "",
                "",
                "",
                "",
                "NAO_ENCONTRADO"
            ])
            print(nome_csv, "-> não encontrado")

    medias_por_regiao = {}

    for regiao in pop_por_regiao:
        medias_por_regiao[regiao] = pop_por_regiao[regiao] / count_por_regiao[regiao]
    
    stats = {
        "total_municipios": total_municipios,
        "total_ok": total_ok,
        "total_nao_encontrado": total_nao_encontrado,
        "total_erro_api": total_erro_api,
        "pop_total_ok": pop_total_ok,
        "medias_por_regiao": medias_por_regiao
    }

    payload = {
        "stats": stats
    }

    ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImR0TG03UVh1SkZPVDJwZEciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL215bnhsdWJ5a3lsbmNpbnR0Z2d1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI0NTRlZDVlZS1iNjZmLTQzYmYtYWQ1NC0wM2ZmM2EwZDllOGQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzczMzUzNjI5LCJpYXQiOjE3NzMzNTAwMjksImVtYWlsIjoidGhlb3Byb2NoYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGhlb3Byb2NoYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibm9tZSI6IlRoZW8gUGVyZWlyYSBkYSBSb2NoYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiNDU0ZWQ1ZWUtYjY2Zi00M2JmLWFkNTQtMDNmZjNhMGQ5ZThkIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NzMzNTAwMjl9XSwic2Vzc2lvbl9pZCI6ImI0ZGM4MjgzLThlMDMtNDZlYS05MjE3LTQ4Njk2ZWQzZTRjMiIsImlzX2Fub255bW91cyI6ZmFsc2V9.hnRTYzL7ISMAnlItIMKRtQAqaVIhnYpxSIknGOzu9Xs"

    print("Total municipios:", total_municipios)
    print("Total OK:", total_ok)
    print("Total nao encontrado:", total_nao_encontrado)
    print("Total erro api:", total_erro_api)
    print("Pop total OK:", pop_total_ok)
    print("Medias por regiao:", medias_por_regiao)

url_submit = "https://mynxlubykylncinttggu.functions.supabase.co/ibge-submit"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(url_submit, json=payload, headers=headers)

resultado = response.json()

print("Score:", resultado["score"])
print("Feedback:", resultado["feedback"])


saida.close()
