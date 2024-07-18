import sys
from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from coupang_crowler import coupang
import threading
import queue
import time

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
        
        # 수평 레이아웃 추가
        layout.addLayout(mall_name_layout)
        
        
        
        # 수평선 추가
        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        # 간격 추가
        layout.addWidget(line1)
        layout.addSpacing(5)  # 간격 추가
        
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
        
        # 수평선 추가
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        # 간격 추가
        layout.addSpacing(5)  # 간격 추가
        layout.addLayout(search_layout)
        layout.addSpacing(5)  # 간격 추가
        layout.addWidget(line2)
        layout.addSpacing(5)  # 간격 추가
        layout.addLayout(sort_layout)
        layout.addSpacing(5)  # 간격 추가
        
        # 검색할 페이지 수 입력 레이아웃
        page_count_layout = QtWidgets.QHBoxLayout()
        page_count_label = QtWidgets.QLabel("검색할 페이지 수: ")
        self.page_count_input = QtWidgets.QSpinBox(self)
        self.page_count_input.setMinimum(1)  # 최소값 설정
        self.page_count_input.setMaximum(100)  # 최대값 설정
        self.page_count_input.setValue(3)  # 기본값 설정
        page_count_layout.addWidget(page_count_label)
        page_count_layout.addWidget(self.page_count_input)
        
        # 수평선 추가
        line3 = QtWidgets.QFrame()
        line3.setFrameShape(QtWidgets.QFrame.HLine)
        line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        # 간격 추가
        layout.addWidget(line3)
        layout.addSpacing(5)  # 간격 추가
        layout.addLayout(page_count_layout)
        layout.addSpacing(5)  # 간격 추가
        
        # 엑셀로 저장 여부 체크 박스
        self.save_excel_checkbox = QtWidgets.QCheckBox("엑셀로 저장", self)
        self.save_excel_checkbox.setChecked(True)  # 기본적으로 체크되어 있도록 설정
        
        ## 수평선 추가
        line4 = QtWidgets.QFrame()
        line4.setFrameShape(QtWidgets.QFrame.HLine)
        line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        # 간격 추가
        layout.addWidget(line4)
        layout.addSpacing(5)  # 간격 추가
        layout.addWidget(self.save_excel_checkbox)
        layout.addSpacing(20)  # 간격 추가
        
        # 버튼 레이아웃
        button_layout = QtWidgets.QHBoxLayout()
        
        # 검색 버튼
        self.search_button = QtWidgets.QPushButton("검색", self)
        self.search_button.clicked.connect(self.start_search_thread)
        button_layout.addWidget(self.search_button)
        
        # 시간 텍스트 박스
        self.log_text = QtWidgets.QTextEdit(self)
        self.log_text.setReadOnly(True)
        
        # 간격 추가
        layout.addWidget(self.log_text)
        layout.addSpacing(20)  # 간격 추가
        
        # 레이아웃에 버튼 레이아웃 추가
        layout.addLayout(button_layout)
        
        # 간격 추가
        layout.addSpacing(10)  # 간격 추가
        
        # 상태 표시 라벨 추가
        self.status_label = QtWidgets.QLabel("", self)
        layout.addWidget(self.status_label)

    
    
    def start_search_thread(self):
        mall_name = self.mall_name_input.text()
        keyword = self.search_input.text()
        sort_method = "쿠팡 추천순" if self.recommended_radio.isChecked() else "판매량 순"
        page_count = self.page_count_input.value()
        save_to_excel = self.save_excel_checkbox.isChecked()
        

        
        # 스레드 생성 및 시작
        search_thread = threading.Thread(target=self.coupang_ins.excute, args=(mall_name, keyword, sort_method, page_count, save_to_excel, self))
        search_thread.start()
        self.update_log(f"{sort_method}으로 {keyword}을 검색.")
        # join을 사용하면 interface가 안움직임 
        # search_thread.join()
        # self.update_log("크롤링이 완료되었습니다.")


    def update_log(self, message):
        # 크롤링 로그 텍스트 박스에 메시지 추가
        self.log_text.append(message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)
    
    window = ShoppingMallSearchApp()
    window.show()
    
    sys.exit(app.exec_())
