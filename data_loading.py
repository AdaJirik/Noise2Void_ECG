import os
import wfdb
import numpy as np


def get_available_records(data_dir: str = "./mitdb") -> list[str]:
    """
    Načte seznam všech dostupných EKG záznamů ze souboru RECORDS.

    Parameters
    ----------
    data_dir : str, default './mitdb'
        Cesta k lokální složce s databází obsahující soubor RECORDS.

    Returns
    -------
    records : list of str
        Seznam názvů dostupných záznamů (např. ['100', '101', '102']).
    """
    records_file = os.path.join(data_dir, "RECORDS")

    if not os.path.isfile(records_file):
        return []

    with open(records_file, "r", encoding="utf-8") as f:
        records = [line.strip() for line in f if line.strip()]

    return records


def load_ecg_signal(
    record_name: str,
    data_dir: str = "./mitdb",
    channels: list[int] | None = None,
    sampfrom: int = 0,
    sampto: int | None = None,
) -> tuple[np.ndarray, int]:
    """
    Načte EKG signál z lokálního souboru MIT-BIH databáze.

    Parameters
    ----------
    record_name : str
        Název nebo ID záznamu (např. '100').
    data_dir : str, default './mitdb'
        Cesta k lokální složce se soubory databáze.
    channels : list of int, optional
        Indexy svodů k načtení (např. [0] pro první svod MLII). Pokud je None,
        načtou se všechny svody.
    sampfrom : int, default 0
        Počáteční index vzorku.
    sampto : int or None, default None
        Koncový index vzorku. Pokud je None, načte se až do konce.

    Returns
    -------
    signal : np.ndarray
        NumPy pole s naměřeným napětím v mV (tvar: [vzorky, svody]).
    fs : int
        Vzorkovací frekvence v Hz (u MIT-BIH je to 360 Hz).
    """
    record_path = os.path.join(data_dir, record_name)

    record = wfdb.rdrecord(
        record_path, channels=channels, sampfrom=sampfrom, sampto=sampto
    )

    return record.p_signal, record.fs
