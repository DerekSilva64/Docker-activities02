import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# CONFIGURAÇÃO DOS TESTES
# ================================
USUARIOS = [10, 50, 100]          # Cargas crescentes
INSTANCIAS = [1, 2, 3]              # N° de instâncias do WordPress
HOSTS = {
    1: "http://wp_nginx",
    2: "http://wp_nginx",      # ou o domínio balanceado entre wp1/wp2
    3: "http://wp_nginx"       # idem, balanceado se aplicável
}
TEMPO_TESTE = "1m"                  # Duração de cada cenário
RESULT_DIR = "locust\\results"

# Cria pasta de resultados
os.makedirs(RESULT_DIR, exist_ok=True)

# ================================
# EXECUÇÃO AUTOMÁTICA DOS TESTES
# ================================
def run_locust_test(host, users, instancias):
    csv_prefix = f"{RESULT_DIR}/wp{instancias}_{users}users"
    print(f"\n🚀 Executando teste: {users} usuários | {instancias} instância(s) | {host}")

    cmd = [
        "docker", "exec", "wp_locust",
        "locust", "-f", "locustfile.py",
        "--headless",
        "-u", str(users),
        "-r", "10",
        "-t", TEMPO_TESTE,
        "--csv", f"/mnt/locust/{csv_prefix}",
        "--host", host
    ]
    subprocess.run(cmd, check=True)
    print("✅ Teste concluído e CSV salvo.\n")

# ================================
# GERAÇÃO DOS GRÁFICOS
# ================================
def plot_results():
    print("📊 Gerando gráficos...")

    metricas = ["Average Response Time"]
    for metrica in metricas:
        plt.figure(figsize=(10, 6))
        for instancias in INSTANCIAS:
            valores_x = []
            valores_y = []
            for usuarios in USUARIOS:
                arquivo = f"{RESULT_DIR}\\wp{instancias}_{usuarios}users_stats.csv"
                if not os.path.exists(arquivo):
                    continue
                df = pd.read_csv(arquivo)
                media = df[metrica].mean()
                valores_x.append(usuarios)
                valores_y.append(media)
            plt.plot(valores_x, valores_y, marker='o', label=f"{instancias} instância(s)")

        plt.title(f"{metrica} × Número de Usuários")
        plt.xlabel("Usuários simultâneos")
        plt.ylabel(metrica)
        plt.legend()
        plt.grid(True)
        plt.ylim((1, 2000))
        plt.xlim((1, 120))
        plt.tight_layout()
        # plt.savefig(f"{RESULT_DIR}/{metrica.replace(' ', '_')}.png")
        # plt.close()
    plt.show()
    print("Gráficos gerados em ./locust/results/")


if __name__ == "__main__":
    # for instancias in INSTANCIAS:
    #     for usuarios in USUARIOS:
    #         run_locust_test(HOSTS[instancias], usuarios, instancias)

    plot_results()
