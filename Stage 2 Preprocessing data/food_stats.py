import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter
import nltk
import os
import matplotlib.pyplot as plt
import sys
from nltk.corpus import stopwords
from wordcloud import WordCloud
import string

stop_words = set(stopwords.words('english'))

# Function to download necessary NLTK resources
def download_nltk_resources():
    required_resources = ['punkt_tab', 'stopwords']
    print("Checking and downloading necessary NLTK resources...")
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource else f'corpora/{resource}')
            print(f"Resource '{resource}' is already downloaded.")
        except LookupError:
            print(f"Downloading '{resource}'...")
            try:
                nltk.download(resource, quiet=False)
                print(f"Successfully downloaded '{resource}'.")
            except Exception as e:
                print(f"Error downloading '{resource}': {e}")
                sys.exit(1)

# Run the download function
download_nltk_resources()

# Đường dẫn file
file_path = r"input.csv" 
output_path = r"./png_folder"

# Kiểm tra file
if not os.path.exists(file_path):
    print(f"File không tồn tại tại: {file_path}. Vui lòng kiểm tra lại đường dẫn hoặc tạo file.")
    exit()

# Đọc file CSV
data = pd.read_csv(file_path)

# 1. Tách và xử lý câu hỏi
all_questions = []
for question_str in data['Questions']:
    questions = question_str.split(', ')
    all_questions.extend(questions)

# 2. Thống kê loại câu hỏi dựa trên từ đầu tiên
def get_question_type(question):
    tokens = word_tokenize(question.strip())
    if tokens:
        return tokens[0].lower()  # Lấy từ đầu tiên (chữ cái đầu câu hỏi)
    return "unknown"

question_types = [get_question_type(q) for q in all_questions]
type_counts = Counter(question_types)

# In số lượng loại câu hỏi
print("\nThống kê loại câu hỏi (dựa trên từ đầu tiên):")
total_questions = sum(type_counts.values())
print(f"Tổng số câu hỏi: {total_questions}")
for q_type, count in type_counts.most_common():
    print(f" - {q_type}: {count} câu hỏi ({(count / total_questions * 100):.1f}%)")

# 3. Gom các loại câu hỏi xuất hiện ít hơn 5% vào "Others"
threshold = 0.05  # Ngưỡng 5%
significant_types = {}
others_count = 0
for q_type, count in type_counts.items():
    percentage = count / total_questions
    if percentage >= threshold:
        significant_types[q_type] = count
    else:
        others_count += count

if others_count > 0:
    significant_types['Others'] = others_count

# Vẽ pie chart cho loại câu hỏi và lưu file PNG
labels_qt = list(significant_types.keys())
sizes_qt = list(significant_types.values())
plt.figure(figsize=(8, 8))
plt.pie(sizes_qt, labels=labels_qt, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
plt.title('Phân bố loại câu hỏi')
output_path_qt = output_path + 'question_types.png'
plt.savefig(output_path_qt, bbox_inches='tight', dpi=300)
print(f"\nĐã lưu biểu đồ phân bố loại câu hỏi vào '{output_path_qt}'")
plt.show()

# 4. N-gram (unigram, bi-gram) phổ biến
def get_ngrams(texts, n):
    all_ngrams = []
    for text in texts:
        tokens = [word for word in word_tokenize(text.lower()) if word not in stop_words and word not in string.punctuation]
        all_ngrams.extend(ngrams(tokens, n))
    return Counter(all_ngrams).most_common(30)

# Unigram và bi-gram cho Questions
uni_grams_questions = get_ngrams(all_questions, 1)
# bi_grams_questions = get_ngrams(all_questions, 2)
# tri_grams_questions = get_ngrams(all_questions, 3)  # Comment tri-gram

# In top 10 1-grams và bi-grams
print("\nTop 10 1-grams trong Questions:")
for ug, count in uni_grams_questions:
    print(f"{ug[0]}: {count} lần")  # ug[0] vì unigram là tuple đơn (word,)

# print("\nTop 10 bi-grams trong Questions:")
# for bg, count in bi_grams_questions:
#     print(f"{bg}: {count} lần")

# # In top 10 tri-grams trong Questions (commented)
# print("\nTop 10 tri-grams trong Questions:")
# for tg, count in tri_grams_questions:
#     print(f"{tg}: {count} lần")

# Tạo word cloud cho top 10 unigrams trong Questions
word_freq_dict = {ug[0]: count for ug, count in uni_grams_questions}
wordcloud_ug = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(word_freq_dict)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_ug, interpolation='bilinear')
plt.title('Top 10 1-grams trong Questions')
plt.axis('off')
output_path_ug = output_path + 'uni_grams_questions.png'
plt.savefig(output_path_ug, bbox_inches='tight', dpi=300)
print(f"\nĐã lưu word cloud cho uni-grams vào '{output_path_ug}'")
plt.show()

