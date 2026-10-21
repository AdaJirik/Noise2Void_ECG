import os
import wfdb

from data_loading import get_available_records
from graph_plotting import plot_ecg_interactive

DATA_DIR = "./mitdb"

if __name__ == "__main__":
    available_records = get_available_records(DATA_DIR)

    if not available_records:
        print(f"Složka '{DATA_DIR}' neobsahuje žádná data. Stahuji MIT-BIH databázi...")
        wfdb.dl_database("mitdb", dl_dir=DATA_DIR)
        available_records = get_available_records(DATA_DIR)

    print(f"Nalezeno {len(available_records)} záznamů: {available_records}")

    _ = plot_ecg_interactive(
        record_names=available_records,
        data_dir=DATA_DIR,
        db_name="MIT-BIH Arrhythmia Database",
    )
    