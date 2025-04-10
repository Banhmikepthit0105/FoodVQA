import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 Tập dữ liệu câu hỏi - đáp (có thể mở rộng)


# 🔹 Chuyển thành DataFrame
df = pd.read_csv('train.csv')

# 🔹 Tạo TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Question"])  # Vector hóa câu hỏi có sẵn


def get_answer(user_question):
    user_tfidf = vectorizer.transform([user_question])  # Vector hóa câu hỏi nhập vào
    similarities = cosine_similarity(user_tfidf, X)  # Tính độ tương đồng cosine
    best_match_idx = similarities.argmax()  # Chọn câu có điểm cao nhất
    return df["Answer"][best_match_idx]
def write_csv(results, filename='test.csv'):
    with open(filename, 'w') as f:
        f.write('\n')
        for result in results:
            f.write(f'{result}\n')

test = pd.read_csv('test.csv')

# add a column predicted_answer to the test dataframe
test['predicted_answer'] = test['Question'].apply(get_answer)
test.to_csv('new_test.csv', index=False)
    
