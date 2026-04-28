import re
import unicodedata
from pathlib import Path

import pandas as pd
from sqlalchemy import text

try:
    from .config import BASE_DIR, CSV_PATH
    from .database import get_engine
except ImportError:
    from config import BASE_DIR, CSV_PATH
    from database import get_engine


def limpar_nome_coluna(nome):
    nome = str(nome).strip().lower()
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    nome = re.sub(r"[^a-z0-9]+", "_", nome)
    return nome.strip("_")


def encontrar_coluna(colunas, opcoes, permitir_parcial=True):
    for opcao in opcoes:
        if opcao in colunas:
            return opcao

    if not permitir_parcial:
        return None

    for coluna in colunas:
        for opcao in opcoes:
            if opcao in coluna:
                return coluna

    return None


def executar_sql(caminho_sql, engine):
    sql = Path(caminho_sql).read_text(encoding="utf-8")
    comandos = [comando.strip() for comando in sql.split(";") if comando.strip()]

    with engine.begin() as conexao:
        for comando in comandos:
            conexao.execute(text(comando))


def preparar_dados(df):
    df.columns = [limpar_nome_coluna(coluna) for coluna in df.columns]
    colunas = list(df.columns)

    coluna_device = encontrar_coluna(
        colunas,
        ["device_id", "device", "room_id", "room_id_id", "id", "sensor_id"],
    )
    coluna_timestamp = encontrar_coluna(
        colunas,
        ["timestamp", "noted_date", "date", "data", "datetime", "time", "ts"],
    )
    coluna_temperature = encontrar_coluna(
        colunas,
        ["temperature", "temperatura", "temp", "reading", "value"],
    )
    coluna_location = encontrar_coluna(
        colunas,
        ["location", "localizacao", "local", "room", "out_in", "ambiente"],
        permitir_parcial=False,
    )

    if coluna_temperature is None:
        raise ValueError("Nenhuma coluna de temperatura foi encontrada no CSV.")

    dados = pd.DataFrame()
    dados["device_id"] = df[coluna_device].astype(str) if coluna_device else "sem_dispositivo"
    dados["timestamp"] = pd.to_datetime(df[coluna_timestamp], errors="coerce", dayfirst=True) if coluna_timestamp else pd.NaT
    dados["temperature"] = pd.to_numeric(df[coluna_temperature], errors="coerce")
    dados["location"] = df[coluna_location].astype(str) if coluna_location else "nao_informado"

    dados = dados.dropna(subset=["timestamp", "temperature"])
    dados = dados.drop_duplicates(subset=["device_id", "timestamp", "temperature", "location"])

    if dados.empty:
        raise ValueError("Depois da limpeza, nenhum registro valido sobrou para inserir.")

    return dados


def main():
    print("Lendo arquivo CSV...")

    if not CSV_PATH.exists():
        print(f"Arquivo nao encontrado: {CSV_PATH}")
        print("Baixe o CSV do Kaggle e salve como data/temperature_readings.csv")
        return

    df = pd.read_csv(CSV_PATH)
    print("Colunas encontradas:")
    print(", ".join(df.columns))

    print("Padronizando dados...")
    dados = preparar_dados(df)

    engine = get_engine()

    print("Criando tabela...")
    executar_sql(BASE_DIR / "sql" / "create_table.sql", engine)

    print("Limpando tabela antiga...")
    with engine.begin() as conexao:
        conexao.execute(text("TRUNCATE TABLE temperature_readings RESTART IDENTITY;"))

    print("Inserindo dados no banco...")
    dados.to_sql("temperature_readings", engine, if_exists="append", index=False)

    print("Criando views...")
    executar_sql(BASE_DIR / "sql" / "create_views.sql", engine)

    print(f"Total de registros inseridos: {len(dados)}")
    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()
