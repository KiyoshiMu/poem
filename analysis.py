from collections import defaultdict
from pathlib import Path
import re

# "[愛、嫌悪]"" -> ["愛", "嫌悪"]
# "希望、幸福" -> ["希望", "幸福"]
# "愛, 感謝, 幸福" -> ["愛", "感謝", "幸福"]

ja_splitor = re.compile(r"[、,]")
ja_cleaner = re.compile(r"[「」\[\]。]")
JA_EMOS = "愛、悲しみ、幸福、怒り、希望、嫌悪、恐れ、驚き".split("、")


def ja_emo_loader(emo_path):
    with open(emo_path, "r", encoding="utf-8") as f:
        raw_emo = f.read()
    emos = ja_splitor.split(ja_cleaner.sub("", raw_emo))
    return [emo.strip() for emo in emos if emo.strip() != ""]


def ja_counter():
    dir_path = Path("ja_emotion")
    emo_counter = defaultdict(int)
    for emo_path in dir_path.glob("*.txt"):
        emos = ja_emo_loader(emo_path)
        for emo in emos:
            emo_counter[emo] += 1
    return emo_counter


en_splitor = re.compile(r"are|and|:|,")
en_cleaner = re.compile(r"[\[\]]")
EN_EMOS = "love, sadness, happiness, anger, hope, disgust, fear, surprise".split(", ")
JA_EMO_TO_EN_EMO = {
    "希望": "hope",
    "愛": "love",
    "幸福": "happiness",
    "悲しみ": "sadness",
    "無力感": "powerlessness",
    "驚き": "surprise",
    "思い出": "memories",
    "恐れ": "fear",
    "勇気": "courage",
    "闘志": "fighting spirit",
    "怒り": "anger",
    "嫌悪": "disgust",
    "静": "quiet",
    "浄": "pure",
    "懐かしさ": "nostalgia",
    "不思議": "wonder",
    "不安": "anxiety",
    "寂しさ": "loneliness",
    "変化": "change",
    "自由": "freedom",
    "躍動": "dynamism",
    "感謝": "gratitude",
    "切なさ": "yearning",
    "後悔": "regret",
}


def en_emo_loader(emo_path):
    with open(emo_path, "r", encoding="utf-8") as f:
        raw_emo = f.read()
    emos = en_splitor.split(en_cleaner.sub("", raw_emo))
    return [emo.strip().lower() for emo in emos if emo.strip() != ""]


def en_counter():
    dir_path = Path("en_emotion")
    emo_counter = defaultdict(int)
    for emo_path in dir_path.glob("*.txt"):
        emos = en_emo_loader(emo_path)
        for emo in emos:
            emo_counter[emo] += 1
    return emo_counter


if __name__ == "__main__":
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set()

    ja_emo_counter = ja_counter()
    ja_emo_counter = {key: value for key, value in ja_emo_counter.items() if value > 1}
    ja_word_cloud = WordCloud(
        background_color="white",
        width=600,
        height=600,
        font_path="NotoSansJP-Regular.ttf",
    )
    ja_word_cloud.generate_from_frequencies(ja_emo_counter)
    plt.imshow(ja_word_cloud)
    plt.axis("off")
    plt.savefig("ja_word_cloud.png")
    print(ja_emo_counter)
    ja_to_en_counter = {
        JA_EMO_TO_EN_EMO[key]: value for key, value in ja_emo_counter.items()
    }
    ja_to_en_word_cloud = WordCloud(background_color="white", width=800, height=600)
    ja_to_en_word_cloud.generate_from_frequencies(ja_to_en_counter)
    plt.imshow(ja_to_en_word_cloud)
    plt.axis("off")
    plt.savefig("ja_to_en_word_cloud.png")
    # histogram using seaborn, x axis is the emotion in English, y axis is the frequency
    ja_to_en_counter_filtered = {key: ja_to_en_counter[key] for key in EN_EMOS}
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=list(ja_to_en_counter_filtered.keys()),
        y=list(ja_to_en_counter_filtered.values()),
    )
    # x axis label
    plt.xlabel("Emotion")
    # y axis label
    plt.ylabel("Frequency")
    plt.savefig("ja_to_en_histogram.png")

    en_emo_counter = en_counter()
    en_emo_counter = {key: value for key, value in en_emo_counter.items() if value > 1}
    en_word_cloud = WordCloud(background_color="white", width=600, height=600)
    en_word_cloud.generate_from_frequencies(en_emo_counter)
    plt.imshow(en_word_cloud)
    plt.axis("off")
    plt.savefig("en_word_cloud.png")
    # histogram using seaborn
    en_emo_counter_filtered = {key: en_emo_counter[key] for key in EN_EMOS}
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=list(en_emo_counter_filtered.keys()), y=list(en_emo_counter_filtered.values())
    )
    # x axis label
    plt.xlabel("Emotion")
    # y axis label
    plt.ylabel("Frequency")
    plt.savefig("en_histogram.png")
    print(en_emo_counter)

    # t test
    from scipy.stats import chisquare

    group1 = [v for v in ja_to_en_counter_filtered.values()]
    sum1 = sum(group1)
    group2 = [v for v in en_emo_counter_filtered.values()]
    sum2 = sum(group2)
    group1 = [v / sum1 * sum2 for v in group1]
    print(group1)
    print(group2)
    print(chisquare(group1, group2))
