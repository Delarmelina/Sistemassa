from pathlib import Path

usuario_id = None
restaurante_id = None

def get_dbpath():
    # Define o caminho base como o diretório raiz do projeto (pasta Sistemassa)
    base_dir = Path(__file__).resolve().parent.parent  # Sobe um nível para alcançar "Sistemassa"
    # Caminho para o banco de dados
    db_path = base_dir / "db" / "estoque.db"
    return db_path

def get_restaurante():
    if restaurante_id is None:
        return None
    return restaurante_id

def set_restaurante(restaurante):
    global restaurante_id
    restaurante_id = restaurante

def get_usuario_id():
    if usuario_id is None:
        return None
    return usuario_id

def set_usuario_id(usuario):
    global usuario_id
    usuario_id = usuario