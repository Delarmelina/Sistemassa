from pathlib import Path

restaurante_id = 1

def get_dbpath():
    # Define o caminho base como o diretório raiz do projeto (pasta Sistemassa)
    base_dir = Path(__file__).resolve().parent.parent  # Sobe um nível para alcançar "Sistemassa"
    # Caminho para o banco de dados
    db_path = base_dir / "db" / "estoque.db"
    return db_path

def get_restaurante():
    return restaurante_id

def set_restaurante(restaurante):
    global restaurante_id
    restaurante_id = restaurante


