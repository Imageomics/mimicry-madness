import torch
from transformers import AutoImageProcessor, AutoModel

from mimicry_madness.constants import HuggingfaceModelIDs

class DINOWrapper(torch.nn.Module):
    def __init__(self, model_path=HuggingfaceModelIDs.DINOv2):
        super().__init__()

        self.model_path = model_path
        self.image_encoder = AutoModel.from_pretrained(model_path)
        self.image_processor = AutoImageProcessor.from_pretrained(model_path)

        self.pretrained_path = model_path
        self.embeddings_dim = 1536  # (CLS + Patch mean)

    def process_image(self, img):
        return self.image_processor(img, return_tensors="pt")["pixel_values"]

    def get_pretrained_path(self):
        return self.pretrained_path

    def get_embedding_dim(self):
        return self.embeddings_dim

    def forward(self, x):
        outputs = self.image_encoder(x)
        if self.model_path == HuggingfaceModelIDs.DINOv2:
            feats = outputs[0]
            cls_token = feats[:, 0, :]
            patch_tokens = feats[:, 1:, :]
            feats = torch.cat([cls_token, patch_tokens.mean(dim=1)], dim=1)

        elif self.model_path == HuggingfaceModelIDs.DINOv3:
            last_hidden_states = outputs.last_hidden_state
            cls_token = last_hidden_states[:, 0, :]
            patch_tokens = last_hidden_states[
                :, 1 + self.image_encoder.config.num_register_tokens :, :
            ]
            feats = torch.cat([cls_token, patch_tokens.mean(dim=1)], dim=1)

        return feats