# Tạo word cloud cho top 10 bi-grams trong Questions
# wordcloud_bg = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies({f"{bg[0]}_{bg[1]}": count for bg, count in bi_grams_questions})
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud_bg, interpolation='bilinear')
# plt.title('Top 10 bi-grams trong Questions')
# plt.axis('off')
# output_path_bg = output_path + 'bi_grams_questions.png'
# plt.savefig(output_path_bg, bbox_inches='tight', dpi=300)
# print(f"\nĐã lưu word cloud cho bi-grams vào '{output_path_bg}'")
# plt.show()

# # Vẽ word cloud cho top 10 tri-grams trong Questions 
# wordcloud_tg = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies({f"{tg[0]}_{tg[1]}_{tg[2]}": count for tg, count in tri_grams_questions})
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud_tg, interpolation='bilinear')
# plt.title('Top 10 tri-grams trong Questions')
# plt.axis('off')
# output_path_tg = output_path + 'tri_grams_questions.png'
# plt.savefig(output_path_tg, bbox_inches='tight', dpi=300)
# print(f"\nĐã lưu word cloud cho tri-grams vào '{output_path_tg}'")
# plt.show()

# Unigram và bi-gram cho Answers (nếu có cột 'Answer')
if 'Answer' in data.columns:
    all_answers = data['Answer'].dropna().tolist()
    uni_grams_answers = get_ngrams(all_answers, 1)
    # bi_grams_answers = get_ngrams(all_answers, 2)
    # tri_grams_answers = get_ngrams(all_answers, 3)  # Comment tri-gram

    print("\nTop 10 1-grams trong Answers:")
    for ug, count in uni_grams_answers:
        print(f"{ug[0]}: {count} lần")

    # print("\nTop 10 bi-grams trong Answers:")
    # for bg, count in bi_grams_answers:
    #     print(f"{bg}: {count} lần")

    # # In top 10 tri-grams trong Answers (commented)
    # print("\nTop 10 tri-grams trong Answers:")
    # for tg, count in tri_grams_answers:
    #     print(f"{tg}: {count} lần")

    # Tạo word cloud cho top 10 unigrams trong Answers
    word_freq_dict_a = {ug[0]: count for ug, count in uni_grams_answers}  # Convert tuple keys to strings
    wordcloud_ug_a = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(word_freq_dict_a)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_ug_a, interpolation='bilinear')
    plt.title('Top 10 1-grams trong Answers')
    plt.axis('off')
    output_path_ug_a = output_path + 'uni_grams_answers.png'
    plt.savefig(output_path_ug_a, bbox_inches='tight', dpi=300)
    print(f"\nĐã lưu word cloud cho uni-grams của Answers vào '{output_path_ug_a}'")
    plt.show()

    # Tạo word cloud cho top 10 bi-grams trong Answers
    # wordcloud_bg_a = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies({f"{bg[0]}_{bg[1]}": count for bg, count in bi_grams_answers})
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud_bg_a, interpolation='bilinear')
    # plt.title('Top 10 bi-grams trong Answers')
    # plt.axis('off')
    # output_path_bg_a = output_path + 'bi_grams_answers.png'
    # plt.savefig(output_path_bg_a, bbox_inches='tight', dpi=300)
    # print(f"\nĐã lưu word cloud cho bi-grams của Answers vào '{output_path_bg_a}'")
    # plt.show()

    # # Vẽ word cloud cho top 10 tri-grams trong Answers (commented)
    # wordcloud_tg_a = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies({f"{tg[0]}_{tg[1]}_{tg[2]}": count for tg, count in tri_grams_answers})
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud_tg_a, interpolation='bilinear')
    # plt.title('Top 10 tri-grams trong Answers')
    # plt.axis('off')
    # output_path_tg_a = output_path + 'tri_grams_answers.png'
    # plt.savefig(output_path_tg_a, bbox_inches='tight', dpi=300)
    # print(f"\nĐã lưu word cloud cho tri-grams của Answers vào '{output_path_tg_a}'")
    # plt.show()
else:
    print("\nCột 'Answer' không tồn tại. Không thể tính bi-gram và tri-gram cho Answers.")