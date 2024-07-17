import sys
import os
import torch
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QProgressBar, QTextEdit, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.ui.components.image_display import ImageDisplay
from app.models.diffusion import DiffusionModel
from app.models.evolution import EvolutionModel

class MainWindow(QMainWindow):
    """
    アプリケーションのメインウィンドウ
    
    ユーザーインターフェースの主要なコンポーネントを管理し、
    画像生成と進化のロジックを制御する
    """

    def __init__(self):
        super().__init__()
        self.diffusion_model = DiffusionModel()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """UIコンポーネントの設定"""
        self.setWindowTitle("EvoDiffusionPython")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        
        self._setup_prompt_input(layout)
        self._setup_image_displays(layout)
        self._setup_control_buttons(layout)
        self._setup_progress_bar(layout)
        self._setup_text_output(layout)

    def _setup_prompt_input(self, layout):
        """プロンプト入力領域の設定"""
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Input prompt here")
        layout.addWidget(self.prompt_input)

        self.prompt_button = QPushButton("Set prompt")
        layout.addWidget(self.prompt_button)

    def _setup_image_displays(self, layout):
        """画像表示領域の設定"""
        image_layout = QGridLayout()
        self.image_displays = []
        for i in range(4):
            button_position = "left" if i % 2 == 0 else "right"
            image_display = ImageDisplay(button_position=button_position)
            self.image_displays.append(image_display)
            image_layout.addWidget(image_display, i // 2, i % 2)
            image_display.installEventFilter(image_display.crop_overlay)
        layout.addLayout(image_layout)

    def _setup_control_buttons(self, layout):
        """操作ボタンの設定"""
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate")
        self.local_mutation_button = QPushButton("Apply Local Mutation")
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.local_mutation_button)
        layout.addLayout(button_layout)

    def _setup_progress_bar(self, layout):
        """進捗バーの設定"""
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

    def _setup_text_output(self, layout):
        """テキスト出力領域の設定"""
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

    def _connect_signals(self):
        """シグナルとスロットの接続"""
        self.prompt_button.clicked.connect(self._on_prompt_button_clicked)
        self.generate_button.clicked.connect(self._on_generate_button_clicked)
        self.local_mutation_button.clicked.connect(self._on_local_mutation_clicked)

    def _get_image_paths(self):
        """生成された画像のパスを取得"""
        base_dir = self.diffusion_model.base_dir
        current_step = self.diffusion_model.current_step
        return [os.path.join(base_dir, f"step_{current_step-1}", f"image_{i}.png") for i in range(4)]

    def _update_images(self):
        """画像表示の更新"""
        for image_display, path in zip(self.image_displays, self._get_image_paths()):
            image_display.set_pixmap(QPixmap(path))

    def _generate_initial_images(self, prompt):
        """初期画像の生成"""
        latents = [self.diffusion_model.generate_latent(i) for i in range(4)]
        self.diffusion_model.generate_images(prompt, latents)
        self._update_images()
        
        base_dir = self.diffusion_model.base_dir
        current_step = self.diffusion_model.current_step
        self.text_output.append(f"Initial images generated in {base_dir}")
        self.text_output.append(f"Current step: {current_step}")
        
        return base_dir, current_step

    def _on_prompt_button_clicked(self):
        """プロンプトボタンがクリックされたときの処理"""
        prompt = self.prompt_input.text()
        self._generate_initial_images(prompt)

    def _get_selected_image_ids(self):
        """選択された画像のIDを取得"""
        return [i for i, display in enumerate(self.image_displays) if display.is_selected]

    def _on_generate_button_clicked(self):
        """生成ボタンがクリックされたときの処理"""
        base_dir, current_step = self.diffusion_model.base_dir, self.diffusion_model.current_step
        prompt = self.prompt_input.text()
        selected_image_ids = self._get_selected_image_ids()

        if not selected_image_ids:
            self.text_output.append("Please select an image.")
            return

        # 選択された画像の潜在変数を読み込み
        selected_latents = [
            torch.load(os.path.join(base_dir, f"step_{current_step - 1}", f"latent_{i}.pt"))
            for i in selected_image_ids
        ]

        # 変異と画像生成
        evolution_model = EvolutionModel(selected_latents)
        mutated_latents = evolution_model.random_mutation()
        self.diffusion_model.save_user_log(selected_image_ids)
        self.diffusion_model.generate_images(prompt, mutated_latents)
        self._update_images()

    def _on_local_mutation_clicked(self):
        """ローカル変異ボタンがクリックされたときの処理"""
        # クロップ領域を持つImageDisplayを見つける
        cropped_displays = [display for display in self.image_displays if display.crop_overlay.get_selected_rect()]
        
        if not cropped_displays:
            QMessageBox.warning(self, "Warning", "Please crop an area in at least one image before applying local mutation.")
            return

        # すべての潜在変数を取得
        base_dir, current_step = self.diffusion_model.base_dir, self.diffusion_model.current_step
        all_latents = [
            torch.load(os.path.join(base_dir, f"step_{current_step - 1}", f"latent_{i}.pt"))
            for i in range(len(self.image_displays))
        ]

        # EvolutionModelを初期化
        evolution_model = EvolutionModel(all_latents)

        # 各クロップされた画像に対してローカル変異を適用
        mutated_latents = []
        for i, display in enumerate(self.image_displays):
            if display.crop_overlay.get_selected_rect():
                crop_rect = display.crop_overlay.get_selected_rect()
                mutated_latent = evolution_model.local_mutation(all_latents[i], crop_rect)
                mutated_latents.append(mutated_latent)
            else:
                mutated_latents.append(all_latents[i])

        # 変異した潜在変数を使用して新しい画像を生成
        prompt = self.prompt_input.text()
        self.diffusion_model.generate_images(prompt, mutated_latents)
        self._update_images()

        self.text_output.append("Local mutation applied to cropped areas.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
