import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QProgressBar, QTextEdit, QRadioButton, QButtonGroup, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.ui.components.image_display import ImageDisplay
from app.models.diffusion import DiffusionModel
from app.models.evolution import EvolutionModel
import os
import torch


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.diffusion_model = DiffusionModel()
        self.setWindowTitle("EvoDiffusionPython")
        self.setGeometry(100, 1000, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # テキスト入力領域
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Input prompt here")
        layout.addWidget(self.prompt_input)

        # テキスト決定ボタン
        self.prompt_button = QPushButton("Set prompt")
        layout.addWidget(self.prompt_button)
        
        # 画像表示領域
        image_layout = QGridLayout()
        self.image_displays = []
        for i in range(4):
            # 左側の画像には評価ボタンを左に、右側の画像には評価ボタンを右に配置
            button_position = "left" if i % 2 == 0 else "right"
            image_display = ImageDisplay(button_position=button_position)
            self.image_displays.append(image_display)  # ImageDisplay インスタンスをリストに追加
            image_layout.addWidget(image_display, i // 2, i % 2)  # image_layout に追加
        layout.addLayout(image_layout)

        # 操作ボタン
        button_layout = QHBoxLayout()
        button_names = ["Generate"]  # 修正ボタンを削除
        self.buttons = {}
        for name in button_names:
            button = QPushButton(name)
            self.buttons[name] = button
            button_layout.addWidget(button)
        layout.addLayout(button_layout)

        # 進捗バー
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # テキスト出力領域（デバッグ用）
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        # イベントハンドラの設定
        self.prompt_button.clicked.connect(self.on_prompt_button_clicked)
        self.buttons["Generate"].clicked.connect(self.on_generate_button_clicked)


    # 画像パス取得メソッド
    def get_image_paths(self):
        image_paths = []
        base_dir = self.diffusion_model.base_dir
        current_step = self.diffusion_model.current_step
        for i in range(4):
            iamge_path = os.path.join(base_dir, f"step_{current_step-1}", f"image_{i}.png")
            image_paths.append(iamge_path)
        return image_paths
    
     # 画像更新メソッド
    def update_images(self):
        image_paths = self.get_image_paths()
        for i, path in enumerate(image_paths):
            pixmap = QPixmap(path)
            self.image_displays[i].set_pixmap(pixmap)

    # 初期画像の生成
    def generate_initial_images(self, prompt):
        latents = [self.diffusion_model.generate_latent(i) for i in range(4)] # 4 枚の画像の潜在変数を生成
        images = self.diffusion_model.generate_images(prompt, latents) # 画像生成
        self.update_images()
        base_dir = self.diffusion_model.base_dir
        current_step = self.diffusion_model.current_step
        self.text_output.append(f"Initial images generated in {base_dir}")
        self.text_output.append(f"Current step: {current_step}")
        return base_dir, current_step

    # promptボタンがクリックされたときの処理
    def on_prompt_button_clicked(self):
        prompt = self.prompt_input.text()
        base_dir, current_step = self.generate_initial_images(prompt)
        return base_dir, current_step
    
    def get_selected_image_ids(self):
        selected_image_ids = []
        for i, image_display in enumerate(self.image_displays):
            if image_display.is_selected:
                selected_image_ids.append(i)
        return selected_image_ids
    
    def on_generate_button_clicked(self):
        base_dir, current_step = self.on_prompt_button_clicked()
        prompt = self.prompt_input.text()
        selected_image_ids = self.get_selected_image_ids()
        if len(selected_image_ids) == 0:
            # 画像が選択されていない場合エラーを表示（TODO: 今後ランダムな画像が再生成されるように修正）
            self.text_output.append("Please select an image.")
            return
        elif len(selected_image_ids) > 0:
            # 画像が選択されている場合、RandamMutation により新しい画像を生成
            # 選択された画像の潜在変数をbase_dir/current_step から読み込み
            selected_latents = []
            for i in selected_image_ids:
                latent_path = os.path.join(base_dir, f"step_{current_step - 1}", f"latent_{i}.pt")
                selected_latents.append(torch.load(latent_path))
            # 変異
            evolution_model = EvolutionModel(selected_latents)
            mutated_latents = evolution_model.random_mutation()
            # ログの保存
            self.diffusion_model.save_user_log(selected_image_ids)
            # 画像生成
            images, base_dir, current_step = self.diffusion_model.generate_images(prompt, mutated_latents)
            self.update_images()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
