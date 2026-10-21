import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Slider
import numpy as np

from data_loading import load_ecg_signal


def plot_ecg_interactive(
    record_names: list[str],
    data_dir: str = "./mitdb",
    db_name: str = "MIT-BIH Arrhythmia Database",
) -> tuple[RangeSlider, Slider]:
    """
    Interaktivně zobrazí EKG signál s možností posuvu v čase a přepínání záznamů.

    Vytvoří okno Matplotlib s EKG křivkami dostupných svodů a dvěma
    interaktivními widgety pod grafem:
    - **RangeSlider (Čas [s])**: Umožňuje zvolit počáteční a koncový čas výřezu.
    - **Slider (Záznam)**: Přepíná mezi záznamy ze seznamu `record_names`.

    Při změně záznamu se dynamicky načtou nová data a automaticky se přizpůsobí
    maximální rozsah časového posuvníku podle délky nového záznamu.

    Parameters
    ----------
    record_names : list of str
        Seznam ID nebo názvů záznamů k zobrazení (např. ['100', '101', '102']).
        Seznam nesmí být prázdný.
    data_dir : str, default './mitdb'
        Cesta k lokální složce se soubory databáze.
    db_name : str, default 'MIT-BIH Arrhythmia Database'
        Hlavní nadpis grafu (zobrazuje se v horní části okna).

    Returns
    -------
    tuple[RangeSlider, Slider]
        Dvojice instancí `(time_slider, rec_slider)`. Odkazy na tyto objekty
        je nutné uložit do proměnné v volající vrstvě, aby je garbage collector
        Pythonu neodstranil z paměti, což by způsobilo nefunkčnost interaktivity.

    Raises
    ------
    ValueError
        Pokud je parametr `record_names` prázdný seznam.
    FileNotFoundError
        Pokud vybraný záznam neexistuje v zadané složce `data_dir`.

    Examples
    --------
    >>> records = ["100", "101", "102"]
    >>> t_slider, r_slider = plot_ecg_interactive(records, data_dir="./.mitdb")
    """

    if not record_names:
        raise ValueError("Seznam 'record_names' nesmí být prázdný.")

    fig, ax = plt.subplots(figsize=(11, 6))
    plt.subplots_adjust(bottom=0.25)
    fig.suptitle(db_name, fontsize=14, fontweight="bold")

    # Načtení prvního záznamu pro inicializaci
    init_rec = record_names[0]
    full_signal, fs = load_ecg_signal(init_rec, data_dir=data_dir)
    total_duration = len(full_signal) / fs

    # Osy pro posuvníky
    ax_time = plt.axes([0.15, 0.1, 0.7, 0.03])
    ax_rec = plt.axes([0.15, 0.03, 0.7, 0.03])

    time_slider = RangeSlider(
        ax_time,
        "Čas [s]",
        0.0,
        total_duration,
        valinit=(0.0, min(10.0, total_duration)),
    )
    rec_slider = Slider(
        ax_rec, "Záznam", 0, len(record_names) - 1, valinit=0, valstep=1
    )

    def draw_plot(rec_name: str, t_start: float, t_end: float):
        ax.clear()
        s_from = int(t_start * fs)
        s_to = int(t_end * fs)

        signal, current_fs = load_ecg_signal(
            rec_name, data_dir=data_dir, sampfrom=s_from, sampto=s_to
        )
        time_axis = np.linspace(t_start, t_end, num=len(signal))

        for ch_idx in range(signal.shape[1]):
            ax.plot(time_axis, signal[:, ch_idx], label=f"Svod {ch_idx + 1}")

        ax.set_title(f"Záznam: {rec_name}", fontsize=12)
        ax.set_xlabel("Čas [s]")
        ax.set_ylabel("Napětí [mV]")
        ax.grid(True)
        if signal.shape[1] > 1:
            ax.legend(loc="upper right")

    def update(val):
        nonlocal total_duration, fs
        rec_idx = int(rec_slider.val)
        rec_name = record_names[rec_idx]

        full_sig, fs = load_ecg_signal(rec_name, data_dir=data_dir)
        new_duration = len(full_sig) / fs

        if new_duration != total_duration:
            total_duration = new_duration
            time_slider.valmax = total_duration
            time_slider.ax.set_xlim(0.0, total_duration)

        t_start, t_end = time_slider.val
        draw_plot(rec_name, t_start, t_end)
        fig.canvas.draw_idle()

    draw_plot(init_rec, 0.0, min(10.0, total_duration))

    time_slider.on_changed(update)
    rec_slider.on_changed(update)

    plt.show()

    return time_slider, rec_slider
