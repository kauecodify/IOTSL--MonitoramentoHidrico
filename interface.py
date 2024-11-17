# Bibliotecas paho-mqtt, RPi.GPIO e Adafruit-ADS1x15
# pip install paho-mqtt RPi.GPIO Adafruit-ADS1x15 matplotlib
# pip install matplotlib

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
from matplotlib.widgets import Button

LIMITE_TURBIDEZ = 50.0
LIMITE_PH_MIN = 6.5
LIMITE_PH_MAX = 8.5
LIMITE_NIVEL_MIN = 50.0
LIMITE_NIVEL_MAX = 150.0

turbidez_data = []
ph_data = []
nivel_data = []
tempo_data = []

def ler_sensores():
    turbidez = random.uniform(0, 100)
    ph = random.uniform(3.0, 7.0)
    nivel = random.uniform(30, 180)
    return {"turbidez": turbidez, "ph": ph, "nivel": nivel}

def atualizar(frame):
    global tempo_data, turbidez_data, ph_data, nivel_data

    dados = ler_sensores()
    tempo_data.append(time.time())
    turbidez_data.append(dados["turbidez"])
    ph_data.append(dados["ph"])
    nivel_data.append(dados["nivel"])

    if len(tempo_data) > 100:
        tempo_data = tempo_data[-100:]
        turbidez_data = turbidez_data[-100:]
        ph_data = ph_data[-100:]
        nivel_data = nivel_data[-100:]

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(tempo_data, turbidez_data, label="Turbidez (NTU)", color="blue")
    ax1.axhline(LIMITE_TURBIDEZ, color="red", linestyle="--", label="Limite Máx.")
    ax1.set_title("Turbidez")
    ax1.set_ylabel("NTU")
    ax1.legend()

    ax2.plot(tempo_data, ph_data, label="pH", color="green")
    ax2.axhline(LIMITE_PH_MIN, color="orange", linestyle="--", label="pH Mín.")
    ax2.axhline(LIMITE_PH_MAX, color="red", linestyle="--", label="pH Máx.")
    ax2.set_title("pH")
    ax2.set_ylabel("pH")
    ax2.legend()

    ax3.plot(tempo_data, nivel_data, label="Nível (cm)", color="purple")
    ax3.axhline(LIMITE_NIVEL_MIN, color="orange", linestyle="--", label="Nível Mín.")
    ax3.axhline(LIMITE_NIVEL_MAX, color="red", linestyle="--", label="Nível Máx.")
    ax3.set_title("Nível da Água")
    ax3.set_ylabel("cm")
    ax3.set_xlabel("Tempo (s)")
    ax3.legend()

def toggle_background(event):
    current_color = fig.get_facecolor()
    new_color = 'black' if current_color == 'white' else 'white'
    fig.patch.set_facecolor(new_color)
    ax1.set_facecolor(new_color)
    ax2.set_facecolor(new_color)
    ax3.set_facecolor(new_color)
    plt.draw()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
fig.tight_layout(pad=3.0)

ax_button = plt.axes([0.85, 0.01, 0.1, 0.05])  # Posiciona o botão
button = Button(ax_button, 'Alterar fundo')

button.on_clicked(toggle_background)

ani = animation.FuncAnimation(fig, atualizar, interval=10)

plt.show()
