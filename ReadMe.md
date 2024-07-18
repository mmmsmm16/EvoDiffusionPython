# EvoDiffusionPython

EvoDiffusionPythonは、進化的アルゴリズムと拡散モデルを組み合わせた画像生成ツールです。ユーザーは、テキストプロンプトを入力し、生成された画像に対して局所的な変異や選択を行うことで、望む画像を段階的に生成することができます。

## 機能

- テキストプロンプトからの初期画像生成
- 生成された画像に対する選択と評価
- 選択された画像に基づくランダム変異
- 画像の特定領域に対する局所的な変異
- ユーザー操作のログ記録

## プロジェクト構造

```
.
├── Dockerfile
├── docker-compose.yaml
└── app
    ├── main.py
    ├── data
    │   └── test
    ├── models
    │   ├── diffusion.py
    │   └── evolution.py
    └── ui
        ├── main_window.py
        └── components
            ├── crop_button.py
            ├── crop_overlay.py
            └── image_display.py
```

## セットアップ

このプロジェクトは Docker を使用して環境を構築する

1. リポジトリをクローン：
   ```
   git clone https://github.com/mmmsmm16/EvoDiffusionPython.git
   cd EvoDiffusionPython
   ```

2. Docker イメージをビルドし、コンテナを起動：
   ```
   docker-compose up --build
   ```

3. アプリケーションが起動し、指定されたポートでアクセス可能になる

## 使用方法

1. ブラウザまたはアプリケーションウィンドウでツールを開く

2. テキストプロンプトを入力し、「Set prompt」ボタンをクリックして初期画像を生成

3. 生成された画像から好みのものを選択

4. 「Generate」ボタンをクリックして、選択した画像に基づいて新しい画像を生成

5. 局所的な変異を適用したい場合：
   - 「Crop」ボタンをクリックし、画像上で変異を適用したい領域を選択
   - 「Apply Local Mutation」ボタンをクリックして、選択した領域に変異を適用

6. 希望の結果が得られるまで、選択と生成のプロセスを繰り返す

## 主なコンポーネント

- `app/main.py`: アプリケーションのエントリーポイント
- `app/ui/main_window.py`: アプリケーションのメインウィンドウとユーザーインターフェース
- `app/ui/components/image_display.py`: 個々の画像表示と操作を管理
- `app/ui/components/crop_overlay.py`: 画像上でのクロッピング領域の選択を管理
- `app/models/diffusion.py`: 画像生成と潜在変数の管理
- `app/models/evolution.py`: 画像の交叉（未実装）・変異処理を担当
