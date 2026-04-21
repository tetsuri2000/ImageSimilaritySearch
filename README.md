# Image Similarity Search System
**NTU Final Year Project (FYP)**

A desktop-based offline image similarity search application that uses ResNet50 deep features and FAISS for fast image retrieval.

## Features
- Deep learning-based image similarity search (ResNet50 + FAISS)
- User-friendly GUI interface
- Support JPG, PNG, BMP, GIF, WebP
- Build image index from local folder
- Adjustable similarity threshold
- Image preview and result display
- Batch operations: Copy, Move, Delete
- Open file location directly
- All processing runs locally (privacy-focused)

## Technologies
- Python
- Tkinter (GUI)
- PyTorch / ResNet50
- FAISS
- Pillow


## How to Run
1. Install dependencies:
   ```bash
   pip install torch torchvision faiss-cpu pillow send2trash
   
2. Run the app:
   python main.py
   
   
## NTU FYP Information
- Student: Li Zhe
- Project Title: Similar Image Search System
- Institution: Nanyang Technological University
