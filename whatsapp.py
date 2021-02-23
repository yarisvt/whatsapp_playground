import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme()


def get_data(file_name):
    data = {"date": [], "time": [], "name": [], "message": [],
            "full_message": []}

    start_pattern = r"^\[(\d{2}-\d{2}-\d{4})\s(\d{2}:\d{2}:\d{2})]\s"
    message_patern = r"^\[(\d{2}-\d{2}-\d{4})\s(\d{2}:\d{2}:\d{2})]\s(.*?)(?<=:)\s(.*)"

    with open(file_name, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if "\u200e" not in line and re.match(start_pattern, line):
                match = re.search(message_patern, line)
                if match:
                    data["date"].append(match.group(1))
                    data["time"].append(match.group(2))
                    data["name"].append(match.group(3).replace(":", ""))
                    data["message"].append(
                        re.sub(r"[,.\"'?!]", "",
                               match.group(4)).lower().split())
                    data["full_message"].append(match.group(4).lower())

    return pd.DataFrame.from_dict(data)


def average_words_per_message(df):
    grouped_data = df.groupby(["name"])["full_message"].apply(
        lambda x: sum([len(i) for i in x]) / len(x))
    axs = grouped_data.plot(kind="barh", figsize=(8, 5),
                            title="Average characters per message",
                            color=[f"C{i}" for i in range(len(grouped_data))])
    axs.set(ylabel="")
    plt.tight_layout()
    plt.show()


def total_messages_per_person(df):
    grouped_data = df.groupby(["name"]).size()
    axs = grouped_data.plot(kind="barh", figsize=(8, 5),
                            title="Total messages per person",
                            color=[f"C{i}" for i in range(len(grouped_data))])
    axs.set(ylabel="")
    plt.tight_layout()
    plt.show()


def find_by_word(df, words):
    data = df["message"].apply(lambda x: any(
        item for item in words if item in x))
    grouped_data = df[data].groupby(["name"]).size()

    axs = grouped_data.plot(kind="barh", figsize=(8, 5),
                            title=", ".join(words),
                            color=[f"C{i}" for i in range(len(grouped_data))])

    axs.set(ylabel="")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = get_data("_chat.txt")
    average_words_per_message(df)
    total_messages_per_person(df)
    find_by_word(df, ["ik"])
