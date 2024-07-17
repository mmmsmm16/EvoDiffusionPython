import torch
from diffusers.utils.torch_utils import randn_tensor

class EvolutionModel:
    """
    画像生成のための進化モデルを実装するクラス

    このクラスは、選択された潜在変数に基づいて新しい潜在変数を生成し、
    画像の進化プロセスをシミュレートする
    """

    def __init__(self, selected_latents):
        """
        EvolutionModelの初期化

        Args:
            selected_latents (list): 選択された潜在変数のリスト
        """
        self.selected_latents = selected_latents
        self._setup_device_and_dtype()
        self._initialize_parameters()

    def _setup_device_and_dtype(self):
        """デバイスとデータ型のセットアップ"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = torch.float16

    def _initialize_parameters(self):
        """進化パラメータの初期化"""
        self.latent_shape = (1, 4, 64, 64)
        self.population_size = 4
        self.mutation_rate = 1.0

    def random_mutation(self):
        """
        ランダムな変異を適用して新しい潜在変数を生成する

        Returns:
            list: 変異後の潜在変数のリスト
        """
        num_selected = len(self.selected_latents)
        
        if num_selected == 0:
            raise ValueError("No images selected.")
        elif num_selected == 1:
            return self._mutate_single_latent()
        else:
            return self._mutate_multiple_latents()

    def _mutate_single_latent(self):
        """単一の潜在変数に対する変異"""
        mutated_latents = []
        z0 = self.selected_latents[0]
        
        for i in range(1, self.population_size + 1):
            noise = self._generate_noise(i)
            new_z = z0 + noise
            normalized_z = self._normalize_latent(new_z)
            mutated_latents.append(normalized_z)
        
        self._update_mutation_rate()
        return mutated_latents

    def _mutate_multiple_latents(self):
        """複数の潜在変数に対する変異"""
        mutated_latents = []
        avg_z = torch.mean(torch.stack(self.selected_latents), dim=0)
        
        for i in range(1, self.population_size + 1):
            noise = self._generate_noise(i)
            new_z = avg_z + noise
            normalized_z = self._normalize_latent(new_z)
            mutated_latents.append(normalized_z)
        
        return mutated_latents

    def _generate_noise(self, index):
        """ノイズの生成"""
        return randn_tensor(self.latent_shape, dtype=self.dtype, device=self.device) * (index / self.population_size) * self.mutation_rate

    def _normalize_latent(self, latent):
        """潜在変数の正規化"""
        norm_factor = torch.sqrt(torch.tensor(float(torch.prod(torch.tensor(self.latent_shape)))))
        return latent / torch.norm(latent) * norm_factor

    def _update_mutation_rate(self):
        """変異率の更新"""
        self.mutation_rate *= 0.7

    def local_mutation(self, target_pixel):
        """
        指定範囲のピクセルを新しいランダムノイズで置き換える

        Args:
            target_pixel (tuple): 置き換えるピクセルの座標 (x_start, y_start, x_end, y_end)

        Returns:
            list: 変異後の潜在変数リスト
        """
        mutated_latents = []
        x_start, y_start, x_end, y_end = target_pixel

        for latent in self.selected_latents:
            edited_latent = self._edit_latent(latent, target_pixel)
            mutated_latents.append(edited_latent)

        return mutated_latents

    def _edit_latent(self, initial_latent, target_pixel):
        """
        指定されたピクセル範囲を新しいランダムノイズで置き換える関数

        Args:
            initial_latent (torch.Tensor): 編集する潜在変数
            target_pixel (tuple): 編集対象のピクセル範囲を指定する(x_start, y_start, x_end, y_end)

        Returns:
            torch.Tensor: 編集された潜在変数
        """
        x_start, y_start, x_end, y_end = target_pixel
        
        # 潜在変数のサイズを取得
        _, channels, height, width = initial_latent.shape
        
        # 編集対象のピクセル範囲を置き換え
        edited_latent = initial_latent.clone()
        
        # 新しいランダムノイズを生成（すべてのチャネルに対して）
        new_noise = randn_tensor((1, channels, y_end - y_start, x_end - x_start), 
                                 dtype=self.dtype, device=self.device)
        
        # すべてのチャネルに対して新しいノイズを適用
        edited_latent[:, :, y_start:y_end, x_start:x_end] = new_noise

        # 編集された潜在変数を正規化
        normalized_latent = self._normalize_latent(edited_latent)
        
        return normalized_latent
