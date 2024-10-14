import matplotlib
import matplotlib.pyplot as plt

def plot_and_save(df,
                  group_column,
                  x_column,
                  y_column,
                  x_label,
                  y_label,
                  title,
                  legend_text,
                  file_name
    ):
    plt.figure(figsize=(8, 6))
    for group in df[group_column].unique():
        subset = df[df[group_column] == group]
        plt.plot(subset[x_column], subset[y_column], label=f'Group {group}')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(title=legend_text)
    plt.grid(True)
    plt.savefig(f'derivatives_ha2//{file_name}', dpi=300, bbox_inches='tight')