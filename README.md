# Phân tích Hiểm họa Sạt lở đất Toàn cầu (NASA Global Landslide Catalog)

## 1. Tổng quan dự án
Dự án tập trung vào việc khám phá và phân tích tập dữ liệu sạt lở đất toàn cầu của NASA để hiểu rõ các quy luật về thời gian, không gian và cơ chế nhân quả. Mục tiêu cuối cùng là xác định các kịch bản rủi ro cao và xây dựng mô hình dự báo nhằm giảm thiểu thiệt hại về người và tài sản.

* **Thành viên thực hiện:** 
    - Võ Ngọc Tiến (23120370)
    - Mai Đình Trí (23120377)
* **Tên nhóm:** Magic Family 

## 2. Nguồn và Mô tả dữ liệu
* **Nguồn:** Global Landslide Catalog (GLC) được cung cấp bởi NASA.
* **Mô tả:** Tập dữ liệu ghi nhận các vụ sạt lở từ năm 1988 đến 2017, nhưng được thu thập tập trung từ 2007 - 2017, bao gồm các thông tin về: vị trí địa lý (`longitude`, `latitude`), thời gian xảy ra sạt lở (`event_date`), tác nhân (`landslide_trigger`), quy mô (`landslide_size`), loại hình ( `landslide_category`) và thiệt hại về người (`fatality_count`). Thông tin chi tiết có thể xem trong file `01_data_collection.ipynb`


## 3. Câu hỏi nghiên cứu
Dự án tập trung giải quyết 5 câu hỏi lớn:
1. Sạt lở có phải là một hiểm họa có tính quy luật không? Quy luật phân bố theo không gian và thời gian như thế nào?
2. Sự phân bố sạt lở phản ánh chính xác nguy cơ tự nhiên hay bị ảnh hưởng bởi khả năng quan sát?
3. Mối quan hệ nhân - quả trong thảm họa sạt lở đất là gì? Các loại hình và nguyên nhân sạt lở cụ thể nào, dẫn đến hậu quả nghiêm trọng nhất về mặt con người, và chúng phân bố ở đâu?
4. Trong các đơn vị hành chính có dân số cao, những tháng nào ghi nhận nhiều vụ sạt lở nhất và các vụ sạt lở trong những tháng này gây ra mức độ thiệt hại về con người (tử vong và bị thương) ra sao?
5. Dựa trên các đặc điểm về nguyên nhân, thời gian và bối cảnh địa lý, liệu có thể xây dựng mô hình học máy để phân loại và cảnh báo sớm khả năng gây thương vong (tử vong hoặc bị thương) của một vụ sạt lở không?
## 4. Tóm tắt kết quả chính
* **Quy luật thời gian:** Sạt lở tăng mạnh theo chu kỳ khí hậu cực đoan (ENSO) và có tính mùa vụ rõ rệt theo từng vùng khí hậu.
* **Thiên lệch báo cáo:** Phát hiện sự "nhiễu" dữ liệu tại các nước phát triển (như Mỹ). Số vụ cao tại đây phản ánh năng lực báo cáo tốt hơn là nguy cơ tự nhiên thực tế so với khu vực Himalaya hay Andes.
* **Nguyên nhân chết người:** Xác định được kịch bản "Mưa lớn + Lũ bùn (Mudslide)" là tác nhân gây thương vong lớn nhất tại các vùng nhiệt đới như Nam Mỹ và Nam Á.
* **Dữ liệu cho thấy một nghịch lý:** trong khi tháng 8 dẫn đầu về số lượng vụ việc, thì tháng 1 lại là thời điểm của những thảm họa khốc liệt nhất với tỷ lệ tử vong trên mỗi vụ cao vượt trội. Về mặt địa lý, Nam Á đứng đầu thế giới về thiệt hại về người bất chấp tần suất xảy ra thấp hơn Bắc Mỹ, minh chứng cho mức độ tổn thương cộng đồng nghiêm trọng tại khu vực này.

