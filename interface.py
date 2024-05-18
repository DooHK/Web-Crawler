import sys
from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet

class ShoppingMallSearchApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # 버튼 레이아웃
        button_layout = QtWidgets.QHBoxLayout()
        
        # 검색 버튼
        self.search_button = QtWidgets.QPushButton("검색", self)
        self.search_button.clicked.connect(self.perform_search)
        button_layout.addWidget(self.search_button)
        
        # 결과 저장 버튼
        self.save_button = QtWidgets.QPushButton("결과 저장", self)
        self.save_button.clicked.connect(self.save_results)
        button_layout.addWidget(self.save_button)
        
        # 상태 표시 라벨
        self.status_label = QtWidgets.QLabel("", self)
        
        # 로그 표시 텍스트 박스
        self.log_text = QtWidgets.QTextEdit(self)
        self.log_text.setReadOnly(True)
        
        # 레이아웃에 추가
        layout.addLayout(mall_name_layout)
        layout.addLayout(search_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.log_text)
        
    def perform_search(self):
        mall_name = self.mall_name_input.text()
        search_keyword = self.search_input.text()
        
        if not mall_name or not search_keyword:
            self.status_label.setText("쇼핑몰 이름과 검색어를 입력해주세요.")
            return
        
        self.status_label.setText("검색 중...")
        self.log_text.append(f"'{mall_name}'에서 '{search_keyword}' 검색 중...")
        
        # 여기에 실제 웹 크롤링 코드를 추가합니다.
        # 예를 들어, Selenium, BeautifulSoup 등을 사용하여 검색 결과를 가져옵니다.
        
        # 크롤링 결과 예시
        search_results = [
            f"상품1: {search_keyword} in {mall_name}",
            f"상품2: {search_keyword} in {mall_name}",
            f"상품3: {search_keyword} in {mall_name}"
        ]
        
        # 로그에 결과 추가
        for result in search_results:
            self.log_text.append(result)
        
        self.status_label.setText("검색 완료.")
        
    def save_results(self):
        results = self.log_text.toPlainText()
        
        if not results:
            self.status_label.setText("저장할 결과가 없습니다.")
            return
        
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "결과 저장", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(results)
            self.status_label.setText(f"결과가 '{file_name}'에 저장되었습니다.")
        else:
            self.status_label.setText("저장 취소.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)
    
    window = ShoppingMallSearchApp()
    window.show()
    
    sys.exit(app.exec_())
