# Wave File Analysis App (Wave Analyzer)

A cross-platform desktop application built with Python and CustomTkinter to parse and visualize Wave (`.wav`) files.

## Features
- **Metadata extraction**: Shows channels, sampling rate, bit depth, duration, and frame count.
- **Waveform Visualization**: Plots the time-domain amplitude of the audio.
- **Spectrogram**: Visualizes the frequency spectrum over time using a viridis colormap.
- **Cross-platform**: Works on Windows, macOS, and Linux.

---

## 🛠 環境構築手順 (Setup Instructions)

このアプリケーションを実行するには Python 3.8 以上がインストールされている必要があります。
プラットフォームごとの環境構築手順は以下の通りです。

### 1. Windows の場合

1. コマンドプロンプトまたは PowerShell を開きます。
2. アプリケーションのフォルダ（この README があるフォルダ）に移動します。
   ```cmd
   cd C:\path\to\antigravity_wave_file_analysis
   ```
3. 仮想環境（.venv）を作成します。
   ```cmd
   python -m venv .venv
   ```
4. 仮想環境を有効化（アクティベート）します。
   ```cmd
   .venv\Scripts\activate
   ```
   *(PowerShellを使用していてスクリプトの実行が許可されていない場合は `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` を事前に実行してください)*
5. 必要なライブラリをインストールします。
   ```cmd
   pip install -r requirements.txt
   ```
6. アプリケーションを起動します。
   ```cmd
   python app.py
   ```

### 2. macOS の場合

1. ターミナル (Terminal) を開きます。
2. アプリケーションのフォルダに移動します。
   ```bash
   cd /Users/k-abe/github/antigravity_wave_file_analysis
   ```
3. 仮想環境（.venv）を作成します。
   ```bash
   python3 -m venv .venv
   ```
4. 仮想環境を有効化します。
   ```bash
   source .venv/bin/activate
   ```
5. 必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
6. アプリケーションを起動します。
   ```bash
   python app.py
   ```

### 3. Linux (Ubuntu/Debian等) の場合

1. ターミナルを開きます。
2. まずシステム全体として `python3-venv` などの開発パッケージがインストールされていることを確認します。
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip
   ```
3. アプリケーションのフォルダに移動します。
   ```bash
   cd /path/to/antigravity_wave_file_analysis
   ```
4. 仮想環境（.venv）を作成します。
   ```bash
   python3 -m venv .venv
   ```
5. 仮想環境を有効化します。
   ```bash
   source .venv/bin/activate
   ```
6. 必要なライブラリをインストールします（GUI描画に必要なtkinterライブラリもOS側で必要になる場合があります）。
   ```bash
   sudo apt install python3-tk
   pip install -r requirements.txt
   ```
7. アプリケーションを起動します。
   ```bash
   python app.py
   ```

---

## 💡 その他の使い方
テスト用の音声ファイルがない場合は、以下のコマンドでテスト用の `sample.wav` を自動生成できます。（仮想環境を有効化した状態で実行してください）
```bash
python generate_sample.py
```