## 5. Cấu trúc thư mục
```bash
NASA_Landslide_Project/
├── data/
│   ├── raw/                          
│   │   └── Global_Landslide_Catalog_Export.csv
│   └── processed/                    
        └── Global_Landslide_Processed.csv
├── notebooks/                        
│   ├── 01_data_collection.ipynb      # Thu thập dữ liệu
│   ├── 02_data_exploration.ipynb     # Khám phá và làm sạch dữ liệu ban đầu
│   ├── 04_eda_visualization.ipynb    # Phân tích sâu và trực quan hóa (EDA)
│   └── 05_modeling.ipynb             # Xây dựng mô hình dự báo
├── src/                              # Các module mã nguồn hỗ trợ
│   ├── __init__.py
│   ├── config.py                     # Định nghĩa hằng số và đường dẫn dữ liệu
│   ├── data_processing.py            # Chứa các hàm xử lý dữ liệu (tiền xử lý)
│   └── utils.py                      # Các hàm tiện ích (sửa lỗi font, định dạng,...)                          
├── README.md                         
└── requirements.txt                 
```

## 6. Hướng dẫn Chạy chương trình

Để đảm bảo chương trình chạy ổn định và đồng bộ dữ liệu giữa các máy tính, vui lòng thực hiện theo quy trình 4 bước sau:

### Bước 1: Thiết lập Môi trường ảo (Virtual Environment)
Việc sử dụng môi trường ảo giúp tách biệt các thư viện của đồ án này với các dự án khác, tránh xung đột phiên bản.
1. Mở terminal tại thư mục gốc của dự án.
2. Tạo môi trường ảo: 
   ```bash
   python -m venv venv
   ```
3. Kích hoạt môi trường ảo:
   - **Windows:** `.\venv\Scripts\activate`
   - **macOS/Linux:** `source venv/bin/activate`

### Bước 2: Cài đặt Thư viện
Cài đặt chính xác các phiên bản thư viện cần thiết bằng lệnh:
```bash
pip install -r requirements.txt
```

### Bước 3: Đăng ký Kernel cho Jupyter Notebook
Để các tệp Notebook nhận diện đúng môi trường ảo vừa tạo, bạn cần đăng ký Kernel:
1. Cài đặt ipykernel: `pip install ipykernel`
2. Đăng ký Kernel mới:
   ```bash
   python -m ipykernel install --user --name=nasa_project --display-name "Python (NASA Project)"
   ```

### Bước 4: Thứ tự Thực thi các Notebook
Mở Jupyter Notebook hoặc VS Code, chọn Kernel **"Python (NASA Project)"** và chạy các tệp theo đúng thứ tự logic để đảm bảo dữ liệu được xử lý tuần tự:

1. **`01_data_collection.ipynb`**: Tải dữ liệu gốc từ nguồn NASA về thư mục `data/raw/`.
2. **`02_data_exploration.ipynb`**: Làm sạch dữ liệu, sửa lỗi font chữ và xử lý các giá trị thiếu.
3. **`04_eda_visualization.ipynb`**: Thực hiện phân tích trực quan hóa để trích xuất các quy luật sạt lở (Yêu cầu dữ liệu từ bước 2).
4. **`05_modeling.ipynb`**: Xây dựng và đánh giá các mô hình dự báo Machine Learning.

> **Mẹo nhỏ:** 
> - Trước khi lưu hoặc gửi tệp Notebook cho cộng sự, vui lòng chọn **Cell > All Output > Clear** để giảm dung lượng file và tránh xung đột khi gộp mã nguồn trên Git.
> - Phiên bản tối thiểu Python của bạn nên là `Python 3.11` trở lên.

## 7. Thư viện sử dụng
* `pandas`, `numpy`: Xử lý dữ liệu.
* `matplotlib`, `seaborn`, `plotly`: Trực quan hóa dữ liệu.
* `scikit-learn`: Xây dựng mô hình học máy.