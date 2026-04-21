# Image Similarity Search System
**NTU Final Year Project (FYP)**

A desktop-based offline image similarity search application built with Python, using ResNet50 and FAISS.

## Features
- Deep feature-based similarity search (ResNet50 + FAISS)
- User-friendly GUI with image preview
- Support common image formats (JPG, PNG, WebP, etc.)
- Build index from local folders (with subfolder support)
- Adjustable similarity threshold
- Batch operations: Copy, Move, Delete selected images
- Open file location directly from results

## Project Structure
ImageSearch/
├── main.py
├── config.py
├── core/
├── ui/
└── utils/


## How to Run
1. Install dependencies:
   ```bash
   pip install torch torchvision faiss-cpu pillow send2trash

2. Run the app:
   ```bash
   python main.py

Academic Info
Student Name: Li Zhe
Student ID: U2320772D
Institution: Nanyang Technological University (NTU)


Next:
```bash
git add README.md
git commit -m "Add README for FYP"
git push
