import os
import sys

def criar_modulo(nome_modulo, diretorio_base):
    """
    Cria a estrutura de pastas e arquivos para um novo módulo.
    """
    # Caminho completo da pasta do módulo
    caminho_modulo = os.path.join(diretorio_base, nome_modulo)

    # Cria a pasta do módulo se ela não existir
    os.makedirs(caminho_modulo, exist_ok=True)
    print(f"📂 Diretório verificado/criado: {caminho_modulo}")

    # Lista de arquivos padrão
    arquivos = [
        "repository.py",
        "router.py",
        "schemas.py",
        "service.py",
        "__init__.py"
    ]

    # Cria cada arquivo dentro da pasta do módulo
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho_modulo, arquivo)
        
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                pass 
            print(f"  📄 Arquivo criado: {arquivo}")
        else:
            print(f"  ⚠️ Arquivo já existe (ignorado): {arquivo}")

    print(f"\n✅ Módulo '{nome_modulo}' configurado com sucesso!")

if __name__ == "__main__":

    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    
    caminho_modules = os.path.abspath(os.path.join(diretorio_script, "..", "modules"))

    # Verifica se os nomes dos módulos foram passados como argumento no terminal
    if len(sys.argv) > 1:
        # Pega todos os argumentos passados após o nome do script
        nomes_dos_modulos = sys.argv[1:]
        
        # Roda a função para cada módulo listado no comando
        for nome_do_modulo in nomes_dos_modulos:
            criar_modulo(nome_do_modulo, diretorio_base=caminho_modules)
    else:
        nome_do_modulo = input("Digite o nome do novo módulo (ex: Users, Finance): ").strip()

        if nome_do_modulo:
            criar_modulo(nome_do_modulo, diretorio_base=caminho_modules)
            
        else:
            print("❌ Erro: O nome do módulo não pode estar vazio.")