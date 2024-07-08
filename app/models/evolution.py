import torch
import os
from diffusers.utils.torch_utils import randn_tensor

class EvolutionModel():
    def __init__(self, selected_latents):
        self.selected_latents = selected_latents
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = torch.float16
        self.latent_shape = (1, 4, 64, 64)
        self.population_size = 4
        self.mutation_rate = 1.0

    # RamdomMutation
    def random_mutation(self):
        mutated_latents = []
        num_selected = len(self.selected_latents)
        
        # ユーザが一枚の画像を選択した場合
        if num_selected == 1:
            z0 = self.selected_latents[0]
            for i in range(i, self.population_size):
                noise = randn_tensor(self.latent_shape, dtype=self.dtype, device=self.device) * (i / self.population_size) * self.mutation_rate 
                new_z = z0 + noise
                # 正規化
                new_z = new_z / torch.norm(new_z) * (torch.sqrt(torch.tensor(float(torch.prod(torch.tensor(self.latent_shape))))))
                mutated_latents.append(new_z)
            # 変異強度の更新
            self.mutation_rate *= 0.7
            
        # ユーザが複数の画像を選択した場合
        elif num_selected > 1:
            avg_z = torch.mean(torch.stack(self.selected_latents), dim=0)
            for i in range(1, self.population_size):
                noise = randn_tensor(self.latent_shape, dtype=self.dtype, device=self.device) * (i / self.population_size) * self.mutation_rate
                new_z = avg_z + noise
                # 正規化
                new_z = new_z / torch.norm(new_z) * (torch.sqrt(torch.tensor(float(torch.prod(torch.tensor(self.latent_shape))))))
                mutated_latents.append(new_z)
        else:
            raise ValueError("No images selected.")

        return mutated_latents
