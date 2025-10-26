import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Optional, Tuple
from matplotlib.figure import Figure


def generate_chart(
    csv_file: str | pd.DataFrame,
    group_field: str,
    value_field: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    palette: str = "Set2",
    save: bool = False,
    save_dir: str = "results",
    filename: Optional[str] = None
) -> Tuple[Figure, Optional[str]]:
    """
    Universal function for reading a CSV file, grouping data, and generating a bar chart.

    Args:
        csv_path (str): Path to the CSV file.
        fields (List[str]): Expected CSV columns (for validation).
        group_field (str): Column name to group by.
        value_field (str): Column name with numeric values.
        title (str, optional): Chart title. Defaults to None.
        xlabel (str, optional): X-axis label. Defaults to group_field.
        ylabel (str, optional): Y-axis label. Defaults to value_field.
        palette (str, optional): Seaborn color palette. Defaults to "Set2".
        save (bool, optional): Whether to save the chart to a file. Defaults to False.
        save_dir (str, optional): Directory to save the file. Defaults to "results".
        filename (str, optional): Custom filename (without extension). Defaults to f"{group_field}_chart".

    Returns:
        Tuple[Figure, Optional[str]]:
            - Figure object with the created plot.
            - Path to the saved file if save=True, otherwise None.
    """
    # === 1. Load data ===
    if isinstance(csv_file, pd.DataFrame):
        df = csv_file
    else:
        df: pd.DataFrame = pd.read_csv(csv_file, encoding="utf-8-sig")

    # === 2. Validate expected columns ===
    missing = [col for col in (group_field, value_field) if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Found: {list(df.columns)}")

    # === 3. Clean numeric data ===
    df[value_field] = pd.to_numeric(df[value_field], errors="coerce")
    df.dropna(subset=[value_field], inplace=True)

    # === 4. Group and aggregate data ===
    grouped = (
        df.groupby(group_field, as_index=False)[value_field]
        .mean()
        .sort_values(value_field, ascending=False)
    )

    # === 5. Build the chart ===
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=grouped, x=group_field, y=value_field, palette=palette, ax=ax)

    ax.set_title(title or f"Average {value_field} by {group_field}", fontsize=14)
    ax.set_xlabel(xlabel or group_field)
    ax.set_ylabel(ylabel or value_field)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # === 6. Optionally save ===
    file_path = None
    if save:
        os.makedirs(save_dir, exist_ok=True)
        filename = filename or f"{group_field}_chart"
        file_path = os.path.join(save_dir, f"{filename}.png")
        fig.savefig(file_path, dpi=300)
        print(f"✅ Saved: {file_path}")

    return fig, file_path


# === Example usage ===
if __name__ == "__main__":
    # Example: build a chart grouped by 'Область'
    generate_chart(
        csv_file="input_data.csv",
        group_field="Область",
        value_field="Значення",
        title="Середнє значення по областях",
        save=True,
        save_dir="results/regions",
        filename="regions_chart"
    )

    # Example: build a chart grouped by 'Місто'
    generate_chart(
        csv_file="input_data.csv",
        group_field="Місто/Район",
        value_field="Значення",
        title="Середнє значення по містах",
        save=True,
        save_dir="results/cities",
        filename="cities_chart"
    )
