import json
import os

DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "vocab_n5.json")

# Sample N5 Vocabulary (Source: Common JLPT N5 lists)
# Structure: {'word': 'String', 'reading': 'String', 'meaning': 'String'}
SAMPLE_DATA = [
    {"word": "会う", "reading": "あう", "meaning": "만나다"},
    {"word": "青", "reading": "あお", "meaning": "파랑"},
    {"word": "赤", "reading": "あか", "meaning": "빨강"},
    {"word": "明るい", "reading": "あかるい", "meaning": "밝다"},
    {"word": "秋", "reading": "あき", "meaning": "가을"},
    {"word": "開く", "reading": "あく", "meaning": "열리다"},
    {"word": "開ける", "reading": "あける", "meaning": "열다"},
    {"word": "上げる", "reading": "あげる", "meaning": "주다, 올리다"},
    {"word": "朝", "reading": "あさ", "meaning": "아침"},
    {"word": "朝ご飯", "reading": "あさごはん", "meaning": "아침밥"},
    {"word": "あさって", "reading": "あさって", "meaning": "모레"},
    {"word": "足", "reading": "あし", "meaning": "발, 다리"},
    {"word": "明日", "reading": "あした", "meaning": "내일"},
    {"word": "あそこ", "reading": "あそこ", "meaning": "저기"},
    {"word": "遊ぶ", "reading": "あそぶ", "meaning": "놀다"},
    {"word": "暖かい", "reading": "あたたかい", "meaning": "따뜻하다"},
    {"word": "頭", "reading": "あたま", "meaning": "머리"},
    {"word": "新しい", "reading": "あたらしい", "meaning": "새롭다"},
    {"word": "あちら", "reading": "あちら", "meaning": "저쪽 (정중형)"},
    {"word": "暑い", "reading": "あつい", "meaning": "덥다"},
    {"word": "熱い", "reading": "あつい", "meaning": "뜨겁다"},
    {"word": "厚い", "reading": "あつい", "meaning": "두껍다"},
    {"word": "後", "reading": "あと", "meaning": "뒤, 후"},
    {"word": "あなた", "reading": "あなた", "meaning": "당신"},
    {"word": "兄", "reading": "あに", "meaning": "형/오빠 (자신의)"},
    {"word": "姉", "reading": "あね", "meaning": "누나/언니 (자신의)"},
    {"word": "あの", "reading": "あの", "meaning": "저 (지시사)"},
    {"word": "アパート", "reading": "アパート", "meaning": "아파트"},
    {"word": "浴びる", "reading": "あびる", "meaning": "뒤집어쓰다/샤워하다"},
    {"word": "危ない", "reading": "あぶない", "meaning": "위험하다"},
    {"word": "甘い", "reading": "あまい", "meaning": "달다"},
    {"word": "あまり", "reading": "あまり", "meaning": "그다지"},
    {"word": "雨", "reading": "あめ", "meaning": "비"},
    {"word": "洗う", "reading": "あらう", "meaning": "씻다"},
    {"word": "ある", "reading": "ある", "meaning": "있다 (사물)"},
    {"word": "歩く", "reading": "あるく", "meaning": "걷다"},
    {"word": "あれ", "reading": "あれ", "meaning": "저것"},
    {"word": "いい/よい", "reading": "いい/よい", "meaning": "좋다"},
    {"word": "いいえ", "reading": "いいえ", "meaning": "아니요"},
    {"word": "言う", "reading": "いう", "meaning": "말하다"},
    {"word": "家", "reading": "いえ", "meaning": "집"},
    {"word": "いかが", "reading": "いかが", "meaning": "어떻습니까"},
    {"word": "行く", "reading": "いく", "meaning": "가다"},
    {"word": "いくつ", "reading": "いくつ", "meaning": "몇 개"},
    {"word": "いくら", "reading": "いくら", "meaning": "얼마"},
    {"word": "池", "reading": "いけ", "meaning": "연못"},
    {"word": "医者", "reading": "いしゃ", "meaning": "의사"},
    {"word": "椅子", "reading": "いす", "meaning": "의자"},
    {"word": "忙しい", "reading": "いそがしい", "meaning": "바쁘다"},
    {"word": "痛い", "reading": "いたい", "meaning": "아프다"},
    {"word": "一", "reading": "いち", "meaning": "일(1)"},
    {"word": "一日", "reading": "いちにち", "meaning": "하루"},
    {"word": "いちばん", "reading": "いちばん", "meaning": "가장, 제일"},
    {"word": "いつ", "reading": "いつ", "meaning": "언제"},
    {"word": "五日", "reading": "いつか", "meaning": "5일"},
    {"word": "一緒", "reading": "いっしょ", "meaning": "함께"},
    {"word": "五つ", "reading": "いつつ", "meaning": "다섯 개"},
    {"word": "いつも", "reading": "いつも", "meaning": "항상"},
    {"word": "犬", "reading": "いぬ", "meaning": "개"},
    {"word": "今", "reading": "いま", "meaning": "지금"},
    {"word": "意味", "reading": "いみ", "meaning": "의미"},
    {"word": "妹", "reading": "いもうと", "meaning": "여동생"},
    {"word": "嫌", "reading": "いや", "meaning": "싫다"},
    {"word": "入口", "reading": "いりぐち", "meaning": "입구"},
    {"word": "居る", "reading": "いる", "meaning": "있다 (사람/동물)"},
    {"word": "要る", "reading": "いる", "meaning": "필요하다"},
    {"word": "入れる", "reading": "いれる", "meaning": "넣다"},
    {"word": "色", "reading": "いろ", "meaning": "색깔"},
    {"word": "いろいろ", "reading": "いろいろ", "meaning": "여러가지"},
    {"word": "上", "reading": "うえ", "meaning": "위"},
    {"word": "後ろ", "reading": "うしろ", "meaning": "뒤"},
    {"word": "薄い", "reading": "うすい", "meaning": "얇다"},
    {"word": "歌", "reading": "うた", "meaning": "노래"},
    {"word": "歌う", "reading": "うたう", "meaning": "노래하다"},
    {"word": "家", "reading": "うち", "meaning": "집 (우리 집)"},
    {"word": "生まれる", "reading": "うまれる", "meaning": "태어나다"},
    {"word": "海", "reading": "うみ", "meaning": "바다"},
    {"word": "売る", "reading": "うる", "meaning": "팔다"},
    {"word": "煩い", "reading": "うるさい", "meaning": "시끄럽다"},
    {"word": "上着", "reading": "うわぎ", "meaning": "겉옷"},
    {"word": "絵", "reading": "え", "meaning": "그림"},
    {"word": "映画", "reading": "えいが", "meaning": "영화"},
    {"word": "映画館", "reading": "えいがかん", "meaning": "영화관"},
    {"word": "英語", "reading": "えいご", "meaning": "영어"},
    {"word": "ええ", "reading": "ええ", "meaning": "네 (구어체)"},
    {"word": "駅", "reading": "えき", "meaning": "역"},
    {"word": "エレベーター", "reading": "エレベーター", "meaning": "엘리베이터"},
    {"word": "円", "reading": "えん", "meaning": "엔(화)"},
    {"word": "鉛筆", "reading": "えんぴつ", "meaning": "연필"}
]

def create_sample_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(SAMPLE_DATA, f, ensure_ascii=False, indent=2)
        
    print(f"Created sample N5 vocabulary file: {OUTPUT_FILE} ({len(SAMPLE_DATA)} words)")

if __name__ == "__main__":
    create_sample_file()
