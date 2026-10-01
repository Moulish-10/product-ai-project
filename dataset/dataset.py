from huggingface_hub import snapshot_download

dataset_path = snapshot_download(
    repo_id="KeenForgeAI/NEU-DET-corrected",
    repo_type="dataset",
    local_dir="./data/neu_det_raw",
)

print("Dataset downloaded to:")
print(dataset_path)