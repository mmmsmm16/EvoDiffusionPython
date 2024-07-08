import torch
import os
import json
from datetime import datetime
from diffusers import AutoPipelineForText2Image
from diffusers.utils.torch_utils import randn_tensor

class  DiffusionModel():
    def __init__(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")  # モデルのロード
        self.pipe = self.pipe.to("cuda") # GPU に転送
        self.generator = torch.Generator(device="cuda") # 乱数生成器
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
        self.latent_shape = (1, 4, 64, 64) # 潜在変数の形状
        self.base_dir = None # データ保存ディレクトリ
        self.current_step = 0 # 現在の進化計算のステップ
        self.user_logs = [] # ユーザの操作ログ
        
    # 初期ノイズの生成関数
    def generate_latent(self, seed):
        if seed is not None:
            self.generator.manual_seed(seed)
        return randn_tensor(self.latent_shape, device=self.device, generator=self.generator, dtype=torch.float16)
    
    # 画像生成関数
    def generate_images(self, prompt, latents):
        if self.base_dir is None: # 初期画像を生成する場合
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.base_dir = os.path.join("app/data", timestamp)
            os.makedirs(self.base_dir, exist_ok=True)

        images = []
        for i, latent in enumerate(latents):
            image = self.pipe(prompt=prompt, height=512, width=512, latents=latent, num_inference_steps=1, guidance_scale=0.0).images[0]
            images.append(image)

            # 画像と潜在変数の保存
            step_dir = os.path.join(self.base_dir, f"step_{self.current_step}")
            os.makedirs(step_dir, exist_ok=True)
            image_path = os.path.join(step_dir, f"image_{i}.png")
            latent_path = os.path.join(step_dir, f"latent_{i}.pt")
            image.save(image_path)
            torch.save(latent, latent_path)

        self.current_step += 1
        return images, self.base_dir, self.current_step

    def save_user_log(self, selected_image_id):
        self.user_logs.append({
            "step": self.current_step - 1,  # 直前のステップのログを記録
            "selected_image_id": selected_image_id
        })
        with open(os.path.join(self.base_dir, "user_log.json"), "w") as f:
            json.dump(self.user_logs, f)
