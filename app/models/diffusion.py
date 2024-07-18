import torch
import os
import json
from datetime import datetime
from diffusers import AutoPipelineForText2Image
from diffusers.utils.torch_utils import randn_tensor

class DiffusionModel:
    """
    テキストプロンプトから画像を生成し、進化計算のプロセスを管理するクラス

    このクラスは、Stable Diffusion XL Turboモデルを使用して画像を生成し、
    生成された画像と関連データを保存する。
    また、ユーザーの操作ログも記録する
    """

    def __init__(self):
        self._setup_model()
        self._setup_generator()
        self._initialize_attributes()

    def _setup_model(self):
        """Stable Diffusion XL Turboモデルのセットアップ"""
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16,
            variant="fp16"
        )
        self.pipe = self.pipe.to("cuda")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _setup_generator(self):
        """乱数生成器のセットアップ"""
        self.generator = torch.Generator(device="cuda")

    def _initialize_attributes(self):
        """属性の初期化"""
        self.latent_shape = (1, 4, 64, 64)
        self.base_dir = None
        self.current_step = 0
        self.user_logs = []

    def generate_latent(self, seed=None):
        """
        初期ノイズ（潜在変数）を生成する。

        Args:
            seed (int, optional): 乱数のシード値。指定されない場合はランダム。

        Returns:
            torch.Tensor: 生成された潜在変数
        """
        if seed is not None:
            self.generator.manual_seed(seed)
        return randn_tensor(self.latent_shape, device=self.device, generator=self.generator, dtype=torch.float16)

    def generate_images(self, prompt, latents):
        """
        与えられたプロンプトと潜在変数から画像を生成する。

        Args:
            prompt (str): 画像生成のためのテキストプロンプト
            latents (list): 潜在変数のリスト

        Returns:
            tuple: 生成された画像のリスト、ベースディレクトリ、現在のステップ
        """
        self._setup_base_directory()
        images = []

        for i, latent in enumerate(latents):
            image = self._generate_single_image(prompt, latent)
            images.append(image)
            self._save_image_and_latent(image, latent, i)

        self.current_step += 1
        return images, self.base_dir, self.current_step

    def _setup_base_directory(self):
        """ベースディレクトリのセットアップ（初回のみ）"""
        if self.base_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.base_dir = os.path.join("app/data", timestamp)
            os.makedirs(self.base_dir, exist_ok=True)

    def _generate_single_image(self, prompt, latent):
        """単一の画像を生成"""
        return self.pipe(
            prompt=prompt,
            height=512,
            width=512,
            latents=latent,
            num_inference_steps=1,
            guidance_scale=0.0
        ).images[0]

    def _save_image_and_latent(self, image, latent, index):
        """画像と潜在変数を保存"""
        step_dir = os.path.join(self.base_dir, f"step_{self.current_step}")
        os.makedirs(step_dir, exist_ok=True)
        
        image_path = os.path.join(step_dir, f"image_{index}.png")
        latent_path = os.path.join(step_dir, f"latent_{index}.pt")
        
        image.save(image_path)
        torch.save(latent, latent_path)

    def save_user_log(self, selected_image_id, mutation_type, crop_rect=None):
        """
        ユーザーの操作ログを保存する

        Args:
            selected_image_id (int or list): ユーザーが選択した画像のID（複数可）
            mutation_type (str): 変異のタイプ（'random' または 'local'）
            crop_rect (dict, optional): 局所変異の場合のクロップ領域
        """
        log_entry = {
            "step": self.current_step - 1,  # 直前のステップのログを記録
            "selected_image_id": selected_image_id,
            "mutation_type": mutation_type
        }

        if mutation_type == 'local' and crop_rect is not None:
            log_entry["crop_rect"] = crop_rect

        self.user_logs.append(log_entry)
        self._write_user_log_to_file()

    def _write_user_log_to_file(self):
        """ユーザーログをJSONファイルに書き込む"""
        log_path = os.path.join(self.base_dir, "user_log.json")
        with open(log_path, "w") as f:
            json.dump(self.user_logs, f, indent=2)
