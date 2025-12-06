# Vietnamese Sentiment Analyzer

Ứng dụng phân loại cảm xúc tiếng Việt (Positive – Neutral – Negative) sử dụng DistilBERT Multilingual, Django REST Framework, Vue 3 và TailwindCSS.


## Kiến trúc hệ thống
1. **Frontend**: Vue 3 + TailwindCSS
   - Nhập câu, hiển thị kết quả & lịch sử.
2. **Backend**: Django REST
   - Nhận câu, chạy model, lưu SQLite.
3. **Model NLP**: DistilBERT Multilingual Cased
   - 3 nhãn: Positive, Neutral, Negative

---

## Yêu cầu hệ thống

### Python
- Python 3.10+
- Django >=5
- Django REST Framework
- PyTorch
- Transformers
- BitsAndBytes
- Ekphrasis
- Clean-text, Emoji

### Frontend
- Node.js 18+
- Vue 3
- Vite
- TailwindCSS

---
## Link video Demo
https://youtu.be/BYSttxRs684
## Cài đặt 


```bash
git clone https://github.com/tranhoangnam712/sentiment-analysis-django-vue.git
pip install -r requirements.txt
cd sentiment-frontend 
npm install
```
## Hướng dẫn download model

Do file `checkpoint.pth` quá lớn, không được push lên GitHub.  
Trước khi chạy ứng dụng, bạn cần download file này từ Google Drive:

[Download checkpoint.pth](https://drive.google.com/file/d/1xpbeauW2KajNCmA0g7f7TnBIooZ9d22N/view?usp=sharing)

Sau khi download xong, **đặt file** vào thư mục:

sentiment_api/analyzer/
> Lưu ý: Tên file phải chính xác là `checkpoint.pth`.
## Chạy chương trình 
### Chạy backendbackend
```bash 
cd sentiment_api
python manage.py runserver
```
### Chạy frontendfrontend
```bash 
cd sentiment_frontend
npm run dev
```