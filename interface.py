import sys
from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from  coupang_crowler import coupang 
class ShoppingMallSearchApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #crawler 파트
        self.coupang_ins = coupang()

        self.setWindowTitle("쇼핑몰 검색")
        self.setGeometry(100, 100, 600, 400)
        
        # 메인 위젯과 레이아웃 설정
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # 쇼핑몰 이름 레이아웃
        mall_name_layout = QtWidgets.QHBoxLayout()
        mall_name_label = QtWidgets.QLabel("쇼핑몰 이름: ")
        self.mall_name_input = QtWidgets.QLineEdit(self)
        self.mall_name_input.setPlaceholderText("쇼핑몰 이름 입력")
        mall_name_layout.addWidget(mall_name_label)
        mall_name_layout.addWidget(self.mall_name_input)
        
        # 검색어 입력 레이아웃
        search_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("검색어: ")
        self.search_input = QtWidgets.QLineEdit(self)
        self.search_input.setPlaceholderText("검색어 입력")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # 페이지 정렬 방식 라디오 버튼
        self.sort_radio_group = QtWidgets.QButtonGroup(self)
        self.recommended_radio = QtWidgets.QRadioButton("추천순", self)
        self.sales_radio = QtWidgets.QRadioButton("판매량 순", self)
        self.recommended_radio.setChecked(True)  # 기본적으로 추천순 선택
        self.sort_radio_group.addButton(self.recommended_radio)
        self.sort_radio_group.addButton(self.sales_radio)
        sort_layout = QtWidgets.QHBoxLayout()
        sort_label = QtWidgets.QLabel("페이지 정렬 방식: ")
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.recommended_radio)
        sort_layout.addWidget(self.sales_radio)

        # 검색할 페이지 수 입력 레이아웃
        page_count_layout = QtWidgets.QHBoxLayout()
        page_count_label = QtWidgets.QLabel("검색할 페이지 수: ")
        self.page_count_input = QtWidgets.QSpinBox(self)
        self.page_count_input.setMinimum(1)  # 최소값 설정
        self.page_count_input.setMaximum(100)  # 최대값 설정
        self.page_count_input.setValue(3)  # 기본값 설정
        page_count_layout.addWidget(page_count_label)
        page_count_layout.addWidget(self.page_count_input)

        # 엑셀로 저장 여부 체크 박스
        self.save_excel_checkbox = QtWidgets.QCheckBox("엑셀로 저장", self)
        self.save_excel_checkbox.setChecked(True)  # 기본적으로 체크되어 있도록 설정

        # 버튼 레이아웃
        button_layout = QtWidgets.QHBoxLayout()
        
        # 검색 버튼
        self.search_button = QtWidgets.QPushButton("검색", self)
        self.search_button.clicked.connect(self.on_search_clicked)
        button_layout.addWidget(self.search_button)
        
        # 결과 저장 버튼
        # self.save_button = QtWidgets.QPushButton("결과 저장", self)
        # self.save_button.clicked.connect(self.save_results)
        # button_layout.addWidget(self.save_button)
        
        # 상태 표시 라벨
        self.status_label = QtWidgets.QLabel("", self)
        
        # 로그 표시 텍스트 박스
        self.log_text = QtWidgets.QTextEdit(self)
        self.log_text.setReadOnly(True)
        
        # 레이아웃에 추가
        layout.addLayout(mall_name_layout)
        layout.addLayout(search_layout)
        layout.addLayout(sort_layout)
        layout.addLayout(page_count_layout)
        layout.addWidget(self.save_excel_checkbox)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.log_text)
        
    def on_search_clicked(self):
        # 검색 버튼 클릭 시 실행될 메서드
        mall_name = self.mall_name_input.text()
        search_keyword = self.search_input.text()
        
        # 쇼핑몰 이름과 검색어를 가져와서 coupang의 excute 메서드 호출
        self.coupang_ins.excute(mall_name, search_keyword)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)
    
    window = ShoppingMallSearchApp()
    window.show()
    
    sys.exit(app.exec_())
